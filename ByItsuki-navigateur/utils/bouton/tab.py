from datetime import datetime
import json
from pathlib import Path
import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage
from utils.search_profil.silence_log_js import SilentWebEnginePage

from utils import (
    base_style,
    root_history,
)


def create_tab(parent, profile, title="Nouvel onglet",
                min_width=800, max_width=None, min_height=600, max_height=None):
    """Crée un nouvel onglet avec un QWebEngineView configuré."""


    #--- Chemin du répertoire d'historique ---
    history_root = root_history()
    history_general = history_root / "general"
    history_general.mkdir(parents=True, exist_ok=True)

    historique_index = parent.tab.count() + 1
    folder_name = history_root / f"tab_{historique_index}"
    folder_name.mkdir(parents=True, exist_ok=True)

    history_root = folder_name
    # Entrée d'accueil pour l'historique
    moteur = os.getenv("MOTEURRECHERCHE", "GOOGLE").upper()
    moteur_str = os.getenv(moteur).split("search?q=")[0]

    accueil_entry = {
        "index": 0,
        "timestamp": datetime.now().isoformat(),
        "url": moteur_str,
        "title": "Accueil",
        }
    history_file = history_root / "history.json"
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump([accueil_entry], f, ensure_ascii=False, indent=2)

    tab_widget = QWidget()
    layout = QVBoxLayout(tab_widget)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)

    web_view = QWebEngineView()
    # vide l'historique à la création de l'onglet pour garder la version personnalisée
    web_view.history().clear()
    page = SilentWebEnginePage(profile, web_view)
    web_view.setPage(page)

    web_view.setMinimumSize(min_width, min_height)
    web_view.setMaximumSize(max_width or 16777215, max_height or 16777215)
    web_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    web_view.setHtml(base_style())

    def update_tab_icon(icon):
        index = parent.tab.indexOf(tab_widget)
        if index >= 0 and not icon.isNull():
            parent.tab.setTabIcon(index, icon)

    web_view.iconChanged.connect(update_tab_icon)

    # --- Stockage interne ---
    tab_widget.title = title
    tab_widget.profile = profile
    tab_widget.web_view = web_view
    tab_widget.history_root = history_root
    tab_widget.current_pos = 0 # position actuelle dans l'historique
    tab_widget.historique_general = []
    tab_widget.page = page
    tab_widget.page.linkClickedSignal.connect(lambda url: parent.url_search.setText(url))


    def on_link_clicked(url):

        # Historique par onglet
        history_file = history_root / "history.json"
        if history_file.exists():
            with open(history_file, "r", encoding="utf-8") as f:
                history_tab = json.load(f)
        else:
            history_tab = []

        # indexation de l'historique
        index = 2
        for i in history_tab:
            index = i["index"] + 1

        entry = {
            "index": index,
            "timestamp": datetime.now().isoformat(),
            "url": url,
            "title": web_view.title(),
        }

        history_tab.append(entry)
        with open(history_file, "w", encoding="utf-8") as f:
            json.dump(history_tab, f, ensure_ascii=False, indent=2)

        tab_widget.current_pos = len(history_tab)
        print(f"Nouvelle position actuelle après clic: {tab_widget.current_pos}")
        # Historique général
        history_general_file = history_general / "history_general.json"
        if history_general_file.exists():
            with open(history_general_file, "r", encoding="utf-8") as f:
                general_history = json.load(f)
        else:
            general_history = []

        general_history.append(entry)
        with open(history_general_file, "w", encoding="utf-8") as f:
            json.dump(general_history, f, ensure_ascii=False, indent=2)


    page.linkClickedSignal.connect(on_link_clicked)
    tab_widget.on_link_clicked = on_link_clicked


    layout.addWidget(web_view)
    return tab_widget

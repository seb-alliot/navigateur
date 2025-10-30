import os
import json
from datetime import datetime
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QSizePolicy, QPushButton, QLineEdit, QComboBox
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
from utils.search_profil.silence_log_js import SilentWebEnginePage
from utils import base_style, root_history
from interface.code import click_link
from utils.classe.gestion_history import GestionHistory

class CreateElements(QWidget):
    def __init__(self, parent, profile, title="Nouvel onglet",
                min_width=800, max_width=None, min_height=600, max_height=None):
        super().__init__(parent)
        self.parent = parent
        self.profile = profile
        self.title = title

        self.setMinimumSize(min_width, min_height)
        self.setMaximumSize(max_width or 16777215, max_height or 16777215)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    # -----------------------------
    def create_button(self, placeholder, slot, **kwargs):
        min_width = kwargs.get("min_width", 200)
        max_width = kwargs.get("max_width", 300)
        min_height = kwargs.get("min_height", 30)
        max_height = kwargs.get("max_height", 45)
        tool_tip = kwargs.get("tool_tip", "")
        extra_style = kwargs.get("extra_style", "")

        button = QPushButton(placeholder)
        button.setMinimumSize(min_width, min_height)
        button.setMaximumSize(max_width, max_height)
        if extra_style:
            button.setStyleSheet(extra_style)
        if tool_tip:
            button.setToolTip(tool_tip)
        button.clicked.connect(slot)
        return button

    # -----------------------------
    def create_input(self, placeholder, slot=None, **kwargs):
        min_width = kwargs.get("min_width", 200)
        max_width = kwargs.get("max_width", None)
        min_height = kwargs.get("min_height", 30)
        max_height = kwargs.get("max_height", 45)
        tool_tip = kwargs.get("tool_tip", "")
        extra_style = kwargs.get("extra_style", "")

        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        input_field.setMinimumSize(min_width, min_height)
        input_field.setMaximumHeight(max_height)
        input_field.setToolTip(tool_tip)
        if max_width:
            input_field.setMaximumWidth(max_width)
        if extra_style:
            input_field.setStyleSheet(extra_style)
        if slot:
            input_field.returnPressed.connect(slot)
        return input_field

    # -----------------------------
    def create_select(self, options=None, default_index=0, **kwargs):
        min_width = kwargs.get("min_width", 200)
        max_width = kwargs.get("max_width", None)
        min_height = kwargs.get("min_height", 30)
        max_height = kwargs.get("max_height", 45)
        tool_tip = kwargs.get("tool_tip", "")

        combo_box = QComboBox()
        combo_box.addItems(options or [])
        combo_box.setCurrentIndex(default_index)
        combo_box.setToolTip(tool_tip)

        if min_width:
            combo_box.setMinimumWidth(min_width)
        if max_width:
            combo_box.setMaximumWidth(16777215 if max_width is None else max_width)
        if min_height:
            combo_box.setMinimumHeight(min_height)
        if max_height:
            combo_box.setMaximumHeight(16777215 if max_height is None else max_height)

        return combo_box

    # -----------------------------
    def create_tab(self, parent, profile, title="Nouvel onglet",
                min_width=800, max_width=None, min_height=600, max_height=None):
        # --- Initialisation de l’historique ---
        history_root = root_history()
        history_general = history_root / "general"
        history_general.mkdir(parents=True, exist_ok=True)

        tab_index = parent.tab.count() + 1
        tab_folder = history_root / f"tab_{tab_index}"
        tab_folder.mkdir(parents=True, exist_ok=True)
        history_file = tab_folder / "history.json"

        # --- Page d'accueil ---
        moteur = os.getenv("MOTEURRECHERCHE", "GOOGLE").upper()
        moteur_str = os.getenv(moteur, "https://www.google.com/search?q=").split("search?q=")[0]

        accueil_entry = {
            "timestamp": datetime.now().isoformat(),
            "url": moteur_str,
            "title": "Accueil",
        }

        with open(history_file, "w", encoding="utf-8") as f:
            json.dump([accueil_entry], f, ensure_ascii=False, indent=2)

        # --- Configuration du widget onglet ---
        tab_widget = QWidget()
        layout = QVBoxLayout(tab_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        web_view = QWebEngineView()
        web_view.history().clear()
        page = SilentWebEnginePage(profile, web_view)
        web_view.setPage(page)
        web_view.setHtml(base_style())

        # --- Infos internes ---
        tab_widget.title = title
        tab_widget.profile = profile
        tab_widget.web_view = web_view
        tab_widget.history_root = tab_folder
        tab_widget.history_file = history_file
        tab_widget.current_pos = 0
        tab_widget.page = page

        # --- Historique des liens ---
        def on_link_clicked(url):
            data = click_link(url, tab_index, web_view.title(), history_general, tab_widget.current_pos)
            if data:
                tab_widget.current_pos = data["current_pos"]
                tab_widget.history_tab = data["history_tab"]
                url = data["url"]
            tab_widget.history_manager.add_entry(url, title)


        page.linkClickedSignal.connect(on_link_clicked)
        tab_widget.on_link_clicked = on_link_clicked


        # --- Icône d’onglet ---
        def update_tab_icon(icon):
            index = parent.tab.indexOf(tab_widget)
            if index >= 0 and not icon.isNull():
                parent.tab.setTabIcon(index, icon)

        def update_url(url):
            if hasattr(parent, "url_search"):
                parent.url_search.setText(url.toString())

        web_view.iconChanged.connect(update_tab_icon)
        web_view.urlChanged.connect(update_url)

        tab_widget.tab_index = tab_index

        # --- Charger la page d’accueil ---
        web_view.load(QUrl(accueil_entry["url"]))

        # --- Navigation personnalisée ---
        tab_widget.history_manager = GestionHistory(tab_widget, parent.url_search, tab_widget.history_file)
        layout.addWidget(web_view)

        return tab_widget

import sys
from pathlib import Path
from datetime import datetime

from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtCore import Signal, QUrl

from utils.base_style_page import base_style

# === Pour afficher les logs JS  et voir les liens cliqués ===
class DebugWebEnginePage(QWebEnginePage):
    linkClickedSignal = Signal(str)  # signal personnalisé pour URL cliquée

    def javaScriptConsoleMessage(self, level, message, line, source_id):
        print(f"[JS:{level.name}] {message} ({source_id}:{line})")
        super().javaScriptConsoleMessage(level, message, line, source_id)

    def acceptNavigationRequest(self, url, nav_type, isMainFrame):
        if nav_type == QWebEnginePage.NavigationTypeLinkClicked:
            url_str = url.toString()
            self.linkClickedSignal.emit(url_str)
            print("Émission du signal linkClickedSignal avec l'URL :", url_str)

        return super().acceptNavigationRequest(url, nav_type, isMainFrame)


def create_tab(parent, profile, title="Nouvel onglet",
                min_width=800, max_width=None, min_height=600, max_height=None):
    """Crée un nouvel onglet avec un QWebEngineView configuré."""

    base = Path(__file__).resolve().parent.parent.parent.parent
    if str(base) not in sys.path:
        sys.path.append(str(base))
    history_root = base / "ByItsuki-navigateur" / "configuration" / "storage" / "historique"
    print("Chemin du répertoire d'historique :", history_root)
    tab_widget = QWidget()
    layout = QVBoxLayout(tab_widget)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)

    web_view = QWebEngineView()
    page = DebugWebEnginePage(profile, web_view)
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
    tab_widget.historique = []
    tab_widget.page = page
    tab_widget.page.linkClickedSignal.connect(lambda url: parent.url_search.setText(url))

    def on_link_clicked(url):
        tab_widget.historique.append(url)
        print("Historique mis à jour :", tab_widget.historique)
        parent.url_search.setText(url)
        history_root.mkdir(parents=True, exist_ok=True)
        history_file = history_root / "history.txt"
        print("Chemin du fichier d'historique :", history_file)
        with open(history_file, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().isoformat()} - {url}\n")

    page.linkClickedSignal.connect(on_link_clicked)

    layout.addWidget(web_view)
    return tab_widget

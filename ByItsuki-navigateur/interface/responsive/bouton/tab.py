from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtCore import QUrl

from utils.base_style_page import base_style

# === Classe personnalisée pour afficher les logs JS dans la console ===
class DebugWebEnginePage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, message, line, source_id):
        # Affiche tout ce que les sites JS envoient à la console
        print(f"[JS:{level.name}] {message} ({source_id}:{line})")
        super().javaScriptConsoleMessage(level, message, line, source_id)


def create_tab(parent, profile, title="Nouvel onglet",
                min_width=800, max_width=None, min_height=600, max_height=None):
    """Crée un nouvel onglet avec un QWebEngineView configuré."""

    # --- Conteneur principal ---
    tab_widget = QWidget()
    layout = QVBoxLayout(tab_widget)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)

    # --- Vue Web ---
    web_view = QWebEngineView()

    # Utilisation de la page personnalisée (avec logs JS)
    page = DebugWebEnginePage(profile, web_view)
    web_view.setPage(page)

    # --- Taille et comportement ---
    web_view.setMinimumSize(min_width, min_height)
    web_view.setMaximumSize(max_width or 16777215, max_height or 16777215)
    web_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    # --- User-Agent personnalisé ---
    page.profile().setHttpUserAgent(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/129.0.6668.90 Safari/537.36"
    )

    # --- Page d’accueil par défaut ---
    web_view.setHtml(base_style())

    def update_tab_icon(icon):
        index = parent.tab.indexOf(tab_widget)
        if index >= 0 and not icon.isNull():
            parent.tab.setTabIcon(index, icon)


    web_view.iconChanged.connect(update_tab_icon)
    # --- Stockage interne ---
    tab_widget.title = title
    tab_widget.web_view = web_view

    layout.addWidget(web_view)
    return tab_widget

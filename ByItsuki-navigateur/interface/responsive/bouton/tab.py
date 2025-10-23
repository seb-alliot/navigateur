from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PyQt6.QtWebEngineWidgets import QWebEngineView
from utils.silence_log_js import SilentWebEnginePage
from utils.base_style_page import base_style

def create_tab(parent, profile, title="Nouvel onglet",
                min_width=800, max_width=None, min_height=600, max_height=None):

    # --- Conteneur principal de l’onglet ---
    tab_widget = QWidget()
    layout = QVBoxLayout(tab_widget)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)

    # --- Vue Web ---
    web_view = QWebEngineView()
    page = SilentWebEnginePage(profile, web_view)
    web_view.setPage(page)

    # Taille et comportement
    web_view.setMinimumSize(min_width, min_height)
    web_view.setMaximumSize(max_width or 16777215, max_height or 16777215)
    web_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    # Page par défaut (style interne)
    web_view.setHtml(base_style())

    # --- Stockage interne pour l’accès rapide depuis Principal ---
    tab_widget.title = title
    tab_widget.web_view = web_view

    layout.addWidget(web_view)
    return tab_widget

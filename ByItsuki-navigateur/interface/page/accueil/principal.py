import os
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))
icon_root = project_root / "interface" / "img" / "asset" / "icons"

from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QApplication, QSizePolicy, QTabWidget
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile

from interface.page.base_page import BasePage
from interface.page.parametre.menu_parametre import Menu_parametre
from interface.code.recherche.recherche import research
from interface.responsive import create_button, create_input
from utils.base_style_page import base_style
from utils.silence_log_js import SilentWebEnginePage


class Principal(BasePage):
    def __init__(self):
        super().__init__()


                # --- Profil pour les pages Web ---
        self.profile = QWebEngineProfile("custom_profile", self)
        self.profile.setHttpUserAgent(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/118.0.5993.118 Safari/537.36 "
            "ByItsuki-Navigateur/1.0 (Windows NT 10.0; Win64; x64)"
        )

        self.init_ui()


    def init_ui(self):
        # --- Barre d'adresse ---
        self.url_search = create_input("Barre d'adresse", self.search, 500, None, 40, 40)
        address_layout = QHBoxLayout()
        address_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        address_layout.addWidget(self.url_search)

        # --- Boutons ---
        self.search_button = create_button("🔍", self.search, 40, 40, 40, 40, "Lancer la recherche")
        address_layout.addWidget(self.search_button)

        self.open_button = create_button("+", self.new_tab, 40, 40, 40, 40, "Nouvel onglet")
        address_layout.addWidget(self.open_button)

        self.parameter_menu_button = create_button("", self.menu_parametre, 40, 40, 40, 40, "Paramètres")
        self.parameter_menu_button.setIcon(QIcon(str(icon_root / "menu_logo.png")))
        self.parameter_menu_button.setIconSize(QSize(24, 24))
        address_layout.addWidget(self.parameter_menu_button)

        self.content_layout.addLayout(address_layout)

        # --- Onglets ---
        self.tab = QTabWidget()
        self.content_layout.addWidget(self.tab)

        # --- Onglet de base (Accueil) ---
        self.home_tab = QWebEngineView()
        self.home_tab.setPage(SilentWebEnginePage(self.profile, self))
        self.home_tab.setHtml(base_style())
        self.tab.addTab(self.home_tab, "Accueil")
        self.tab.setCurrentWidget(self.home_tab)

    def menu_parametre(self):
        self.param_menu = Menu_parametre()
        self.param_menu.show()

    def new_tab(self):
        new_web_view = QWebEngineView()
        new_web_view.setPage(SilentWebEnginePage(self.profile, self))
        new_web_view.setMinimumSize(1024, 768)
        new_web_view.setHtml(base_style())

        # Ajouter un nouvel onglet
        index = self.tab.addTab(new_web_view, "Nouvel onglet")
        self.tab.setCurrentWidget(new_web_view)
        self.url_search.setText("")

        new_web_view.titleChanged.connect(lambda title, i=index: self.tab.setTabText(i, title[:30]))


    def search(self):
        current_web_view = self.tab.currentWidget()
        if not current_web_view:
            return

        query = self.url_search.text().strip()
        if not query:
            return
        url = research(self, query)
        if url:
            current_web_view.load(url[0])
            self.url_search.setText(url[0].toString())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = Principal()
    main_window.show()
    sys.exit(app.exec())

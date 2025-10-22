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
from interface.responsive import create_button, create_input , create_tab
from utils.root_icon import resource_path
from utils.profil_search import create_profile

class Principal(BasePage):
    def __init__(self):
        super().__init__()


        # --- Profil pour les pages Web ---
        self.profile = create_profile(self)

        self.init_interface()


    def init_interface(self):
        # --- Barre d'adresse ---
        self.url_search = create_input("Barre d'adresse", self.search, 500, None, 40, 40)
        address_layout = QHBoxLayout()
        address_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        address_layout.addWidget(self.url_search)

        # --- Boutons ---
        self.search_button = create_button("🔍", self.search, 40, 40, 40, 40, "Lancer la recherche")
        # Connecter la barre d'adresse à la recherche via le bouton Entrée = returnPressed.connect
        self.url_search.returnPressed.connect(self.search)
        address_layout.addWidget(self.search_button)

        self.open_button = create_button("+", self.new_tab, 40, 40, 40, 40, "Nouvel onglet")
        address_layout.addWidget(self.open_button)

        self.parameter_menu_button = create_button("", self.menu_parametre, 40, 40, 40, 40, "Paramètres")
        icon_file = resource_path("interface/img/asset/icons/menu_logo.png")
        self.parameter_menu_button.setIcon(QIcon(str(icon_file)))
        # self.parameter_menu_button.setIcon(QIcon(str(icon_root / "menu_logo.png") if icon_root.exists() else icon_file))
        self.parameter_menu_button.setIconSize(QSize(24, 24))
        address_layout.addWidget(self.parameter_menu_button)

        self.content_layout.addLayout(address_layout)

        # --- Onglets ---
        self.tab = QTabWidget()
        self.content_layout.addWidget(self.tab)

        # --- Onglet de base (Accueil) ---
        self.home_tab = create_tab(self, profile=self.profile)
        self.tab.addTab(self.home_tab, "Accueil")
        self.tab.setCurrentWidget(self.home_tab)
        self.home_tab.web_view.titleChanged.connect(lambda title: self.tab.setTabText(0, title[:30] if self.url_search.text().strip() != "" else "Accueil"))


    def menu_parametre(self):
        self.param_menu = Menu_parametre()
        self.param_menu.show()


    def new_tab(self):
        new_tab = create_tab(self, profile=self.profile)
        # Ajouter un nouvel onglet
        index = self.tab.addTab(new_tab, new_tab.title)
        self.tab.setCurrentWidget(new_tab)
        self.url_search.setText("")
        new_tab.web_view.titleChanged.connect(lambda title, i=index: self.tab.setTabText(i, title[:30] if self.url_search.text().strip() != "" else "Nouvel onglet"))


    def search(self):
        use_tab = self.tab.currentWidget()
        if not use_tab or not hasattr(use_tab, "web_view"):
            return

        query = self.url_search.text().strip()
        if not query:
            return

        url = research(self, query)
        if url:
            use_tab.web_view.load(url[0])
            self.url_search.setText(url[0].toString())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = Principal()
    main_window.show()
    sys.exit(app.exec())

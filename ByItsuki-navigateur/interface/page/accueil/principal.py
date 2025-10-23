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
        address_layout = QHBoxLayout()

        self.button_back = create_button("←", self.back, 40, 40, 40, 40, "Retourner à la page précédente")
        self.button_back.clicked.connect(self.back)
        address_layout.addWidget(self.button_back)

        self.button_forward = create_button("→", self.forward, 40, 40, 40, 40, "Aller à la page suivante")
        self.button_forward.clicked.connect(self.forward)
        address_layout.addWidget(self.button_forward)

        self.reload_button = create_button("⟳", self.reload, 40, 40, 40, 40, "Recharger la page")
        self.reload_button.clicked.connect(self.reload)
        address_layout.addWidget(self.reload_button)

        self.url_search = create_input("Barre de recherche...", self.search, 500, None, 40, 40)

        address_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        address_layout.addWidget(self.url_search)

        self.search_button = create_button("🔍", self.search, 40, 40, 40, 40, "Lancer la recherche")
        # Connecter la barre d'adresse à la recherche via le bouton Entrée = returnPressed.connect
        self.url_search.returnPressed.connect(self.search)
        address_layout.addWidget(self.search_button)

        self.open_button = create_button("+", self.new_tab, 40, 40, 40, 40, "Nouvel onglet")
        address_layout.addWidget(self.open_button)

        self.parameter_menu_button = create_button("", self.menu_parametre, 40, 40, 40, 40, "Paramètres")
        icon_file = resource_path("interface/img/asset/icons/menu_logo.png")
        self.parameter_menu_button.setIcon(QIcon(str(icon_file)))
        # la ligne en dessous est a commenter quand on compile en .exe
        self.parameter_menu_button.setIcon(QIcon(str(icon_root / "menu_logo.png") if icon_root.exists() else icon_file))
        self.parameter_menu_button.setIconSize(QSize(24, 24))
        address_layout.addWidget(self.parameter_menu_button)

        self.content_layout.addLayout(address_layout)

        # --- Onglets ---
        self.tab = QTabWidget()
        self.tab.setTabsClosable(True)
        self.tab.currentChanged.connect(self.change_tab)
        self.tab.tabCloseRequested.connect(lambda index: self.tab.removeTab(index))
        self.content_layout.addWidget(self.tab)

        # --- Onglet de base (Accueil) ---
        self.home_tab = create_tab(self, profile=self.profile)
        self.tab.addTab(self.home_tab, "Accueil")
        self.tab.setCurrentWidget(self.home_tab)
        self.home_tab.web_view.titleChanged.connect(lambda title: self.tab.setTabText(0, title[:30] if self.url_search.text().strip() != "" else "Accueil"))

    # Navigation des onglets
    def back(self):
        use_tab = self.tab.currentWidget()
        if use_tab and hasattr(use_tab, "web_view"):
            use_tab.web_view.back()
    def forward(self):
        use_tab = self.tab.currentWidget()
        if use_tab and hasattr(use_tab, "web_view"):
            use_tab.web_view.forward()
    def reload(self):
        use_tab = self.tab.currentWidget()
        if use_tab and hasattr(use_tab, "web_view"):
            use_tab.web_view.reload()

    def menu_parametre(self):
        self.param_menu = Menu_parametre()
        self.param_menu.show()


    def new_tab(self):
        self.news_tab = create_tab(self, profile=self.profile)
        # Ajouter un nouvel onglet
        index = self.tab.addTab(self.news_tab, self.news_tab.title)
        self.tab.setCurrentWidget(self.news_tab)
        self.url_search.setText("")
        # Mettre à jour le titre de l’onglet lors du changement de page
        self.news_tab.web_view.titleChanged.connect(lambda title, i=index: self.tab.setTabText(i, title[:30] if self.url_search.text().strip() != "" else "Nouvel onglet"))

    def change_tab(self, index):
        self.tab.setCurrentIndex(index)
        self.url_search.setText(self.tab.currentWidget().web_view.url().toString())

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

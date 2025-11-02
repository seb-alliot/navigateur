import os
import sys
import json
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))


from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QApplication, QSizePolicy, QTabWidget, QComboBox , QWidget
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize, QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineProfile

from interface.page.base_page import BasePage
from interface.page.parametre.menu_parametre import Menu_parametre
from interface.code import (
    close_tab_window,
)

from utils import (
    root_icon,
    create_profile,
    CreateElements,
    root_history,
    site_name,
)


class Principal(BasePage):
    def __init__(self):
        super().__init__()
        # --- Profil pour les pages Web ---
        self.profile = create_profile(self)
        self.creator = CreateElements(self, self.profile)
        self.init_interface()


    def init_interface(self):

        self.content_navigation = QVBoxLayout()
        self.content_layout.addLayout(self.content_navigation)

        # --- Barre d'adresse ---
        address_layout = QHBoxLayout()

        self.button_back = self.creator.create_button("←", self.back, min_width=40, min_height=40, max_height=40, max_width=40, tool_tip="Page précédente")
        address_layout.addWidget(self.button_back)

        self.button_forward = self.creator.create_button("→", self.forward, min_width=40, min_height=40, max_height=40, max_width=40, tool_tip="Page suivante")
        address_layout.addWidget(self.button_forward)

        self.reload_button = self.creator.create_button("⟳", self.reload, min_width=40, min_height=40, max_height=40, max_width=40, tool_tip="Recharger la page")
        self.reload_button.clicked.connect(self.reload)
        address_layout.addWidget(self.reload_button)

        self.start = self.creator.create_button("🏠", self.go_home, min_width=40, min_height=40, max_height=40, max_width=40, tool_tip="Page d'accueil")
        address_layout.addWidget(self.start)

        self.choice_moteur = self.creator.create_select(
            options=["Google", "Bing", "DuckDuckGo", "Qwant"],
            default_index=0,
            min_width=50,
            max_width=100,
            min_height=40,
            max_height=40,
            tooltip="Choisir le moteur de recherche"
        )
        address_layout.addWidget(self.choice_moteur)

        self.url_search = self.creator.create_input("Barre de recherche...", self.search, min_width=500, max_width=None, min_height=40, max_height=40, tool_tip="Entrer votre recherche ou URL ici")
        address_layout.addWidget(self.url_search)

        self.drop_button = self.creator.drop_button(line_edit=self.url_search, icon=None)
        icon_file = root_icon("drop_icon.png")
        self.drop_button.setIcon(QIcon(str(icon_file)))
        self.drop_button.setIconSize(QSize(35, 35))
        self.drop_button.drop.connect(lambda url: self.save_favorites(url))

        index = address_layout.indexOf(self.url_search)
        address_layout.insertWidget(index, self.drop_button)

        self.search_button = self.creator.create_button("🔍", self.search, min_width=40, min_height=40, max_height=40, max_width=40, tool_tip="Lancer la recherche")
        self.url_search.returnPressed.connect(self.search)
        address_layout.addWidget(self.search_button)

        self.open_button = self.creator.create_button("+", self.new_tab, min_width=40, min_height=40, max_height=40, max_width=40, tool_tip="Nouvel onglet")
        address_layout.addWidget(self.open_button)

        self.parameter_menu_button = self.creator.create_button("", self.menu_parametre, min_width=40, min_height=40, max_height=40, max_width=40, tool_tip="Paramètres")
        icon_file = root_icon("menu_icon.png")
        self.parameter_menu_button.setIcon(QIcon(str(icon_file)))
        self.parameter_menu_button.setIconSize(QSize(35, 35))
        address_layout.addWidget(self.parameter_menu_button)
        self.content_layout.addLayout(address_layout)

        # --- nouvelle bar horizontale pour les favoris ---
        self.fav_content = QHBoxLayout()
        self.fav_content.setAlignment(Qt.AlignmentFlag.AlignLeft)
        # --- Barre de favoris ---
        self.favorite_bar = self.creator.fav_bar(parent=self, slot=self.open_favorite, title=None, icon=None, min_height=40, max_height=40)
        self.favorite_bar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.fav_content.addWidget(self.favorite_bar)
        self.content_layout.addLayout(self.fav_content)

        # --- nouvelle bar horizontale pour les onglets ---
        self.onglet_content = QVBoxLayout()
        # --- Onglets ---
        self.onglet_layout = QHBoxLayout()
        self.tab = QTabWidget(self)
        self.tab.setTabsClosable(True)
        self.tab.tabCloseRequested.connect(self.close_tab)
        self.tab.currentChanged.connect(self.change_tab)
        self.onglet_layout.addWidget(self.tab)

        # --- Onglet de base (Accueil) ---
        self.home_tab = self.creator.create_tab(self, profile=self.profile)
        self.tab.addTab(self.home_tab, "Accueil")
        self.tab.setCurrentWidget(self.home_tab)
        self.home_tab.web_view.titleChanged.connect(lambda title: self.tab.setTabText(0, title[:30] if self.url_search.text().strip() != "" else "Accueil"))

        self.content_layout.addLayout(self.onglet_layout)
        self.content_navigation.addLayout(self.onglet_content)
        self.onglet_layout.addWidget(self.tab)

    def back(self):
        tab = self.tab.currentWidget()
        if hasattr(tab, "history_manager"):
            tab.history_manager.back()

    def forward(self):
        tab = self.tab.currentWidget()
        if hasattr(tab, "history_manager"):
            tab.history_manager.forward()

    def reload(self):
        use_tab = self.tab.currentWidget()
        if use_tab and hasattr(use_tab, "web_view"):
            use_tab.web_view.reload()

    # Menu des paramètres
    def menu_parametre(self):
        self.param_menu = Menu_parametre(profile=None)
        self.param_menu.show()

    # Ajouter un nouvel onglet
    def new_tab(self):
        self.news_tab = self.creator.create_tab(self, self.profile)
        # Ajouter un nouvel onglet
        index = self.tab.addTab(self.news_tab, self.news_tab.title)
        self.tab.setCurrentWidget(self.news_tab)
        self.go_home()
        # Met à jour le titre de l’onglet lors du changement de page
        self.news_tab.web_view.titleChanged.connect(lambda title, i=index: self.tab.setTabText(i, title[:30] if self.url_search.text().strip() != "" else "Nouvel onglet"))

    # met à jour la barre d'adresse lors du changement d'onglet
    def change_tab(self, index):
        current_tab = self.tab.widget(index)
        if not current_tab or not hasattr(current_tab, "web_view"):
            self.url_search.clear()
            return
        self.url_search.setText(current_tab.web_view.url().toString())

    # --- Méthode interne commune ---
    def search(self, moteur=None):
        moteur = moteur or self.choice_moteur.currentText().upper()
        default = os.getenv("MOTEURRECHERCHE", "GOOGLE").upper()
        choix = moteur if moteur != default else default

        use_tab = self.tab.currentWidget()
        if not use_tab or not hasattr(use_tab, "web_view"):
            self.new_tab()
            use_tab = self.tab.currentWidget()

        if hasattr(use_tab, "history_manager"):
            use_tab.history_manager.research(choix)


    # Page d'accueil par defaut par rapport au moteur par default
    def go_home(self):
        moteur = os.getenv("MOTEURRECHERCHE", "GOOGLE").upper()
        self.search(moteur)

    # Fermer un onglet
    def close_tab(self, index):
        tab = self.tab.widget(index)
        close_tab_window(self.tab, index, tab)

    # Tout fermer proprement à la fermeture de l'application
    def closeEvent(self, event):
        while self.tab.count() > 0:
            self.close_tab(0)
        event.accept()

    def open_favorite(self, url):
        current_tab = self.tab.currentWidget()
        if current_tab and hasattr(current_tab, "web_view"):
            current_tab.web_view.load(QUrl(url))
            return

    def save_favorites(self, url):
        favoris_file = root_history() / "favoris-bar" / "favoris.json"
        favoris_file.parent.mkdir(parents=True, exist_ok=True)
        if not favoris_file.exists():
            with open(favoris_file, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)
        try:
            with open(favoris_file, "r", encoding="utf-8") as f:
                favoris = json.load(f)
        except (PermissionError, json.JSONDecodeError):
            favoris = []
        entry = {
            "url": url,
            "title": site_name(url, moteur=None),
            "icon": self.tab.currentWidget().web_view.iconUrl().toString()
        }
        if entry:
            favoris.append(entry)
            with open(favoris_file, "w", encoding="utf-8") as f:
                json.dump(favoris, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = Principal()
    main_window.show()
    sys.exit(app.exec())

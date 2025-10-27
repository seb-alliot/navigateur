import os
import sys
import json
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))


from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QApplication, QSizePolicy, QTabWidget, QComboBox
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize, QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineProfile

from interface.page.base_page import BasePage
from interface.page.parametre.menu_parametre import Menu_parametre
from interface.code import (
    research,
    close_tab_window,
)

from utils import (
    create_button,
    create_input,
    create_tab,
    create_select,
    root_icon,
    create_profile,
)

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

        self.start = create_button("🏠", self.go_home, 40, 40, 40, 40, "Page d'accueil")
        self.start.clicked.connect(self.go_home)
        address_layout.addWidget(self.start)

        self.choice_moteur = create_select(["Google", "Bing", "DuckDuckGo", "Qwant"], 0, 100, 40, "Choisir le moteur de recherche")
        address_layout.addWidget(self.choice_moteur)

        self.url_search = create_input("Barre de recherche...", self.search, 500, None, 40, 40, "Entrer votre recherche ou URL ici")

        address_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        address_layout.addWidget(self.url_search)

        self.search_button = create_button("🔍", self.search, 40, 40, 40, 40, "Lancer la recherche")
        # Connecter la barre d'adresse à la recherche via le bouton Entrée = returnPressed.connect
        self.url_search.returnPressed.connect(self.search)
        address_layout.addWidget(self.search_button)

        self.open_button = create_button("+", self.new_tab, 40, 40, 40, 40, "Nouvel onglet")
        address_layout.addWidget(self.open_button)

        self.parameter_menu_button = create_button("", self.menu_parametre, 40, 40, 40, 40, "Paramètres")
        icon_file = root_icon("menu_icon.png")
        self.parameter_menu_button.setIcon(QIcon(str(icon_file)))
        # la ligne en dessous est a commenter quand on compile en .exe
        self.parameter_menu_button.setIcon(QIcon(str(root_icon("menu_icon.png"))))
        self.parameter_menu_button.setIconSize(QSize(24, 24))
        address_layout.addWidget(self.parameter_menu_button)

        self.content_layout.addLayout(address_layout)

        # --- Onglets ---
        self.tab = QTabWidget()
        self.tab.setTabsClosable(True)
        self.tab.currentChanged.connect(self.change_tab)
        self.tab.tabCloseRequested.connect(self.close_tab)
        self.content_layout.addWidget(self.tab)


        # --- Onglet de base (Accueil) ---
        self.home_tab = create_tab(self, profile=self.profile)
        self.tab.addTab(self.home_tab, "Accueil")
        self.tab.setCurrentWidget(self.home_tab)
        self.home_tab.web_view.titleChanged.connect(lambda title: self.tab.setTabText(0, title[:30] if self.url_search.text().strip() != "" else "Accueil"))

        # Charger la page d'accueil par défaut
        self.go_home()


    def back(self):
        tab = self.tab.currentWidget()
        if not tab or not hasattr(tab, "history_root"):
            return

        history_file = tab.history_root / "history.json"
        if not history_file.exists():
            self.go_home()
            return

        with open(history_file, "r", encoding="utf-8") as f:
            history_data = json.load(f)

        if tab.current_pos == 0:
            # On est déjà au début de l'historique
            self.go_home()
            return
        tab.current_pos = tab.current_pos
        tab.current_pos -= 1
        entry = history_data[tab.current_pos]

        tab.web_view.load(QUrl(entry["url"]))
        self.url_search.setText(entry["url"])


    def forward(self):
        tab = self.tab.currentWidget()
        if not tab or not hasattr(tab, "history_root"):
            return

        history_file = tab.history_root / "history.json"
        if not history_file.exists():
            self.go_home()
            return

        with open(history_file, "r", encoding="utf-8") as f:
            history_data = json.load(f)

        if tab.current_pos == 0:
            self.go_home()
            return
        tab.current_pos = tab.current_pos
        tab.current_pos += 1
        entry = history_data[tab.current_pos]

        tab.web_view.load(QUrl(entry["url"]))
        self.url_search.setText(entry["url"])



    def reload(self):
        use_tab = self.tab.currentWidget()
        if use_tab and hasattr(use_tab, "web_view"):
            use_tab.web_view.reload()

    # Menu des paramètres
    def menu_parametre(self):
        self.param_menu = Menu_parametre()
        self.param_menu.show()

    # Ajouter un nouvel onglet
    def new_tab(self):
        self.news_tab = create_tab(self, self.profile)
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
    def base_page(self, query=None, moteur=None):
        query = (query or "").strip()
        moteur = moteur or self.choice_moteur.currentText().upper()
        default = os.getenv("MOTEURRECHERCHE", "GOOGLE").upper()

        choix = moteur if moteur != default else default

        use_tab = self.tab.currentWidget()
        if not use_tab or not hasattr(use_tab, "web_view"):
            self.new_tab()
            use_tab = self.tab.currentWidget()

        url = research(self, query, choix)
        if url:
            use_tab.web_view.load(url[0])
            if query:
                self.url_search.setText(url[0].toString())
            else:
                self.url_search.setText(url[0].toString().split("?q=")[0])

    # Recherche via la barre d'adresse
    def search(self):
        self.base_page(self.url_search.text(), self.choice_moteur.currentText().upper())

    # Page d'accueil par defaut par rapport au moteur par default
    def go_home(self):
        moteur = os.getenv("MOTEURRECHERCHE", "GOOGLE").upper()
        self.base_page("", moteur)

    # Fermer un onglet
    def close_tab(self, index):
        tab = self.tab.widget(index)
        close_tab_window(self.tab, index, tab)

    # Tout fermer proprement
    def closeEvent(self, event):
        while self.tab.count() > 0:
            self.close_tab(0)
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = Principal()
    main_window.show()
    sys.exit(app.exec())

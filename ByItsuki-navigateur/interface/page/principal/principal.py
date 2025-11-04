import os
import sys
from pathlib import Path
if getattr(sys, "frozen", False):
    project_root = Path(sys.executable).parent
else:
    project_root = Path(__file__).resolve().parents[3]

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
from PySide6.QtWebEngineCore import QWebEngineProfile
from PySide6.QtWidgets import QWidget, QApplication, QHBoxLayout, QVBoxLayout, QSizePolicy, QTabWidget
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QIcon
from PySide6.QtWebEngineWidgets import QWebEngineView
from interface.page.base_page import BasePage
from utils import create_profile, CreateElements

class Principal(BasePage):
    def __init__(self, profile=None):
        super().__init__()
        self._profile = profile
        self._creator = None
        self.home_tab_initialized = False
        self.init_interface()

    # ------------------ Récupération du profil ------------------
    @property
    def profile(self):
        if self._profile is None:
            self._profile = self.recovery_profile()
        return self._profile
    def recovery_profile(self, profile=None):
        if profile is not None:
            return profile
        base_path = Path(os.getenv("LOCALAPPDATA")) / "ByItsuki-Navigateur" / "configuration" / "data_navigation"
        if base_path.exists() and any(base_path.iterdir()):
            profile = QWebEngineProfile("ByItsukiProfile")
            profile.setCachePath(str(base_path / "cache"))
            profile.setPersistentStoragePath(str(base_path / "storage"))
            profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies)
        else:
            profile = create_profile(name="ByItsukiProfile")
        return profile

    # -------- Création des éléments en lazy --------
    @property
    def creator(self):
        if self._creator is None:
            from utils import CreateElements  # import local si nécessaire
            self._creator = CreateElements(self, self.profile)
        return self._creator

    # ------------------ Interface ------------------
    def init_interface(self):
        from utils import root_icon
        from PySide6.QtCore import QSize

        self.content_navigation = QVBoxLayout()
        self.content_layout.addLayout(self.content_navigation)

        # ---- Barre d'adresse ----
        address_layout = QHBoxLayout()
        self.button_back = self.creator.create_button("←", self.back, min_width=40, max_height=40)
        self.button_forward = self.creator.create_button("→", self.forward, min_width=40, max_height=40)
        self.reload_button = self.creator.create_button("⟳", self.reload, min_width=40, max_height=40)
        self.start = self.creator.create_button("🏠", self.go_home, min_width=40, max_height=40)
        self.choice_moteur = self.creator.create_select(
            ["Google", "Bing", "DuckDuckGo", "Qwant"], 0, min_width=50, max_width=100
        )
        self.url_search = self.creator.create_input("Barre de recherche...", self.search, min_width=500, max_height=40)
        self.drop_button = self.creator.drop_button(self.url_search)
        self.search_button = self.creator.create_button("🔍", self.search, min_width=40, max_height=40)
        self.open_button = self.creator.create_button("+", self.new_tab, min_width=40, max_height=40)
        self.parameter_menu_button = self.creator.create_button("", self.menu_parametre, min_width=40, max_height=40)

        # Icônes
        icon_file = root_icon("drop_icon.png")
        self.drop_button.setIcon(QIcon(str(icon_file)))
        self.drop_button.setIconSize(QSize(35, 35))
        icon_file = root_icon("menu_icon.png")
        self.parameter_menu_button.setIcon(QIcon(str(icon_file)))
        self.parameter_menu_button.setIconSize(QSize(35, 35))

        for widget in [
            self.button_back, self.button_forward, self.reload_button, self.start,
            self.choice_moteur, self.drop_button, self.url_search,
            self.search_button, self.open_button, self.parameter_menu_button
        ]:
            address_layout.addWidget(widget)
        self.content_layout.addLayout(address_layout)

        # ---- Barre de favoris ----
        self.fav_content = QHBoxLayout()
        self.fav_content.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.favorite_bar = self.creator.fav_bar(parent=self, slot=self.open_favorite, min_height=40, max_height=40)
        self.favorite_bar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.fav_content.addWidget(self.favorite_bar)
        self.content_layout.addLayout(self.fav_content)

        # ---- Onglets ----
        self.onglet_layout = QHBoxLayout()
        self.tab = QTabWidget(self)
        self.tab.setTabsClosable(True)
        self.tab.tabCloseRequested.connect(self.close_tab)
        self.tab.currentChanged.connect(self.on_tab_changed)
        self.onglet_layout.addWidget(self.tab)
        self.content_layout.addLayout(self.onglet_layout)

        # Onglet initial vide pour lazy load
        self.home_tab = QWidget()
        self.tab.addTab(self.home_tab, "Accueil")
        self.tab.setCurrentWidget(self.home_tab)

    # ------------------ Lazy load des onglets ------------------
    def on_tab_changed(self, index):
        tab = self.tab.widget(index)
        if tab == self.home_tab and not self.home_tab_initialized:
            # Création réelle de l'onglet Accueil
            new_tab = self.creator.create_tab(self, self.profile, title="Accueil")
            self.tab.removeTab(index)
            self.tab.insertTab(index, new_tab, "Accueil")
            self.tab.setCurrentIndex(index)
            self.home_tab = new_tab
            self.home_tab_initialized = True
        elif hasattr(tab, "lazy_init") and tab.lazy_init:
            # Nouvel onglet créé à la volée
            new_tab = self.creator.create_tab(self, self.profile, title="Nouvel onglet")
            self.tab.removeTab(index)
            self.tab.insertTab(index, new_tab, "Nouvel onglet")
            self.tab.setCurrentIndex(index)

    # ------------------ Navigation ------------------
    def back(self):
        tab = self.tab.currentWidget()
        if hasattr(tab, "history_manager"):
            tab.history_manager.back()

    def forward(self):
        tab = self.tab.currentWidget()
        if hasattr(tab, "history_manager"):
            tab.history_manager.forward()

    def reload(self):
        tab = self.tab.currentWidget()
        if hasattr(tab, "web_view"):
            tab.web_view.reload()

    def go_home(self):
        self.search(os.getenv("MOTEURRECHERCHE", "GOOGLE").upper())

    def search(self, moteur=None):
        moteur = moteur or self.choice_moteur.currentText().upper()
        tab = self.tab.currentWidget()
        if not hasattr(tab, "web_view"):
            self.new_tab()
            tab = self.tab.currentWidget()
        if hasattr(tab, "history_manager"):
            tab.history_manager.research(moteur)

    def new_tab(self):
        tab = QWidget()
        tab.lazy_init = True
        index = self.tab.addTab(tab, "Nouvel onglet")
        self.tab.setCurrentIndex(index)

    def close_tab(self, index):
        tab = self.tab.widget(index)
        from interface.code import close_tab_window
        close_tab_window(self.tab, index, tab)

    def menu_parametre(self):
        from interface.page.parametre.menu_parametre import Menu_parametre
        self.param_menu = Menu_parametre(profile=None)
        self.param_menu.show()

    def open_favorite(self, url):
        tab = self.tab.currentWidget()
        if hasattr(tab, "web_view"):
            tab.web_view.load(QUrl(url))


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    from interface.page.principal.principal import Principal

    app = QApplication(sys.argv)
    main_window = Principal(profile=None)
    main_window.show()

    sys.exit(app.exec())

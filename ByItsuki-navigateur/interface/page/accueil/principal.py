import os
import sys
from pathlib import Path

# --- Gestion des chemins ---
project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))
icon_root = project_root / "interface" / "img" / "asset" / "icons"

# --- Imports PyQt ---
from PyQt6.QtWidgets import QHBoxLayout, QScrollArea, QVBoxLayout, QWidget, QLabel, QFrame, QApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize, QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile

# --- Imports projet ---
from interface.page.base_page import BasePage
from interface.page.parametre.menu_parametre import Menu_parametre
from interface.code.recherche.recherche import research
from interface.responsive import create_button, create_input
from utils.silence_log_js import SilentWebEnginePage


class Principal(BasePage):
    def __init__(self):
        super().__init__()
        self.init_ui()

        self.web_view = QWebEngineView()
        self.web_view.setMinimumHeight(400)
        self.content_layout.addWidget(self.web_view)

        self.profile = QWebEngineProfile("custom_profile", self)
        self.profile.setHttpUserAgent(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/118.0.5993.118 Safari/537.36"
            "ByItsuki-Navigateur/1.0 (Windows NT 10.0; Win64; x64)"
        )

        # --- Page silencieuse pour éviter les logs JS dans la console uniquement ---
        self.page = SilentWebEnginePage(self.profile, self)
        self.web_view.setPage(self.page)

    def init_ui(self):
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.content_layout.addLayout(button_layout)

        self.research_input = create_input("Rechercher...","Rechercher" ,100,300,40,40)
        button_layout.addWidget(self.research_input)

        # --- Bouton recherche 🔍 ---
        search_button = create_button("🔍", self.search, 40, 40, 40, 40, "Lancer la recherche")
        button_layout.addWidget(search_button)

        open_button = create_button("+", self.open_new_window, 40, 40, 40, 40, "Nouvelle fenêtre")
        button_layout.addWidget(open_button)

        parameter_menu_button = create_button(
            "", self.open_parameter_menu, 40, 40, 40, 40, "Paramètres"
        )
        parameter_menu_button.setIcon(QIcon(str(icon_root / "menu_logo.png")))  # str obligatoire sinon fonctionne pas
        parameter_menu_button.setIconSize(QSize(24, 24))
        button_layout.addWidget(parameter_menu_button)

    def open_parameter_menu(self):
        self.param_menu = Menu_parametre()
        self.param_menu.show()

    def open_new_window(self):
        print("Nouvelle fenêtre ouverte")

    def search(self):
        query = self.research_input.text().strip()
        url = research(self, query)
        self.web_view.load(url[0])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = Principal()
    main_window.show()
    sys.exit(app.exec())

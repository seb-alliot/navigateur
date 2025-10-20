import sys
from pathlib import Path
# Importation des variables d'environnement
from dotenv import load_dotenv
load_dotenv(dotenv_path=".config")
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QTimer, QSize
# Gestion du chemin
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

icon_path = project_root / "interface" / "img" / "asset" / "icons"

from interface.responsive import create_button, create_input
from interface.page.parametre.menu_parametre import Menu_parametre




class Principal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{os.getenv('APP_NAME')} - {os.getenv('VERSION')}")
        self.resize(600, 400)
        self.setFocus()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.init_ui()
    def init_ui(self):
        title = QLabel(f"Bienvenue sur le {os.getenv('APP_NAME')}")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.layout.addWidget(title)


        button_layout = QHBoxLayout()
        self.layout.addLayout(button_layout)

        # Champ de recherche
        research_input = create_input("Rechercher...", 300, 30)
        button_layout.addWidget(research_input)
        # ouverture nouvelle fenêtre
        open_button = create_button("+", self.open_new_window)
        button_layout.addWidget(open_button)

        # Bouton menu paramètres
        parameter_menu_button = create_button("", self.open_parameter_menu, min_width=40, max_width=40, min_height=40, max_height=40, tool_tip="Ouvrir le menu des paramètres")
        parameter_menu_button.setIcon(QIcon(str(icon_path / "menu_logo.png")))
        parameter_menu_button.setIconSize(QSize(24, 24))
        button_layout.addWidget(parameter_menu_button)

    def open_parameter_menu(self):
        self.param_menu = Menu_parametre()
        self.param_menu.show()

    def open_new_window(self):
        print("Nouvelle fenêtre ouverte")


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = Principal()
    window.show()
    sys.exit(app.exec())
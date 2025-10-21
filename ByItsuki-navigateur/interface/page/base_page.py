# interface/page/base_page.py
import sys
from pathlib import Path
from dotenv import load_dotenv
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize
import os

# Chargement des variables d’environnement
load_dotenv(dotenv_path=".config")

# Gestion du chemin projet
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

icon_path = project_root / "interface" / "img" / "asset" / "icons"

from interface.responsive import create_button, create_input


class BasePage(QWidget):
    """Page de base étendue par toutes les autres fenêtres."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{os.getenv('APP_NAME')}")
        self.resize(1024, 768)



        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.header_layout = QHBoxLayout()
        self.layout.addLayout(self.header_layout)

        # Contenu principal (à remplir par les classes filles)
        self.content_layout = QVBoxLayout()
        self.layout.addLayout(self.content_layout)

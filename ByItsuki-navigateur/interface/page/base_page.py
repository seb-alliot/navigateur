import sys
from pathlib import Path
from dotenv import load_dotenv
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt
import os

# Gestion du chemin projet
if getattr(sys, 'frozen', False):
    base_path = Path(sys._MEIPASS)
else:
    base_path = Path(__file__).resolve().parent.parent.parent.parent

# Chemin vers le fichier de configuration
config_path = base_path / "configuration" / ".config"

# Chargement des variables d'environnement
load_dotenv(dotenv_path=config_path)



class BasePage(QWidget):
    """Page de base étendue par toutes les autres fenêtres."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{os.getenv('APP_NAME', 'ByItsuki-Navigateur')}")
        self.resize(1024, 768)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.header_layout = QHBoxLayout()
        self.layout.addLayout(self.header_layout)

        # Contenu principal (à remplir par les classes filles)
        self.content_layout = QVBoxLayout()
        self.layout.addLayout(self.content_layout)

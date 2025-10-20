import sys
from pathlib import Path
# Importation des variables d'environnement
from dotenv import load_dotenv
load_dotenv(dotenv_path=".config/.env")
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
)
from PyQt6.QtCore import Qt, QTimer
# Gestion du chemin
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))


class Recherche(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{os.getenv('APP_NAME')} - Recherche")
        self.resize(600, 400)
        self.setFocus()
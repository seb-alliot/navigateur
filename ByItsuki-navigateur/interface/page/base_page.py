import sys
from pathlib import Path
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt
import os



class BasePage(QWidget):
    """Page de base étendue par toutes les autres fenêtres."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{os.getenv('APP_NAME', 'ByItsuki-Navigateur')}")
        self.resize(1024, 768)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Contenu principal (à remplir par les classes filles)
        self.content_layout = QVBoxLayout()
        self.layout.addLayout(self.content_layout)

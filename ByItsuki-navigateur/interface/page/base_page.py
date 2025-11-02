import sys
from pathlib import Path
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt
import os



class BasePage(QWidget):
    """Page de base étendue par toutes les autres fenêtres."""

    def __init__(self):
        super().__init__()
        self.resize(1024, 768)

        # Layout principal
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # Contenu principal (à remplir par les classes filles)
        self.content_layout = QVBoxLayout()
        self.content_layout.setSpacing(0)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addLayout(self.content_layout)

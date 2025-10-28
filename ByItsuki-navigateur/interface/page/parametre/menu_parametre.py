
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QVBoxLayout
)


from PySide6.QtCore import Qt
from utils import CreateElements


class Menu_parametre(QWidget):
    def __init__(self, profile=None):
        super().__init__()
        self.setWindowTitle("Paramètres")
        self.resize(600, 400)
        self.setFocus()

        button_layout = QVBoxLayout()
        self.setLayout(button_layout)

        self.creator = CreateElements(self, profile)
        settings_button = self.creator.create_button("Paramètres", self.open_settings)
        button_layout.addWidget(settings_button)

        help_button = self.creator.create_button("Aide", self.open_help)
        button_layout.addWidget(help_button)

    def open_settings(self):
        print("Paramètres ouverts")
    def open_help(self):
        print("Aide ouverte")

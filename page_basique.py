import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt

class PageAccueil(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Page d'accueil")
        self.resize(600, 400)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        titre = QLabel("Bienvenue sur la page d'accueil")
        titre.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(titre)

        bouton = QPushButton("Aller ailleurs")
        layout.addWidget(bouton)

        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PageAccueil()
    window.show()
    sys.exit(app.exec())

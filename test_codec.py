import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtWebEngineWidgets import QWebEngineView

# Page HTML de test avec H.264 / AAC
html_test = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Test H.264 / AAC</title>
</head>
<body>
    <h2>Test lecture vidéo H.264 / AAC</h2>
    <video controls width="640">
        <source src="https://www.w3schools.com/html/mov_bbb.mp4" type="video/mp4">
        Votre navigateur ne supporte pas la vidéo.
    </video>
</body>
</html>
"""

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test QWebEngine H.264 / AAC")
        self.resize(800, 600)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)

        # Charger la page de test
        self.web_view.setHtml(html_test)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

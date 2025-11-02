from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QMessageBox
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt, QSize
from io import BytesIO
import requests

import json
from urllib.parse import urlparse

class FavBar(QWidget):
    def __init__(self, parent=None, slot=None, icon=None, title=None, min_height=40, max_height=40, tool_tip=""):
        super().__init__(parent)
        self.setAcceptDrops(True)

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.setLayout(self.layout)

        self.setMinimumHeight(min_height)
        self.setMaximumHeight(max_height)

        self.icon = icon
        self.title = title
        self.slot = slot

        self.setStyleSheet(
            "QPushButton { background: #1f1f1f; color: white; border: none; margin: 0; padding: 0 6px; }"
            "QPushButton:hover { background-color: white; color: black; }"
        )

        self.hide()
        self.load_favorites()

    # --- Drag & Drop ---
    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        url = event.mimeData().text()
        from utils import site_name
        title = site_name(url)
        favicon_url = self.favicon_url(url)
        icon = self.icon_url(favicon_url) if favicon_url else None

        self.add_favorite(url, title, icon)
        self.update_favorites()
        event.acceptProposedAction()

    # --- Extraction favicon ---
    @staticmethod
    def favicon_url(url: str) -> str:
        try:
            parsed = urlparse(url)
            base = f"{parsed.scheme}://{parsed.netloc}"
            return f"{base}/favicon.ico"
        except Exception:
            return None

    # --- Ajout favori ---
    def add_favorite(self, url, title, icon=None):
        from utils import site_name
        display_text = title[:25] if title else url[:25]
        button = QPushButton(display_text)
        button.setMinimumHeight(40)
        button.setMaximumHeight(40)
        button.setMinimumWidth(100)
        button.setMaximumWidth(150)
        button.setToolTip(url)

        button.title = title or site_name(url)

        if icon:
            button.setIcon(icon)
            button.setIconSize(QSize(15, 15))

        if self.slot:
            button.clicked.connect(lambda _, u=url: self.slot(u))

        button.setContextMenuPolicy(Qt.CustomContextMenu)
        button.customContextMenuRequested.connect(lambda pos, b=button: self.remove_favorite(b))

        self.layout.addWidget(button)
        self.show()

    # --- Chargement depuis JSON ---
    def load_favorites(self):
        from utils import root_history
        favoris_path = root_history() / "favoris-bar" / "favoris.json"
        if not favoris_path.exists():
            return
        try:
            with open(favoris_path, "r", encoding="utf-8") as f:
                favoris = json.load(f)
        except json.JSONDecodeError:
            print("[FavBar] JSON mal formé, ignoré.")
            return

        for fav in favoris:
            url = fav.get("url", "")
            title = fav.get("title", "")
            icon_url = fav.get("icon", "")
            icon = self.icon_url(icon_url) if icon_url else None
            if url:
                self.add_favorite(url, title, icon)

        if self.layout.count() > 0:
            self.show()

    # --- Suppression ---
    def remove_favorite(self, button):
        request = QMessageBox.question(
            self,
            "Supprimer le favori",
            f"Supprimer {button.title} ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if request == QMessageBox.StandardButton.Yes:
            self.layout.removeWidget(button)
            button.deleteLater()
            self.update_favorites()
            if self.layout.count() == 0:
                self.hide()

    # --- Mise à jour JSON ---
    def update_favorites(self):
        from utils import root_history
        favoris_path = root_history() / "favoris-bar" / "favoris.json"
        favoris = []
        for i in range(self.layout.count()):
            item = self.layout.itemAt(i)
            widget = item.widget()
            if isinstance(widget, QPushButton):
                url = widget.toolTip()
                parsed = urlparse(url)
                icon_url = f"{parsed.scheme}://{parsed.netloc}/favicon.ico"
                favoris.append({
                    "url": url,
                    "title": widget.title,
                    "icon": icon_url
                })
        favoris_path.parent.mkdir(exist_ok=True)
        with open(favoris_path, "w", encoding="utf-8") as f:
            json.dump(favoris, f, ensure_ascii=False, indent=2)

    # --- Téléchargement icône ---
    @staticmethod
    def icon_url(url):
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                pixmap = QPixmap()
                if pixmap.loadFromData(response.content):
                    return QIcon(pixmap)
        except Exception:
            pass
        return None

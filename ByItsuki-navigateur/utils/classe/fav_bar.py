from PySide6.QtWidgets import QWidget

class FavBar(QWidget):
    def __init__(self, parent=None, slot=None, icon=None, title=None, min_height=40, max_height=40, tool_tip=""):
        from PySide6.QtWidgets import QHBoxLayout, QPushButton
        from PySide6.QtCore import Qt, QSize

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

    @staticmethod
    def favicon_url(url: str) -> str:
        from urllib.parse import urlparse
        try:
            parsed = urlparse(url)
            base = f"{parsed.scheme}://{parsed.netloc}"
            return f"{base}/favicon.ico"
        except Exception:
            return None

    def add_favorite(self, url, title, icon=None):
        from PySide6.QtWidgets import QPushButton
        from PySide6.QtCore import QSize
        from utils import site_name
        from PySide6.QtGui import Qt

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

    def load_favorites(self):
        import json
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

    def remove_favorite(self, button):
        from PySide6.QtWidgets import QMessageBox
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

    def update_favorites(self):
        import json
        from urllib.parse import urlparse
        from utils import root_history

        favoris_path = root_history() / "favoris-bar" / "favoris.json"
        favoris = []
        for i in range(self.layout.count()):
            item = self.layout.itemAt(i)
            widget = item.widget()
            if hasattr(widget, "toolTip"):
                url = widget.toolTip()
                parsed = urlparse(url)
                icon_url = f"{parsed.scheme}://{parsed.netloc}/favicon.ico"
                favoris.append({
                    "url": url,
                    "title": getattr(widget, "title", ""),
                    "icon": icon_url
                })
        favoris_path.parent.mkdir(exist_ok=True)
        with open(favoris_path, "w", encoding="utf-8") as f:
            json.dump(favoris, f, ensure_ascii=False, indent=2)

    @staticmethod
    def icon_url(url):
        import requests
        from PySide6.QtGui import QPixmap, QIcon
        from io import BytesIO

        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                pixmap = QPixmap()
                if pixmap.loadFromData(response.content):
                    return QIcon(pixmap)
        except Exception:
            pass
        return None

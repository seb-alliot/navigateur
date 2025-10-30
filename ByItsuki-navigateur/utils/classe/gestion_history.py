import json
from datetime import datetime
# from interface.code import navigation
from PySide6.QtCore import QUrl

class GestionHistory:
    def __init__(self, tab_widget, url_search, history_file):
        self.tab_widget = tab_widget
        self.url_search = url_search
        self.history_file = history_file

        # Charger l'historique existant ou initialiser
        self.load_history()

    # -------------------------
    def load_history(self):
        if self.history_file.exists():
            with open(self.history_file, "r", encoding="utf-8") as f:
                self.history_data = json.load(f)
        else:
            self.history_data = []

        if not self.history_data:
            self.history_data = [{
                "timestamp": datetime.now().isoformat(),
                "url": "https://www.google.com/",
                "title": "Accueil"
            }]

        self.current_pos = len(self.history_data) - 1

    # -------------------------
    def persist(self):
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(self.history_data, f, ensure_ascii=False, indent=2)

    # -------------------------
    def add_entry(self, url, title=None):
        self.history_data = self.history_data[:self.current_pos + 1]
        entry = {
            "timestamp": datetime.now().isoformat(),
            "url": url,
            "title": title or "Page sans titre"
        }

        self.history_data.append(entry)
        self.current_pos = len(self.history_data) - 1
        self.persist()

    # -------------------------
    def back(self):
        if self.current_pos > 0:
            self.current_pos -= 1
            entry = self.history_data[self.current_pos]
            self.load_url(entry["url"])

    # -------------------------
    def forward(self):
        if self.current_pos < len(self.history_data) - 1:
            self.current_pos += 1
            entry = self.history_data[self.current_pos]
            self.load_url(entry["url"])

    # -------------------------
    def load_url(self, url):
        self.tab_widget.web_view.load(url if isinstance(url, str) else url)
        if self.url_search:
            self.url_search.setText(url if isinstance(url, str) else url.toString())
            self.tab_widget.web_view.load(QUrl(url))

    # # -------------------------
    # def navigate(self):
    #     """Navigation vers l'URL actuelle (utilise la fonction navigation externe)."""
    #     navigation(
    #         self.tab_widget,
    #         self.url_search,
    #         self.current_pos,
    #         self.history_file
    #     )

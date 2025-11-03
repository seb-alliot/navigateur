class GestionNavigation:
    def __init__(self, tab_widget, url_search, history_file):
        self.tab_widget = tab_widget
        self.url_search = url_search
        self.history_file = history_file

        # Charger l'historique existant ou initialiser
        self.load_history()

    # -------------------------
    def load_history(self):
        import json, os
        from datetime import datetime

        if self.history_file.exists():
            with open(self.history_file, "r", encoding="utf-8") as f:
                self.history_data = json.load(f)
        else:
            self.history_data = []

        if not self.history_data:
            self.history_data = [{
                "moteur": os.getenv("MOTEURRECHERCHE"),
                "timestamp": datetime.now().isoformat(),
                "url": "https://www.google.com/",
                "title": "Accueil"
            }]

        self.current_pos = len(self.history_data) - 1

    # -------------------------
    def persist(self):
        import json, os
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(self.history_data, f, ensure_ascii=False, indent=2)

    # -------------------------
    def add_entry(self, url, moteur, title):
        from datetime import datetime
        self.history_data = self.history_data[:self.current_pos + 1]
        entry = {
            "moteur": moteur,
            "timestamp": datetime.now().isoformat(),
            "url": url,
            "title": title
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
        from PySide6.QtCore import QUrl
        qurl = url if isinstance(url, QUrl) else QUrl(url)
        self.tab_widget.web_view.load(qurl)
        if self.url_search:
            self.url_search.setText(qurl.toString())

    # -------------------------
    def research(self, choix):
        import os
        from PySide6.QtCore import QUrl
        from urllib.parse import quote_plus

        choix = os.getenv(choix)
        query = self.url_search.text().strip()
        if query:
            encode_query = quote_plus(query)
            self.url_search.clear()
            url = QUrl(f"{choix}{encode_query}")
            self.load_url(url)
        else:
            url = QUrl(choix)
            self.load_url(url)

from PySide6.QtCore import QUrl
import json
from utils import root_history
from ..navigation import navigation  # attention aux imports relatifs

class TabHistory:
    def __init__(self, tab_index, current_pos):
        self.root_history = root_history()
        self.tab_index = tab_index
        self.current_position = current_pos
        self.history_data = []
        self.history_folder = self.root_history / f"tab_{self.tab_index}"
        self.history_file = self.history_folder / "history.json"


    def navigate(self, tab, url_search, current_pos):
        navigation(tab, url_search, current_pos)

    def persist(self):
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(self.history_data, f, ensure_ascii=False, indent=4)

    def add_entry(self, url):
        # Supprimer tout l'historique après la position actuelle
        self.history_data = self.history_data[:self.current_position + 1]

        # Ajouter la nouvelle URL
        self.history_data.append({"url": url})
        self.current_position = len(self.history_data) - 1
        self.persist()

    def load_history(tab):
        if not tab or not hasattr(tab, "history_file"):
            return
        if tab.history_file.exists():
            with open(tab.history_file, "r", encoding="utf-8") as f:
                history_data = json.load(f)
        else:
            history_data = []

        return history_data

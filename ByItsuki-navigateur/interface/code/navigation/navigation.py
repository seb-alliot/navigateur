from PySide6.QtCore import QUrl
import json

def navigation(tab, url_search, current_pos):

        if not tab or not hasattr(tab, "history_file"):
                return
        history_file = tab.history_file
        with open(history_file, "r", encoding="utf-8") as f:
                history_data = json.load(f)
        if current_pos < 0 or current_pos >= len(history_data):
                return
        tab.current_pos = current_pos
        entry = history_data[tab.current_pos]

        tab.web_view.load(QUrl(entry["url"]))
        url_search.setText(entry["url"])

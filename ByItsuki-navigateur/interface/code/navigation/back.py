from PySide6.QtCore import QUrl
import json

def go_back(tab, history_file, url_search, current_pos):
        with open(history_file, "r", encoding="utf-8") as f:
            history_data = json.load(f)

        current_pos = current_pos
        tab.current_pos -= 1
        entry = history_data[tab.current_pos]

        tab_url = tab.web_view.load(QUrl(entry["url"]))
        url_search = url_search.setText(entry["url"])


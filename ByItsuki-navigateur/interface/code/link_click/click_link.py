import json
from datetime import datetime


def click_link(url, tab_index, web_view_title , moteur, history_general, current_pos):
        # Chargement de l’historique d’onglet
        from utils.root_file.root_history import root_history
        history_file = root_history() / f"tab_{tab_index}" / "history.json"
        if history_file.exists():
            with open(history_file, "r", encoding="utf-8") as f:
                history_tab = json.load(f)
        else:
            history_tab = []
        from utils import site_name
        web_view_title = site_name(web_view_title, moteur)
        entry = {
            "moteur": moteur,
            "timestamp": datetime.now().isoformat(),
            "url": url,
            "title": web_view_title,
        }

        # # Empêche l’ajout de doublons successifs
        if moteur == history_tab[-1]["moteur"] and url == history_tab[-1]["url"]:
            return

        if current_pos == len(history_tab) - 1:
            history_tab.append(entry)
        else:
            history_tab = history_tab[:current_pos + 1]
            history_tab.append(entry)

        with open(history_file, "w", encoding="utf-8") as f:
            json.dump(history_tab, f, ensure_ascii=False, indent=2)

        current_pos = len(history_tab) - 1

        # Historique général
        history_general_file = history_general / "history_general.json"
        if history_general_file.exists():
            with open(history_general_file, "r", encoding="utf-8") as f:
                general_history = json.load(f)
        else:
            general_history = []

        general_history.append(entry)
        with open(history_general_file, "w", encoding="utf-8") as f:
            json.dump(general_history, f, ensure_ascii=False, indent=2)
        data = {
            "moteur": moteur,
            "current_pos": current_pos,
            "history_tab": history_tab,
            "url": entry["url"],
            "title": entry["title"],
        }
        return data
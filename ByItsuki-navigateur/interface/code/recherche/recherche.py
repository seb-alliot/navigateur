from PySide6.QtCore import QUrl
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Gestion du chemin projet
if getattr(sys, 'frozen', False):
    base_path = Path(sys._MEIPASS)
else:
    base_path = Path(__file__).resolve().parent.parent.parent.parent
    print(base_path)


config_path = base_path / "configuration" / ".config"

load_dotenv(dotenv_path=config_path)

def research(self, query, choix):
    query = query

    moteur = os.getenv(choix)

    if query:
        url = QUrl(f"{moteur}{query}")
    else:
        more = "search?q="
        url = QUrl(moteur.replace(more, ""))

    return [url]
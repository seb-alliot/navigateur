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


# Chemin vers le fichier de configuration
config_path = base_path / "configuration" / ".config"

# Chargement des variables d'environnement
load_dotenv(dotenv_path=config_path)

def research(self, query, choix):
    query = query

    # On récup

    # On récupère l’URL de base du moteur choisi
    moteur = os.getenv(choix)

    # On construit l’URL finale
    if query:
        url = QUrl(f"{moteur}{query}")
    else:
        more = "search?q="
        url = QUrl(moteur.replace(more, ""))

    return [url]

import sys
from pathlib import Path


def resource_path(relative_path):
    """Obtenir le chemin absolu d'une ressource, qu'on soit compilé ou pas."""
    try:
        # PyInstaller crée ce dossier temporaire
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = Path(__file__).resolve().parent.parent.parent.parent

    return Path(base_path) / relative_path

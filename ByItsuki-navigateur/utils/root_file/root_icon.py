import sys
from pathlib import Path


def root_icon(icon_name: str):
    try:
        # PyInstaller crée ce dossier temporaire
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = Path(__file__).resolve().parent.parent.parent
    if str(base_path) not in sys.path:
        sys.path.append(str(base_path))
    icon_name = f"{icon_name}"
    root_icon = base_path / "interface" / "img" / "asset" / "icons" / f"{icon_name}"
    return root_icon

import sys
from pathlib import Path

def root_history():
    try:
        base_path = Path(sys._MEIPASS)
    except AttributeError:
        base_path = Path(__file__).resolve().parent.parent.parent

    if str(base_path) not in sys.path:
        sys.path.append(str(base_path))

    history_root = base_path / "configuration" / "data_navigation" / "storage" / "historique"
    history_root.mkdir(parents=True, exist_ok=True)
    return history_root

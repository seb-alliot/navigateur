import os
import sys
from pathlib import Path
from PyQt6.QtWebEngineCore import QWebEngineProfile

def create_profile(parent=None, name="ByItsukiProfile"):

    # Choix du dossier pour le stockage des données persistantes
    if getattr(sys, "frozen", False):
        base = Path(os.getenv("APPDATA", os.getenv("LOCALAPPDATA", "."))) / "ByItsuki-Navigateur" / "web_profile"
    else:
        base = Path(__file__).resolve().parents[1] / "configuration/data_navigation"

    # Crée le dossier de base s'il n'existe pas
    base.mkdir(parents=True, exist_ok=True)

    # Création du profil
    profile = QWebEngineProfile(name, parent)

    profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.DiskHttpCache)
    profile.setCachePath(str(base / "cache"))
    profile.setPersistentStoragePath(str(base / "storage"))

    try:
        profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies)
    except Exception:
        pass

    profile.setHttpUserAgent(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/118.0.5993.118 Safari/537.36 "
        "ByItsuki-Navigateur/1.0"
    )

    return profile

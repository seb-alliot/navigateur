import os
import sys
from pathlib import Path
from PyQt6.QtWebEngineCore import QWebEngineProfile

# --- Configuration globale du moteur Chromium ---
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = (
    "--ignore-certificate-errors "
    "--disable-logging "
    "--log-level=3"
)

# --- Cache du profil global pour éviter les recréations multiples ---
navigation_profil = None


def create_profile(parent=None, name="ByItsukiProfile"):
    """
    Crée ou renvoie un profil QWebEngineProfile persistant et partagé entre les onglets.
    """

    global navigation_profil
    if navigation_profil is not None:
        return navigation_profil  # ✅ On réutilise le même profil

    # --- Choix du dossier pour le stockage des données ---
    if getattr(sys, "frozen", False):
        base = Path(os.getenv("APPDATA", os.getenv("LOCALAPPDATA", "."))) / "ByItsuki-Navigateur" / "web_profile"
    else:
        base = Path(__file__).resolve().parents[1] / "configuration" / "data_navigation"

    base.mkdir(parents=True, exist_ok=True)

    # --- Création du profil persistant ---
    profile = QWebEngineProfile(name, parent)

    profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.DiskHttpCache)
    profile.setCachePath(str(base / "cache"))
    profile.setPersistentStoragePath(str(base / "storage"))

    try:
        profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies)
    except Exception:
        # Compatibilité selon version de Qt
        profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.AllowPersistentCookies)

    # --- User-Agent personnalisé ---
    profile.setHttpUserAgent(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/118.0.5993.118 Safari/537.36 "
        "ByItsuki-Navigateur/1.0"
    )

    navigation_profil = profile
    return navigation_profil

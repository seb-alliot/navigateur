import os
import sys
from pathlib import Path
from PySide6.QtWebEngineCore import QWebEngineProfile, QWebEngineSettings

os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = (
    "--ignore-gpu-blocklist "
    "--enable-gpu-rasterization "
    "--enable-accelerated-video-decode "
    "--enable-features=MediaFoundationService,UseOzonePlatform "
    "--enable-media-foundation-widevine-cdm"
)


def create_profile(parent=None, name="ByItsukiProfile"):
    # Dossier de stockage
    if getattr(sys, "frozen", False):
        base = Path(os.getenv("LOCALAPPDATA")) / "ByItsuki-Navigateur" / "configuration" / "data_navigation"
    else:
        base = Path(__file__).resolve().parents[1] / "configuration" / "data_navigation"

    base.mkdir(parents=True, exist_ok=True)

    # Création du profil
    profile = QWebEngineProfile(name, parent)
    profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.DiskHttpCache)
    profile.setCachePath(str(base / "cache"))
    profile.setPersistentStoragePath(str(base / "storage"))
    profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies)

    # Paramètres WebEngine
    settings = profile.settings()
    settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
    settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
    settings.setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)
    settings.setAttribute(QWebEngineSettings.WebAttribute.ScrollAnimatorEnabled, True)
    settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
    settings.setAttribute(QWebEngineSettings.WebAttribute.AutoLoadImages, True)
    settings.setAttribute(QWebEngineSettings.WebAttribute.PlaybackRequiresUserGesture, False)
    settings.setAttribute(QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, True)
    settings.setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, True)
    settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)

    # Headers & user-agent
    profile.setHttpAcceptLanguage("fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7")
    profile.setHttpUserAgent(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/129.0.0.0 Safari/537.36 "
        "ByItsuki-Navigateur/1.0"
    )

    return profile

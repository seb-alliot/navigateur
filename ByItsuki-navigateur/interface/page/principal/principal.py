import os
import subprocess
# Détection iGPU Intel sous Windows
# Accelération du demarrage sur ordi avec iGPU Intel

def is_intel_igpu():
    try:
        output = subprocess.check_output("wmic path win32_videocontroller get name", shell=True, text=True)
        return "intel" in output.lower()
    except Exception:
        return False

if is_intel_igpu():
    # Désactive l'igpu et refourgue le taff au cpu
    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu --disable-software-rasterizer"
else:
    pass

import sys
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QApplication, QHBoxLayout, QVBoxLayout, QSizePolicy,
    QTabWidget, QPushButton, QLineEdit, QComboBox
)
if getattr(sys, "frozen", False):
    project_root = Path(sys.executable).parent
else:
    project_root = Path(__file__).resolve().parents[3]

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
from PySide6.QtCore import Qt, QUrl, QObject, Signal, QThread, QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWebEngineCore import QWebEngineProfile
from interface.page.base_page import BasePage
from utils import create_profile

# Import de DropButton nécessaire
from utils import DropButton

# ----------------------------
# Worker pour préparer les dossiers
# ----------------------------
class ProfileFolderPrep(QObject):
    finished = Signal()

    def run(self):
        base_path = Path(os.getenv("LOCALAPPDATA", Path.home())) / "ByItsuki-Navigateur/configuration/data_navigation"
        base_path.mkdir(parents=True, exist_ok=True)
        (base_path / "cache").mkdir(parents=True, exist_ok=True)
        (base_path / "storage").mkdir(parents=True, exist_ok=True)
        self.finished.emit()

# ----------------------------
# Fenêtre principale
# ----------------------------
class Principal(BasePage):
    def __init__(self):
        super().__init__()
        self._profile = None
        self._creator = None
        self.home_tab_initialized = False

        # UI minimale immédiate
        self.init_interface()

        # Préparation des dossiers sur un thread
        self.init_profile()

    # ------------------ Interface minimale ------------------
    def init_interface(self):
        from utils import root_icon
        from PySide6.QtCore import QSize

        self.content_navigation = QVBoxLayout()
        self.content_layout.addLayout(self.content_navigation)

        # ---- Barre d'adresse ----
        address_layout = QHBoxLayout()

        # boutons légers, non interactifs
        self.button_back = QPushButton("←")
        self.button_forward = QPushButton("→")
        self.reload_button = QPushButton("⟳")
        self.start = QPushButton("🏠")
        self.choice_moteur = QComboBox()
        self.choice_moteur.addItems(["Google", "Bing", "DuckDuckGo", "Qwant"])
        self.url_search = QLineEdit("Barre de recherche...")
        self.url_search.setEnabled(False)

        self.drop_button = DropButton(line_edit=self.url_search, parent=self)
        self.drop_button.setText("⋯")
        self.drop_button.setEnabled(False)

        self.search_button = QPushButton("🔍")
        self.search_button.setEnabled(False)
        self.open_button = QPushButton("+")
        self.open_button.setEnabled(False)
        self.parameter_menu_button = QPushButton("")
        self.parameter_menu_button.setEnabled(False)

        # icônes
        try:
            icon_file = root_icon("drop_icon.png")
            # Le DropButton est instancié sans icône pour utiliser le texte,
            # mais on peut forcer l'icône ici si le fichier est prêt.
            self.drop_button.setIcon(QIcon(str(icon_file)))
            self.drop_button.setIconSize(QSize(15, 15))
            self.drop_button.setText("")

            icon_file = root_icon("menu_icon.png")
            self.parameter_menu_button.setIcon(QIcon(str(icon_file)))
            self.parameter_menu_button.setIconSize(QSize(15, 15))
        except Exception:
            pass

        # ajouter widgets au layout
        for w in [
            self.button_back, self.button_forward, self.reload_button, self.start,
            self.choice_moteur, self.drop_button, self.url_search,
            self.search_button, self.open_button, self.parameter_menu_button
        ]:
            address_layout.addWidget(w)
        self.content_layout.addLayout(address_layout)

        # ---- Barre de favoris placeholder ----
        self.fav_content = QHBoxLayout()
        self.fav_content.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.favorite_placeholder = QWidget()
        self.favorite_placeholder.setMinimumHeight(40)
        self.fav_content.addWidget(self.favorite_placeholder)
        self.content_layout.addLayout(self.fav_content)

        # ---- Onglets ----
        self.onglet_layout = QHBoxLayout()
        self.tab = QTabWidget(self)
        self.tab.setTabsClosable(True)
        self.tab.tabCloseRequested.connect(self.close_tab)
        self.tab.currentChanged.connect(self.on_tab_changed)
        self.onglet_layout.addWidget(self.tab)
        self.content_layout.addLayout(self.onglet_layout)

        # Onglet Accueil lazy
        self.home_tab = QWidget()
        self.home_tab.lazy_init = True
        self.tab.addTab(self.home_tab, "Accueil")
        self.tab.setCurrentWidget(self.home_tab)

    # ------------------ Thread dossiers ------------------
    def init_profile(self):
        self._thread = QThread()
        self._worker = ProfileFolderPrep()
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.finished.connect(self.profil_ready)
        self._worker.finished.connect(self._thread.quit)
        self._thread.finished.connect(self._thread.deleteLater)
        self._thread.start()

    # ------------------ Quand le profil est prêt ------------------
    def profil_ready(self):
        # créer ou récupérer le profil complet
        self._profile = create_profile(name="ByItsukiProfile")
        QTimer.singleShot(50, self.init_creator)

    # ------------------ Initialisation _creator et activation UI ------------------
    def init_creator(self):
        from utils import CreateElements
        self._creator = CreateElements(self, self._profile)

        # remplacer l'onglet lazy par onglet réel
        if self.home_tab.lazy_init:
            new_tab = self._creator.create_tab(self, self._profile, title="Accueil")
            self.tab.removeTab(self.tab.indexOf(self.home_tab))
            self.tab.insertTab(0, new_tab, "Accueil")
            self.tab.setCurrentIndex(0)
            self.home_tab = new_tab
            self.home_tab_initialized = True

        # remplacer placeholder barre de favoris
        self.fav_content.removeWidget(self.favorite_placeholder)
        self.favorite_bar = self._creator.fav_bar(parent=self, slot=self.open_favorite, min_height=40, max_height=40)
        self.favorite_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.fav_content.addWidget(self.favorite_bar)
        self.favorite_placeholder.deleteLater()

        self.drop_button.parent = self

        # activer tous les widgets et connecter slots
        for w, slot in [
            (self.button_back, self.back),
            (self.button_forward, self.forward),
            (self.reload_button, self.reload),
            (self.start, self.go_home),
            (self.choice_moteur, None),
            (self.url_search, self.search),
            (self.drop_button, None),
            (self.search_button, self.search),
            (self.open_button, self.new_tab),
            (self.parameter_menu_button, self.menu_parametre)
        ]:
            w.setEnabled(True)
            if slot:
                if hasattr(w, "clicked"):
                    w.clicked.connect(slot)
                elif hasattr(w, "returnPressed"):
                    w.returnPressed.connect(slot)

    # ------------------ Lazy tab changed ------------------
    def on_tab_changed(self, index):
        if not self._creator:
            return
        tab = self.tab.widget(index)
        if hasattr(tab, "lazy_init") and tab.lazy_init:
            new_tab = self._creator.create_tab(self, self._profile, title="Nouvel onglet")
            self.tab.removeTab(index)
            self.tab.insertTab(index, new_tab, "Nouvel onglet")
            self.tab.setCurrentIndex(index)

    # ------------------ Navigation ------------------
    def back(self):
        tab = self.tab.currentWidget()
        if hasattr(tab, "history_manager"):
            tab.history_manager.back()

    def forward(self):
        tab = self.tab.currentWidget()
        if hasattr(tab, "history_manager"):
            tab.history_manager.forward()

    def reload(self):
        tab = self.tab.currentWidget()
        if hasattr(tab, "web_view"):
            tab.web_view.reload()

    def go_home(self):
        self.search(os.getenv("MOTEURRECHERCHE", "GOOGLE").upper())

    def search(self, moteur=None):
        moteur = moteur or self.choice_moteur.currentText().upper()
        tab = self.tab.currentWidget()
        if not hasattr(tab, "web_view"):
            self.new_tab()
            tab = self.tab.currentWidget()
        if hasattr(tab, "history_manager"):
            tab.history_manager.research(moteur)

    def new_tab(self):
        if not self._creator:
            return
        tab = QWidget()
        tab.lazy_init = True
        index = self.tab.addTab(tab, "Nouvel onglet")
        self.tab.setCurrentIndex(index)

    def close_tab(self, index):
        tab = self.tab.widget(index)
        from interface.code import close_tab_window
        close_tab_window(self.tab, index, tab)

    def menu_parametre(self):
        from interface.page.parametre.menu_parametre import Menu_parametre
        self.param_menu = Menu_parametre(profile=None)
        self.param_menu.show()

    def open_favorite(self, url):
        tab = self.tab.currentWidget()
        if hasattr(tab, "web_view"):
            tab.web_view.load(QUrl(url))

    def closeEvent(self, event):
        while self.tab.count() > 0:
            self.close_tab(0)
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = Principal()
    main_window.show()
    sys.exit(app.exec())
from PySide6.QtWidgets import (
    QWidget, QSizePolicy,
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl, QObject, Signal, Slot, Qt
from PySide6.QtWebChannel import QWebChannel


class JSHandler(QObject):
    linkClickedSignal = Signal(str)

    @Slot(str)
    def linkClicked(self, url):
        self.linkClickedSignal.emit(url)


from utils.search_profil.silence_log_js import SilentWebEnginePage
from utils import base_style, root_history
from interface.code import click_link
from utils.classe.gestion_navigation import GestionNavigation


class CreateElements(QWidget):

    def __init__(self, parent, profile, title="Nouvel onglet",
                    min_width=800, max_width=None, min_height=600, max_height=None):
        super().__init__(parent)
        self.parent = parent
        self.profile = profile
        self.title = title

        self.setMinimumSize(min_width, min_height)
        self.setMaximumSize(max_width or 16777215, max_height or 16777215)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    # -----------------------------
    def create_button(self, placeholder, slot, **kwargs):
        from PySide6.QtWidgets import QPushButton

        tool_tip = kwargs.get("tool_tip", "")
        extra_style = kwargs.get("extra_style", "")
        min_width = kwargs.get("min_width", 40)
        max_width = kwargs.get("max_width", 40)
        min_height = kwargs.get("min_height", 40)
        max_height = kwargs.get("max_height", 40)

        button = QPushButton(placeholder)
        button.setMinimumSize(min_width, min_height)
        button.setStyleSheet("QPushButton { border: none; margin: 0px; padding: 0px; }")
        if max_width is None:
            button.setMaximumWidth(16777215)
        if max_height is None:
            button.setMaximumHeight(16777215)
        if extra_style:
            button.setStyleSheet(extra_style)
        if tool_tip:
            button.setToolTip(tool_tip)
        button.clicked.connect(slot)
        return button

    # -----------------------------
    def create_input(self, placeholder, slot=None, **kwargs):
        from PySide6.QtWidgets import QLineEdit

        min_width = kwargs.get("min_width", 200)
        max_width = kwargs.get("max_width", None)
        min_height = kwargs.get("min_height", 30)
        max_height = kwargs.get("max_height", 45)
        tool_tip = kwargs.get("tool_tip", "")
        extra_style = kwargs.get("extra_style", "")

        input_field = QLineEdit()
        input_field.setStyleSheet("QLineEdit { border: none; margin: 0px; padding: 0px; }")
        input_field.setPlaceholderText(placeholder)
        input_field.setMinimumSize(min_width, min_height)
        input_field.setMaximumHeight(max_height)
        input_field.setToolTip(tool_tip)
        if max_width:
            input_field.setMaximumWidth(max_width)
        if extra_style:
            input_field.setStyleSheet(extra_style)
        if slot:
            input_field.returnPressed.connect(slot)
        return input_field

    # -----------------------------
    def create_select(self, options=None, default_index=0, **kwargs):
        from PySide6.QtWidgets import QComboBox

        min_width = kwargs.get("min_width", 200)
        max_width = kwargs.get("max_width", None)
        min_height = kwargs.get("min_height", 30)
        max_height = kwargs.get("max_height", 45)
        tool_tip = kwargs.get("tool_tip", "")

        combo_box = QComboBox()
        combo_box.setStyleSheet("QComboBox { background-color: #1f1f1f; border: none; margin: 0px; padding: 0px; }")
        combo_box.addItems(options or [])
        combo_box.setCurrentIndex(default_index)
        combo_box.setToolTip(tool_tip)

        if min_width:
            combo_box.setMinimumWidth(min_width)
        if max_width:
            combo_box.setMaximumWidth(16777215 if max_width is None else max_width)
        if min_height:
            combo_box.setMinimumHeight(min_height)
        if max_height:
            combo_box.setMaximumHeight(16777215 if max_height is None else max_height)

        return combo_box

    # -----------------------------
    def fav_bar(self, parent, slot=None, icon=None, title=None, **kwargs):
        from utils.classe.fav_bar import FavBar

        min_height = kwargs.get("min_height", 30)
        max_height = kwargs.get("max_height", 45)
        tool_tip = kwargs.get("tool_tip", "")

        return FavBar(parent=parent, slot=slot, icon=icon, title=title,
                      min_height=min_height, max_height=max_height,
                      tool_tip=tool_tip)

    # -----------------------------
    def drop_button(self, line_edit, icon=None):
        from utils.classe.drop_url import DropButton
        drop_button = DropButton(line_edit=line_edit, icon=icon)
        return drop_button

    # -----------------------------
    def create_tab(self, parent, profile, title="Nouvel onglet",
                    min_width=800, max_width=None, min_height=600, max_height=None):
        import os, json
        from datetime import datetime
        from PySide6.QtCore import QUrl

        # --- Initialisation de l’historique ---
        history_root = root_history()
        history_general = history_root / "general"
        history_general.mkdir(parents=True, exist_ok=True)
        tab_index = parent.tab.count() + 1
        tab_folder = history_root / f"tab_{tab_index}"
        tab_folder.mkdir(parents=True, exist_ok=True)
        history_file = tab_folder / "history.json"

        # --- Page d'accueil ---
        moteur = os.getenv("MOTEURRECHERCHE", "GOOGLE").upper()
        moteur_str = os.getenv(moteur, "https://www.google.com/search?q=").split("search?q=")[0]

        accueil_entry = {
            "moteur": moteur,
            "timestamp": datetime.now().isoformat(),
            "url": moteur_str,
            "title": "Accueil",
        }

        with open(history_file, "w", encoding="utf-8") as f:
            json.dump([accueil_entry], f, ensure_ascii=False, indent=2)

        # --- Configuration du widget onglet ---
        tab_widget = QWidget()
        tab_widget.setStyleSheet("QPushButton { border: none; margin: 0px; padding: 0px; }")
        from PySide6.QtWidgets import QVBoxLayout
        layout = QVBoxLayout(tab_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.web_view = QWebEngineView()
        self.web_view.history().clear()
        self.page = SilentWebEnginePage(profile, self.web_view)
        self.web_view.setPage(self.page)
        self.web_view.setHtml(base_style())

        # --- Infos internes ---
        tab_widget.title = title
        tab_widget.profile = profile
        tab_widget.web_view = self.web_view
        tab_widget.history_root = tab_folder
        tab_widget.history_file = history_file

        # --- Navigation personnalisée ---
        tab_widget.history_manager = GestionNavigation(tab_widget, parent.url_search, tab_widget.history_file)
        tab_widget.current_pos = 0
        tab_widget.page = self.page
        tab_widget.tab_index = tab_index

        # --- Injetion JS + WebChannel ---
        self.channel = QWebChannel()
        self.js_handler = JSHandler()
        self.signal = self.js_handler.linkClickedSignal
        self.channel.registerObject("qt_object", self.js_handler)
        self.page.setWebChannel(self.channel)

        # Connecte le signal Python
        self.js_handler.linkClickedSignal.connect(self.on_js_link_clicked)

        # --- Historique des liens ---
        def on_link_clicked(url):
            moteur = parent.choice_moteur.currentText().upper()
            data = click_link(url, tab_index, self.web_view.title(), moteur, history_general, tab_widget.current_pos)
            if data:
                tab_widget.current_pos = data["current_pos"]
                tab_widget.history_tab = data["history_tab"]
                title = data["title"]
                moteur = data["moteur"]
                url = data["url"]
            tab_widget.history_manager.add_entry(url, moteur, title)

        self.page.linkClickedSignal.connect(on_link_clicked)
        self.signal.connect(on_link_clicked)
        tab_widget.on_link_clicked = on_link_clicked

        # --- Icône d’onglet ---
        def update_tab_icon(icon):
            index = parent.tab.indexOf(tab_widget)
            if index >= 0 and not icon.isNull():
                parent.tab.setTabIcon(index, icon)

        def update_url(url):
            if hasattr(parent, "url_search"):
                parent.url_search.setText(url.toString())

        self.web_view.iconChanged.connect(update_tab_icon)
        self.web_view.urlChanged.connect(update_url)

        # --- Charger la page d’accueil ---
        self.web_view.load(QUrl(accueil_entry["url"]))

        layout.addWidget(self.web_view)
        if moteur == "BING":
            self.web_view.loadFinished.connect(self.inject_js_after_load)

        return tab_widget

    # --- JS Injection ---
    def inject_js_after_load(self, ok):
        if not ok:
            return
        self.web_view.page().runJavaScript("""
        var s=document.createElement('script');
        s.src='qrc:///qtwebchannel/qwebchannel.js';
        document.head.appendChild(s);
        """)

        js_code = """
        setTimeout(function(){
            (function(){
                function setup(){
                    if(typeof qt==='undefined'||!qt.webChannelTransport){
                        console.log("WebChannel not ready, retrying...");
                        setTimeout(setup,500);
                        return;
                    }
                    new QWebChannel(qt.webChannelTransport,function(channel){
                        const qt_object=channel.objects.qt_object;
                        function attach(a){
                            a.addEventListener('click',function(e){
                                e.preventDefault();
                                qt_object.linkClicked(this.href);
                            });
                        }
                        document.querySelectorAll('a').forEach(attach);
                        const obs=new MutationObserver(m=>{
                            m.forEach(x=>{
                                x.addedNodes.forEach(n=>{
                                    if(n.tagName==='A')attach(n);
                                    else if(n.querySelectorAll)
                                        n.querySelectorAll('a').forEach(attach);
                                });
                            });
                        });
                        obs.observe(document.body,{childList:true,subtree:true});
                        console.log("qt_object connected and listeners active");
                    });
                }
                setup();
            })();
        },800);
        """
        self.web_view.page().runJavaScript(js_code)

    # --- Réception JS ---
    def on_js_link_clicked(self, url):
        if url.startswith("http"):
            self.web_view.setUrl(QUrl(url))

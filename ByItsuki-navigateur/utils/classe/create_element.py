from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl, QObject, Signal, Slot, Qt
from PySide6.QtWebChannel import QWebChannel

from utils.search_profil.silence_log_js import SilentWebEnginePage
from utils import base_style, root_history
from interface.code import click_link
from utils.classe.gestion_navigation import GestionNavigation


class JSHandler(QObject):
    linkClickedSignal = Signal(str)

    @Slot(str)
    def linkClicked(self, url):
        self.linkClickedSignal.emit(url)


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

        # tailles uniformisées
        self.ui_min_height = 40
        self.ui_max_height = 40
        self.ui_min_width = 40
        self.ui_max_width = 200

    # -----------------------------
    def create_button(self, placeholder, slot, **kwargs):
        from PySide6.QtWidgets import QPushButton

        tool_tip = kwargs.get("tool_tip", "")
        extra_style = kwargs.get("extra_style", "")

        button = QPushButton(placeholder)
        button.setMinimumSize(self.ui_min_width, self.ui_min_height)
        button.setMaximumSize(kwargs.get("max_width", self.ui_max_width),
                              kwargs.get("max_height", self.ui_max_height))
        button.setStyleSheet("QPushButton { border: none; margin: 0px; padding: 0px; }")

        if extra_style:
            button.setStyleSheet(extra_style)
        if tool_tip:
            button.setToolTip(tool_tip)
        button.clicked.connect(slot)
        return button

    # -----------------------------
    def create_input(self, placeholder, slot=None, **kwargs):
        from PySide6.QtWidgets import QLineEdit

        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        input_field.setMinimumHeight(self.ui_min_height)
        input_field.setMaximumHeight(self.ui_max_height)
        input_field.setMinimumWidth(kwargs.get("min_width", 200))
        input_field.setMaximumWidth(kwargs.get("max_width", 400))
        input_field.setStyleSheet("QLineEdit { border: none; margin: 0px; padding: 0px; }")

        tool_tip = kwargs.get("tool_tip", "")
        if tool_tip:
            input_field.setToolTip(tool_tip)

        extra_style = kwargs.get("extra_style", "")
        if extra_style:
            input_field.setStyleSheet(extra_style)

        if slot:
            input_field.returnPressed.connect(slot)
        return input_field

    # -----------------------------
    def create_select(self, options=None, default_index=0, **kwargs):
        from PySide6.QtWidgets import QComboBox

        combo_box = QComboBox()
        combo_box.setStyleSheet(
            "QComboBox { background-color: #1f1f1f; border: none; margin: 0px; padding: 0px; }"
        )
        combo_box.addItems(options or [])
        combo_box.setCurrentIndex(default_index)
        combo_box.setMinimumHeight(self.ui_min_height)
        combo_box.setMaximumHeight(self.ui_max_height)
        combo_box.setMinimumWidth(kwargs.get("min_width", 120))
        combo_box.setMaximumWidth(kwargs.get("max_width", 200))

        tool_tip = kwargs.get("tool_tip", "")
        if tool_tip:
            combo_box.setToolTip(tool_tip)

        return combo_box

    # -----------------------------
    def fav_bar(self, parent, slot=None, icon=None, title=None, **kwargs):
        from utils.classe.fav_bar import FavBar
        return FavBar(
            parent=parent,
            slot=slot,
            icon=icon,
            title=title,
            min_height=self.ui_min_height,
            max_height=self.ui_max_height,
            tool_tip=kwargs.get("tool_tip", "")
        )

    # -----------------------------
    def drop_button(self, line_edit, icon=None, **kwargs):
        from utils.classe.drop_url import DropButton
        drop_button = DropButton(line_edit=line_edit, icon=icon, **kwargs)
        drop_button.setMinimumSize(self.ui_min_width, self.ui_min_height)
        drop_button.setMaximumSize(kwargs.get("max_width", self.ui_max_width),
                                   kwargs.get("max_height", self.ui_max_height))
        return drop_button

    # -----------------------------
    def create_tab(self, parent, profile, title="Nouvel onglet",
               min_width=800, max_width=None, min_height=600, max_height=None):
        import os, json
        from datetime import datetime
        from PySide6.QtCore import QUrl
        from PySide6.QtWidgets import QVBoxLayout

        # --- Gestion de l'historique ---
        history_root = root_history()
        history_general = history_root / "general"
        history_general.mkdir(parents=True, exist_ok=True)
        tab_index = parent.tab.count() + 1
        tab_folder = history_root / f"tab_{tab_index}"
        tab_folder.mkdir(parents=True, exist_ok=True)
        history_file = tab_folder / "history.json"

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

        # --- Création de l'onglet ---
        tab_widget = QWidget()
        layout = QVBoxLayout(tab_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        web_view = QWebEngineView()
        page = SilentWebEnginePage(profile, web_view)
        web_view.setPage(page)
        web_view.setHtml(base_style())

        # --- Attributs de l'onglet ---
        tab_widget.title = title
        tab_widget.profile = profile
        tab_widget.web_view = web_view
        tab_widget.history_root = tab_folder
        tab_widget.history_file = history_file
        tab_widget.history_manager = GestionNavigation(tab_widget, parent.url_search, history_file)
        tab_widget.current_pos = 0
        tab_widget.page = page
        tab_widget.tab_index = tab_index

        # --- WebChannel pour JS ---
        channel = QWebChannel()
        js_handler = JSHandler()
        channel.registerObject("qt_object", js_handler)
        page.setWebChannel(channel)

        def on_link_clicked(url):
            data = click_link(url, tab_index, web_view.title(), moteur, history_general, tab_widget.current_pos)
            if data:
                tab_widget.current_pos = data["current_pos"]
                tab_widget.history_tab = data["history_tab"]
                tab_widget.history_manager.add_entry(data["url"], data["moteur"], data["title"])

        page.linkClickedSignal.connect(on_link_clicked)
        js_handler.linkClickedSignal.connect(on_link_clicked)

        # --- Icône et URL ---
        def update_tab_icon(icon):
            index = parent.tab.indexOf(tab_widget)
            if index >= 0 and not icon.isNull():
                parent.tab.setTabIcon(index, icon)

        def update_url(url):
            if hasattr(parent, "url_search"):
                parent.url_search.setText(url.toString())

        web_view.iconChanged.connect(update_tab_icon)
        web_view.urlChanged.connect(update_url)
        web_view.load(QUrl(accueil_entry["url"]))
        layout.addWidget(web_view)

        # --- Plein écran ---
        def handle_fullscreen(request, view: QWebEngineView):
            if request.toggleOn():
                view.window().showFullScreen()
            else:
                view.window().showNormal()
            request.accept()

        page.fullScreenRequested.connect(lambda request: handle_fullscreen(request, web_view))

        # --- Injection JS pour Bing ---
        if moteur == "BING":
            def inject_js_after_load(ok):
                if not ok:
                    return
                web_view.page().runJavaScript("""
                var s=document.createElement('script');
                s.src='qrc:///qtwebchannel/qwebchannel.js';
                document.head.appendChild(s);
                """)
                js_code = """
                setTimeout(function(){
                    (function(){
                        function setup(){
                            if(typeof qt==='undefined'||!qt.webChannelTransport){
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
                                            if(n.tagName==='A') attach(n);
                                            else if(n.querySelectorAll)
                                                n.querySelectorAll('a').forEach(attach);
                                        });
                                    });
                                });
                                obs.observe(document.body,{childList:true,subtree:true});
                            });
                        }
                        setup();
                    })();
                },800);
                """
                web_view.page().runJavaScript(js_code)

            web_view.loadFinished.connect(inject_js_after_load)

        return tab_widget


    # -----------------------------
    def on_js_link_clicked(self, url):
        if url.startswith("http"):
            self.web_view.setUrl(QUrl(url))

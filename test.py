# test_bing_clicks.py

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtCore import QObject, Signal, Slot, QUrl



# -------------------
# Silent page améliorée pour debug
# -------------------
class DebugWebEnginePage(QWebEnginePage):
    linkClickedSignal = Signal(str)

    def __init__(self, profile=None, parent=None):
        super().__init__(profile, parent)

    # Affiche les messages de console JS pour debug (facultatif)
    def javaScriptConsoleMessage(self, level, message, line, source_id):
        print(f"[JS console][level={level}] {message} (line {line}) source: {source_id}")

    def acceptNavigationRequest(self, url, nav_type, isMainFrame):
        # Affiche le type de navigation reçu (utile pour diagnostiquer Bing)
        try:
            nav_type_name = {
                QWebEnginePage.NavigationTypeLinkClicked: "LinkClicked",
                QWebEnginePage.NavigationTypeFormSubmitted: "FormSubmitted",
                QWebEnginePage.NavigationTypeBackForward: "BackForward",
                QWebEnginePage.NavigationTypeReload: "Reload",
                QWebEnginePage.NavigationTypeFormResubmitted: "FormResubmitted",
                QWebEnginePage.NavigationTypeOther: "Other",
            }.get(nav_type, str(nav_type))
        except Exception:
            nav_type_name = str(nav_type)

        print(f"[acceptNavigationRequest] nav_type={nav_type_name}, isMainFrame={isMainFrame}, url={url.toString()}")

        # Mode diagnostic: si tu veux laisser le moteur gérer (réparer Bing), retourne True
        # Pour tester l'interception, retourne False et le handler côté Python chargera l'URL manuellement.
        # Ici on renvoie True pour que par défaut tout fonctionne ; tu pourras modifier selon test.
        return True

    def createWindow(self, _type):
        # Permet de capter window.open / target=_blank ; renvoie une nouvelle page qui relaie les signals
        new_page = DebugWebEnginePage(self.profile(), None)
        new_page.linkClickedSignal.connect(self.linkClickedSignal.emit)
        return new_page

# -------------------
# Handler JS exposé
# -------------------
class JSHandler(QObject):
    linkClickedSignal = Signal(str)

    @Slot(str)
    def linkClicked(self, url):
        print(f"[JSHandler] linkClicked -> {url}")
        self.linkClickedSignal.emit(url)

# -------------------
# Application principale
# -------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Bing clicks - debug")
        self.resize(1200, 800)

        central = QWidget()
        layout = QVBoxLayout(central)
        self.setCentralWidget(central)

        self.web_view = QWebEngineView()
        self.page = DebugWebEnginePage(None, self.web_view)
        self.web_view.setPage(self.page)
        layout.addWidget(self.web_view)

        # WebChannel + JS handler
        self.channel = QWebChannel()
        self.js_handler = JSHandler()
        self.channel.registerObject("qt_object", self.js_handler)
        self.page.setWebChannel(self.channel)

        # Connect signals
        self.js_handler.linkClickedSignal.connect(self.on_js_link_clicked)

        # Connect page linkClickedSignal if you use acceptNavigationRequest emitting it
        self.page.linkClickedSignal.connect(self.on_page_link_clicked)

        # Inject JS après chargement (capture globale + MutationObserver)
        self.web_view.loadFinished.connect(self.inject_js_after_load)

        # Charge Bing par défaut pour tester
        self.web_view.setUrl(QUrl("https://www.bing.com/search?q=manga+scan"))

    def inject_js_after_load(self, ok):
        if not ok:
            print("[inject_js] loadFinished with ok=False")
            return

        # Étape 1 : injecter la bibliothèque WebChannel
        webchannel_js = """
        var script = document.createElement('script');
        script.src = 'qrc:///qtwebchannel/qwebchannel.js';
        document.head.appendChild(script);
        """
        self.web_view.page().runJavaScript(webchannel_js)

        # Étape 2 : injection du script principal
        js_code = """
        setTimeout(function() {
            (function() {
                function setup() {
                    if (typeof qt === 'undefined' || !qt.webChannelTransport) {
                        console.log("WebChannel not ready, retrying...");
                        setTimeout(setup, 500);
                        return;
                    }

                    new QWebChannel(qt.webChannelTransport, function(channel) {
                        const qt_object = channel.objects.qt_object;

                        function attachLinkListener(a) {
                            a.addEventListener('click', function(e) {
                                e.preventDefault();
                                qt_object.linkClicked(this.href);
                            });
                        }

                        document.querySelectorAll('a').forEach(attachLinkListener);

                        const observer = new MutationObserver(function(mutations) {
                            mutations.forEach(function(mutation) {
                                mutation.addedNodes.forEach(function(node) {
                                    if (node.tagName === 'A') attachLinkListener(node);
                                    else if (node.querySelectorAll) {
                                        node.querySelectorAll('a').forEach(attachLinkListener);
                                    }
                                });
                            });
                        });

                        observer.observe(document.body, { childList: true, subtree: true });
                        console.log("qt_object connected and link listeners active.");
                    });
                }

                setup();
            })();
        }, 800);
        """
        self.web_view.page().runJavaScript(js_code)

        print("[inject_js] script injected")






    # appelé quand le JS envoie un clic via QWebChannel
    def on_js_link_clicked(self, url):
        print(f"[on_js_link_clicked] reçu du JS: {url}")
        # Si tu veux intercepter et charger manuellement (mode interception) :
        # self.web_view.setUrl(QUrl(url))

    # appelé si la page émet son propre signal (depuis createWindow etc.)
    def on_page_link_clicked(self, url):
        print(f"[on_page_link_clicked] page signal -> {url}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())

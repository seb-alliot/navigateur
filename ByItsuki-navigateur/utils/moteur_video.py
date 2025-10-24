from cefpython3 import cefpython as cef
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import QTimer

class CefBrowserWidget(QWidget):
    def __init__(self, parent=None, start_url="https://www.google.com"):
        super().__init__(parent)
        self.start_url = start_url
        self.browser = None

        self.vbox = QVBoxLayout(self)
        self.vbox.setContentsMargins(0, 0, 0, 0)

        self.timer = QTimer()
        self.timer.timeout.connect(self.on_timer)
        self.timer.start(10)

        self.init_cef()

    def init_cef(self):
        window_info = cef.WindowInfo()
        rect = [0, 0, self.width(), self.height()]
        window_info.SetAsChild(int(self.winId()), rect)
        self.browser = cef.CreateBrowserSync(window_info, url=self.start_url)

    def on_timer(self):
        cef.MessageLoopWork()

    def resizeEvent(self, event):
        if self.browser:
            self.browser.SetBounds(0, 0, self.width(), self.height())
        super().resizeEvent(event)

    def load_url(self, url):
        if self.browser:
            self.browser.LoadUrl(url)

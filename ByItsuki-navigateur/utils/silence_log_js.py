from PyQt6.QtWebEngineCore import QWebEnginePage

class SilentWebEnginePage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, message, line, source_id):
        pass 

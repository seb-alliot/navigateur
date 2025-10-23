from PyQt6.QtWebEngineCore import QWebEnginePage, QWebEngineCertificateError

class SilentWebEnginePage(QWebEnginePage):
    def __init__(self, profile, parent=None):
        super().__init__(profile, parent)

    #  Supprime tous les messages de la console JS
    def javaScriptConsoleMessage(self, level, message, line, source_id):
        pass

    #  Bloque les pop-ups de type alert(), confirm(), prompt()
    def javaScriptDialog(self, securityOrigin, dialogType, msg, defaultPrompt, resultCallback):
        resultCallback("")  # répond vide pour éviter le blocage
        return True  # empêche l’affichage



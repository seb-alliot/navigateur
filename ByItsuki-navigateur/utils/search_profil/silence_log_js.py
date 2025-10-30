from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineCertificateError
from PySide6.QtCore import Signal

class SilentWebEnginePage(QWebEnginePage):
    linkClickedSignal = Signal(str)

    def __init__(self, profile, parent=None):
        super().__init__(profile, parent)

    #  Supprime tous les messages de la console JS
    def javaScriptConsoleMessage(self, level, message, line, source_id):
        pass

    #  Bloque les pop-ups de type alert(), confirm(), prompt()
    def javaScriptDialog(self, securityOrigin, dialogType, msg, defaultPrompt, resultCallback):
        resultCallback("")  # répond vide pour éviter le blocage
        return True  # empêche l’affichage

    #  Ignore les erreurs SSL bloquantes (utile si certificat auto-signé)
    def certificateError(self, error: QWebEngineCertificateError):
        error.ignoreCertificateError()
        return True

    def acceptNavigationRequest(self, url, nav_type, isMainFrame):
        url_str = url.toString()

        # Si c’est un vrai clic sur un lien
        if nav_type == QWebEnginePage.NavigationTypeLinkClicked:
            self.linkClickedSignal.emit(url_str)
            return True  # autorise la navigation

        # Si la page principale change (ex : Bing redirige après validation)
        if isMainFrame and nav_type == QWebEnginePage.NavigationTypeOther:
            self.linkClickedSignal.emit(url_str)
            return True

        return super().acceptNavigationRequest(url, nav_type, isMainFrame)
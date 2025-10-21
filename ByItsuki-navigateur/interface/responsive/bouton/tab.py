from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PyQt6.QtWebEngineWidgets import QWebEngineView
from utils.silence_log_js import SilentWebEnginePage

def create_tab(parent, title="Nouvel onglet", slot=None, min_width=800, max_width=None, min_height=600, max_height=None):
    """
    Crée un onglet avec une QWebEngineView intégré et des tailles configurables.

    Args:
        parent: Widget parent pour le WebEnginePage.
        title (str): Titre de l'onglet.
        min_width (int): Largeur minimale de l'onglet.
        max_width (int|None): Largeur maximale (None = illimité).
        min_height (int): Hauteur minimale de l'onglet.
        max_height (int|None): Hauteur maximale (None = illimité).

    Returns:
        QWidget: Le widget onglet prêt à être ajouté à un QTabWidget.
    """
    tab_widget = QWidget()
    layout = QVBoxLayout(tab_widget)

    web_view = QWebEngineView()
    web_view.setMinimumSize(min_width, min_height)
    if max_width is not None and max_height is not None:
        web_view.setMaximumSize(max_width, max_height)
    else:
        web_view.setMaximumSize(16777215, 16777215)  # équivalent Qt.QWIDGETSIZE_MAX

    web_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    web_view.setPage(SilentWebEnginePage(parent.profile, parent))

    layout.addWidget(web_view)

    # On peut stocker le titre si nécessaire
    tab_widget.title = title
    tab_widget.web_view = web_view

    return tab_widget

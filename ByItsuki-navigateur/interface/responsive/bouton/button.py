from PyQt6.QtWidgets import QPushButton

def create_button(text, slot, min_width=200, max_width=300, min_height=30, max_height=45, tool_tip="", extra_style=""):
    """
    Crée un QPushButton modulaire avec taille, style et callback personnalisés.

    Args:
        text (str): Texte affiché sur le bouton.
        slot (callable): Fonction à exécuter lors du clic.
        min_width (int): Largeur minimale du bouton.
        max_width (int): Largeur maximale du bouton.
        min_height (int): Hauteur minimale du bouton.
        max_height (int): Hauteur maximale du bouton.
        extra_style (str): CSS supplémentaire à appliquer.

    Returns:
        QPushButton: Le bouton créé et prêt à être ajouté à un layout.
    """
    button = QPushButton(text)
    button.setMinimumSize(min_width, min_height)
    button.setMaximumSize(max_width, max_height)
    if extra_style:
        button.setStyleSheet(extra_style)
    if tool_tip:
        button.setToolTip(tool_tip)
    button.clicked.connect(slot)
    return button

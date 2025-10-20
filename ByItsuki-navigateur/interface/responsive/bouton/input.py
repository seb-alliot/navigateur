from PyQt6.QtWidgets import QLineEdit

def create_input(placeholder, min_width=200, max_width=300, min_height=30, max_height=45, extra_style=""):
    """
    Crée un QLineEdit modulaire avec taille, style et placeholder personnalisés.

    Args:
        placeholder (str): Texte d'indice affiché dans le champ.
        min_width (int): Largeur minimale du champ.
        max_width (int): Largeur maximale du champ.
        min_height (int): Hauteur minimale du champ.
        max_height (int): Hauteur maximale du champ.
        extra_style (str): CSS supplémentaire à appliquer.

    Returns:
        QLineEdit: Le champ créé et prêt à être ajouté à un layout.
    """
    input_field = QLineEdit()
    input_field.setPlaceholderText(placeholder)
    input_field.setMinimumSize(min_width, min_height)
    input_field.setMaximumSize(max_width, max_height)
    if extra_style:
        input_field.setStyleSheet(extra_style)
    return input_field

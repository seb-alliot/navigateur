from PySide6.QtWidgets import QComboBox

def create_select(options=None, default_index=0, width=None, height=None, tooltip=""):
    """Créer un menu déroulant (QComboBox) avec des options données."""
    combo_box = QComboBox()
    options = options if options is not None else []
    combo_box.addItems(options)
    combo_box.setCurrentIndex(default_index)
    combo_box.setToolTip(tooltip)

    if width is not None:
        combo_box.setFixedWidth(width)
    if height is not None:
        combo_box.setFixedHeight(height)

    return combo_box

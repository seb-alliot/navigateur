from PySide6.QtWidgets import QLineEdit

def create_input(placeholder, slot=None, min_width=200, max_width=None, min_height=30, max_height=45, tooltip="", extra_style=""):
    input_field = QLineEdit()
    input_field.setPlaceholderText(placeholder)
    input_field.setMinimumSize(min_width, min_height)
    input_field.setToolTip(tooltip)

    # Si max_width est None, on n'impose pas de limite
    if max_width is not None:
        input_field.setMaximumWidth(max_width)
    input_field.setMaximumHeight(max_height)

    if extra_style:
        input_field.setStyleSheet(extra_style)

    return input_field

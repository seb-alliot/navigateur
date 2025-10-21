from PyQt6.QtWidgets import QLineEdit

def create_input(placeholder,tool_tip="", min_width=200, max_width=300, min_height=30, max_height=45, extra_style=""):

    input_field = QLineEdit()
    input_field.setPlaceholderText(placeholder)
    input_field.setMinimumSize(min_width, min_height)
    input_field.setMaximumSize(max_width, max_height)

    if extra_style:
        input_field.setStyleSheet(extra_style)
    if tool_tip:
        input_field.setToolTip(tool_tip)

    return input_field

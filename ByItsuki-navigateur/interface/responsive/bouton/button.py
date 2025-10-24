from PySide6.QtWidgets import QPushButton

def create_button(placeholder, slot, min_width=200, max_width=300, min_height=30, max_height=45, tool_tip="", extra_style=""):

    button = QPushButton(placeholder)
    button.setMinimumSize(min_width, min_height)
    button.setMaximumSize(max_width, max_height)
    if extra_style:
        button.setStyleSheet(extra_style)
    if tool_tip:
        button.setToolTip(tool_tip)
    button.clicked.connect(slot)
    return button

from PySide6.QtCore import Qt, QMimeData, QPoint, Signal
from PySide6.QtGui import QDrag
from PySide6.QtWidgets import QPushButton, QApplication

class DropButton(QPushButton):
    drop = Signal(str)
    def __init__(self, line_edit, icon=None):
        super().__init__()
        self.line_edit = line_edit
        if icon:
            self.setIcon(icon)
        self.setFixedSize(40, 40)
        self.drag_start_pos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            parent = self.parent()
            if hasattr(parent, "favorite_bar"):
                parent.favorite_bar.show()
            self.drag_start_pos = event.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        if (event.pos() - self.drag_start_pos).manhattanLength() < QApplication.startDragDistance():
            return

        # --- Gestion du drag ---
        drag = QDrag(self)
        mime_data = QMimeData()
        url_text = self.line_edit.text().strip()
        if not url_text:
            return
        mime_data.setText(url_text)
        drag.setMimeData(mime_data)
        drag.exec(Qt.CopyAction | Qt.MoveAction)

        self.drop.emit(url_text)
        # Reset drag
        self.drag_start_pos = None

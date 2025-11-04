from PySide6.QtCore import Signal, Qt, QMimeData
from PySide6.QtGui import QDrag
from PySide6.QtWidgets import QPushButton, QApplication


class DropButton(QPushButton):
    drop = Signal(str)

    def __init__(self, line_edit=None, icon=None, parent=None):
        super().__init__(parent)
        self.line_edit = line_edit
        self.drag_start_pos = None

        if icon:
            self.setIcon(icon)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_pos = event.pos()

            parent_widget = self.parentWidget()
            if parent_widget and hasattr(parent_widget, "favorite_bar"):
                parent_widget.favorite_bar.show()

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        if not self.drag_start_pos:
            return
        if (event.pos() - self.drag_start_pos).manhattanLength() < QApplication.startDragDistance():
            return

        drag = QDrag(self)
        mime_data = QMimeData()

        if self.line_edit and self.line_edit.text().strip():
            mime_data.setText(self.line_edit.text().strip())
        else:
            mime_data.setText("")

        drag.setMimeData(mime_data)
        drag.exec(Qt.CopyAction | Qt.MoveAction)

        self.drop.emit(mime_data.text())
        self.drag_start_pos = None

    def mouseReleaseEvent(self, event):
        self.drag_start_pos = None
        super().mouseReleaseEvent(event)

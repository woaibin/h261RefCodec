from PyQt5.QtWidgets import QGraphicsRectItem
from PyQt5.QtGui import QColor, QBrush, QPen
from PyQt5.QtCore import QRectF


class HoverableRect(QGraphicsRectItem):
    """
    A QGraphicsRectItem that supports hover events to highlight itself.
    """
    def __init__(self, rect: QRectF, color: QColor, parent=None):
        super().__init__(rect, parent)
        self.default_color = color
        self.highlight_color = color.lighter(150)  # Brighter color for hover
        self.setBrush(QBrush(self.default_color))
        self.setPen(QPen(self.default_color.darker(150), 2))
        self.setAcceptHoverEvents(True)

    def hoverEnterEvent(self, event):
        """
        Triggered when the mouse enters the rectangle.
        """
        self.setBrush(QBrush(self.highlight_color))
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        """
        Triggered when the mouse leaves the rectangle.
        """
        self.setBrush(QBrush(self.default_color))
        super().hoverLeaveEvent(event)
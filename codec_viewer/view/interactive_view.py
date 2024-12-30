from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QWheelEvent, QMouseEvent


class InteractiveGraphicsView(QGraphicsView):
    """
    A QGraphicsView that supports mouse drag for moving and wheel or touchpad gestures for scaling.
    """
    def __init__(self, mouse_move_cb=None, parent=None):
        super().__init__(parent)
        self.last_mouse_pos = None
        self.zoom_factor = 1.0  # Factor by which to scale on zoom
        self._is_panning = False
        self.mouse_move_cb = mouse_move_cb

        # Allow unlimited panning by setting an infinite scene rect
        self.setSceneRect(float('-inf'), float('-inf'), float('inf'), float('inf'))
        self.setMouseTracking(True)

    def mousePressEvent(self, event: QMouseEvent):
        """
        Start panning on right-button or middle-button click.
        """
        if event.button() == Qt.LeftButton:
            self.last_mouse_pos = event.pos()
            self._is_panning = True
            self.setCursor(Qt.ClosedHandCursor)  # Change cursor to indicate panning
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        """
        Pan the view when dragging with the right or middle mouse button.
        """
        pos: QPointF = event.pos()

        if self._is_panning and self.last_mouse_pos:
            delta = self.mapToScene(event.pos()) - self.mapToScene(self.last_mouse_pos)
            self.translate(delta.x(), delta.y())  # Move the scene
            self.last_mouse_pos = event.pos()  # Update the last position
        else:
            super().mouseMoveEvent(event)
            if self.mouse_move_cb is not None:
                self.mouse_move_cb(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        """
        Stop panning on right-button or middle-button release.
        """
        if event.button() == Qt.LeftButton:
            self._is_panning = False
            self.setCursor(Qt.ArrowCursor)  # Reset cursor to default
        else:
            super().mouseReleaseEvent(event)

    def wheelEvent(self, event: QWheelEvent):
        """
        Zoom in/out with the mouse wheel or touchpad gesture.
        """
        zoom_in = event.angleDelta().y() > 0  # Check scroll direction

        # Current scale factors
        current_scale = self.transform().m11()  # Horizontal scale factor (uniform scaling)

        # Zoom limits
        min_scale = 0.2  # Minimum zoom level (20% of the original size)
        max_scale = 5.0  # Maximum zoom level (500% of the original size)

        # Apply the zoom
        if zoom_in:
            self.scale(1.02, 1.02)  # Smooth zoom in
        else:
            self.scale(0.98, 0.98)  # Smooth zoom out

    def gestureEvent(self, event):
        """
        Handle pinch gestures for scaling (macOS touchpad support).
        """
        if event.gesture(Qt.PinchGesture):
            pinch = event.gesture(Qt.PinchGesture)
            if pinch.state() == Qt.GestureUpdated:
                self.scale(pinch.scaleFactor(), pinch.scaleFactor())
            return True
        return super().event(event)
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsTextItem, QGraphicsRectItem
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QBrush, QColor, QFont


class MatrixDisplayView(QGraphicsView):
    """
    A QGraphicsView-based widget to display a matrix in a scrollable, pannable, and zoomable view.
    """
    def __init__(self, matrix, parent=None):
        super().__init__(parent)

        # Create a QGraphicsScene for the matrix
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        # Enable mouse interactions (panning and zooming)
        self.setRenderHints(self.renderHints())
        self.setMouseTracking(True)
        self.setDragMode(QGraphicsView.ScrollHandDrag)  # Enable panning with drag

        # Allow unlimited panning by setting an infinite scene rect
        self.setSceneRect(float('-inf'), float('-inf'), float('inf'), float('inf'))

    def display_matrix(self, matrix):
        """
        Display the matrix in the QGraphicsScene.
        """
        rows = len(matrix)
        cols = len(matrix[0]) if rows > 0 else 0
        cell_size = 50  # Size of each cell in pixels

        # Fonts and colors
        font = QFont("Arial", 10)
        font.setBold(True)
        default_brush = QBrush(QColor(240, 240, 240))  # Light gray background for cells
        alternate_brush = QBrush(QColor(255, 255, 255))  # White background for alternating cells

        for i in range(rows):
            for j in range(cols):
                # Calculate the position of the cell
                top_left_x = j * cell_size
                top_left_y = i * cell_size

                # Draw the cell rectangle
                rect = QRectF(top_left_x, top_left_y, cell_size, cell_size)
                cell = QGraphicsRectItem(rect)

                # Set alternating background colors
                if (i + j) % 2 == 0:
                    cell.setBrush(default_brush)
                else:
                    cell.setBrush(alternate_brush)

                cell.setPen(QColor(200, 200, 200))  # Light gray border
                self.scene.addItem(cell)

                # Add the text to the cell
                value = str(matrix[i][j])  # Convert matrix value to string
                text = QGraphicsTextItem(value)
                text.setFont(font)

                # Position the text in the center of the cell
                text.setPos(top_left_x + cell_size / 4, top_left_y + cell_size / 6)
                self.scene.addItem(text)

    def wheelEvent(self, event):
        """
        Override the wheel event to implement smooth zooming.
        """
        zoom_in = event.angleDelta().y() > 0  # Check scroll direction
        zoom_factor = 1.1 if zoom_in else 0.9

        # Apply zoom
        self.scale(zoom_factor, zoom_factor)

    def mousePressEvent(self, event):
        """
        Enable panning with the left mouse button.
        """
        if event.button() == Qt.LeftButton:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """
        Disable panning after releasing the mouse button.
        """
        if event.button() == Qt.LeftButton:
            self.setDragMode(QGraphicsView.NoDrag)
        super().mouseReleaseEvent(event)
import sys
import random
from typing import List, Tuple, Optional
from PyQt5.QtWidgets import (
    QApplication,
    QGraphicsView,
    QGraphicsScene,
    QGraphicsRectItem,
    QGraphicsPixmapItem,
    QVBoxLayout,
    QWidget,
    QLabel,
)
from PyQt5.QtGui import QPixmap, QPen, QColor, QBrush
from PyQt5.QtCore import QRectF, Qt, QPointF


class Macroblock:
    """
    Represents a macroblock with position, size, and sub-macroblock information.
    """
    def __init__(self, x: int, y: int, width: int, height: int, sub_blocks: List[Tuple[int, int, int, int]] = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.sub_blocks = sub_blocks if sub_blocks else []

    def add_sub_block(self, x: int, y: int, width: int, height: int):
        self.sub_blocks.append((x, y, width, height))


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


class MacroblockVisualizer(QWidget):
    """
    A PyQt-based tool for visualizing macroblocks and sub-macroblocks interactively.
    """
    def __init__(self, image_path: str):
        super().__init__()

        # Load the image
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            raise FileNotFoundError(f"Image not found at path: {image_path}")

        # Set up the graphics view and scene
        self.view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)

        # Add the image to the scene
        self.image_item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(self.image_item)

        # Enable dragging and scaling
        self.view.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.view.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.view.setDragMode(QGraphicsView.ScrollHandDrag)

        # Mouse tracking label
        self.hover_label = QLabel("Hover over a macroblock or sub-block...")
        self.hover_label.setFixedHeight(20)

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(self.view)
        layout.addWidget(self.hover_label)
        self.setLayout(layout)
        self.setWindowTitle("Macroblock Visualizer")
        self.resize(800, 600)

        # Macroblocks storage
        self.macroblocks = []

    def add_macroblock(self, macroblock: Macroblock):
        """
        Add a macroblock and its sub-macroblocks to the scene.
        """
        # Random color for the macroblock
        macroblock_color = QColor(
            random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 150
        )
        rect = QRectF(macroblock.x, macroblock.y, macroblock.width, macroblock.height)
        mb_item = HoverableRect(rect, macroblock_color)
        self.scene.addItem(mb_item)

        # Add sub-macroblocks
        for sub_block in macroblock.sub_blocks:
            sub_block_color = QColor(
                random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 100
            )
            sub_rect = QRectF(sub_block[0], sub_block[1], sub_block[2], sub_block[3])
            sub_mb_item = HoverableRect(sub_rect, sub_block_color)
            self.scene.addItem(sub_mb_item)

        # Store macroblock info
        self.macroblocks.append((macroblock, mb_item))

    def mouseMoveEvent(self, event):
        """
        Track the mouse position and detect hovered macroblocks or sub-macroblocks.
        """
        # Map mouse position to the scene
        pos: QPointF = self.view.mapToScene(event.pos())

        # Check if the mouse is over any macroblock or sub-macroblock
        for macroblock, mb_item in self.macroblocks:
            # Check if the mouse is inside the macroblock
            if mb_item.rect().contains(pos):
                self.hover_label.setText(
                    f"Hovering over Macroblock: ({macroblock.x}, {macroblock.y}, {macroblock.width}, {macroblock.height})"
                )
                return

            # Check sub-macroblocks
            for sub_block in macroblock.sub_blocks:
                sub_block_rect = QRectF(sub_block[0], sub_block[1], sub_block[2], sub_block[3])
                if sub_block_rect.contains(pos):
                    self.hover_label.setText(
                        f"Hovering over Sub-Macroblock: ({sub_block[0]}, {sub_block[1]}, {sub_block[2]}, {sub_block[3]})"
                    )
                    return

        # If no block is hovered
        self.hover_label.setText("Hover over a macroblock or sub-block...")

    def reset_view(self):
        """
        Reset the view to fit the entire scene.
        """
        self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)


def main():
    app = QApplication(sys.argv)

    # Initialize the visualizer
    visualizer = MacroblockVisualizer("../wrinkles.png")

    # Add some macroblocks and sub-macroblocks
    mb1 = Macroblock(50, 50, 200, 200)
    mb1.add_sub_block(50, 50, 100, 100)
    mb1.add_sub_block(150, 50, 100, 100)
    mb1.add_sub_block(50, 150, 100, 100)
    mb1.add_sub_block(150, 150, 100, 100)

    mb2 = Macroblock(300, 300, 150, 150)
    mb2.add_sub_block(300, 300, 75, 75)
    mb2.add_sub_block(375, 300, 75, 75)

    visualizer.add_macroblock(mb1)
    visualizer.add_macroblock(mb2)

    # Reset the view to show the entire scene
    visualizer.reset_view()
    visualizer.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
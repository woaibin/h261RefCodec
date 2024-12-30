from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                             QGraphicsScene, QGraphicsPixmapItem, QMenu, QAction, QStackedWidget, QPushButton)
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import QRectF, QPointF, Qt
from macroblock import Macroblock
from codec_viewer.view.interactive_view import InteractiveGraphicsView  # Import our custom view
from codec_viewer.view.matrix_view import MatrixDisplayView  # Import our custom view
from PIL import Image, ImageDraw


class MacroblockVisualizer(QWidget):
    """
    A PyQt-based tool for visualizing macroblocks and sub-macroblocks interactively.
    """

    def __init__(self, image_path: str):
        super().__init__()

        # Load the image
        pixmap = QPixmap(image_path)
        self.org_img_width = pixmap.width()
        self.org_img_height = pixmap.height()
        if pixmap.isNull():
            raise FileNotFoundError(f"Image not found at path: {image_path}")

        # Set up the graphics view and scene
        self.img_view = InteractiveGraphicsView(self.handleBlkHoverEvent)  # Use the custom interactive view
        self.matrix_view = MatrixDisplayView([])  # Initialize with an empty matrix

        self.img_scene = QGraphicsScene()
        self.img_view.setScene(self.img_scene)
        self.matrix_scene = QGraphicsScene()
        self.matrix_view.setScene(self.matrix_scene)

        # Add the image to the scene
        self.image_item = QGraphicsPixmapItem(pixmap)
        self.img_scene.addItem(self.image_item)

        # Mouse tracking label
        self.hover_label = QLabel("Hover over a macroblock or sub-block...")
        self.hover_label.setFixedHeight(20)

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(self.img_view)
        layout.addWidget(self.hover_label)
        self.setLayout(layout)
        self.setWindowTitle("Macroblock Visualizer")
        self.resize(800, 600)

        # Macroblocks storage
        self.macroblocks = []
        self.default_pix_map = None
        self.selected_mb = None
        self.selected_sub_mb = None

    def add_macroblock(self, macroblock: Macroblock):
        # Store macroblock info
        self.macroblocks.append(macroblock)

    def contextMenuEvent(self, event):
        """
        Show a right-click menu with options to display matrices.
        """
        # Create the context menu
        menu = QMenu(self)

        # Add options to the menu
        show_mb_matrix_action = QAction("Show Macroblock Matrix", self)
        show_sub_mb_matrix_action = QAction("Show Sub-Macroblock Matrix", self)

        # Connect menu actions to methods
        show_mb_matrix_action.triggered.connect(self.show_macroblock_matrix)
        show_sub_mb_matrix_action.triggered.connect(self.show_sub_macroblock_matrix)

        # Add actions to the menu
        menu.addAction(show_mb_matrix_action)
        menu.addAction(show_sub_mb_matrix_action)

        # Show the menu at the cursor position
        menu.exec_(event.globalPos())

    def show_macroblock_matrix(self):
        """
        Display the macroblock matrix using the MatrixDisplayView.
        """
        if not self.selected_mb:
            self.hover_label.setText("No macroblock selected!")
            return

        # Generate a matrix for the selected macroblock (mock example)
        # Replace this with actual macroblock data if available
        mb_matrix = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]

        self.matrix_view.display_matrix(mb_matrix)  # Update the matrix in the view

    def show_sub_macroblock_matrix(self):
        """
        Display the sub-macroblock matrix using the MatrixDisplayView.
        """
        if not self.selected_sub_mb:
            self.hover_label.setText("No sub-macroblock selected!")
            return

        # Generate a matrix for the selected sub-macroblock (mock example)
        # Replace this with actual sub-macroblock data if available
        sub_mb_matrix = [
            [10, 20],
            [30, 40]
        ]

        self.matrix_view.display_matrix(sub_mb_matrix)  # Update the matrix in the view

    def handleBlkHoverEvent(self, event):
        """
        Track the mouse position and detect hovered macroblocks or sub-macroblocks,
        translating the position according to the scale factor.
        """
        # Map mouse position to the scene
        pos: QPointF = self.img_view.mapToScene(event.pos())  # Map to scene coordinates

        # Get the scale factors for the view
        # x_scale_factor = self.view.transform().m11()  # Horizontal scaling factor
        # y_scale_factor = self.view.transform().m22()  # Vertical scaling factor

        # Translate the mouse position to the image's coordinates
        image_x = pos.x()
        image_y = pos.y()

        # Remove any existing highlight rect (if previously added)
        if hasattr(self, "highlight_rect_mb") and self.highlight_rect_mb:
            self.img_scene.removeItem(self.highlight_rect_mb)
            self.highlight_rect_mb = None

        if hasattr(self, "highlight_rect_sub_mb") and self.highlight_rect_sub_mb:
            self.img_scene.removeItem(self.highlight_rect_sub_mb)
            self.highlight_rect_sub_mb = None

        # Check if the mouse is over any macroblock or sub-macroblock
        hover_mb = None
        hover_sub_mb = None
        for macroblock in self.macroblocks:
            # Check if the mouse is inside the macroblock
            if (
                    macroblock.x <= image_x <= macroblock.x + macroblock.width
                    and macroblock.y <= image_y <= macroblock.y + macroblock.height
            ):
                self.hover_label.setText(
                    f"Hovering over Macroblock: ({macroblock.x}, {macroblock.y}, {macroblock.width}, {macroblock.height})"
                )
                # Highlight the macroblock
                self.highlight_rect_mb = self.img_scene.addRect(
                    QRectF(
                        macroblock.x, macroblock.y, macroblock.width, macroblock.height
                    ),
                    pen=QColor(255, 0, 0, 200),  # Red outline
                    brush=QColor(255, 0, 0, 50),  # Semi-transparent red fill
                )

                hover_mb = macroblock

                # Check sub-macroblocks
                for sub_block in hover_mb.sub_blocks:
                    sub_block_rect = QRectF(
                        sub_block.x, sub_block.y, sub_block.width, sub_block.height
                    )
                    if sub_block_rect.contains(QPointF(image_x, image_y)):
                        self.hover_label.setText(
                            f"Hovering over Sub-Macroblock: ({sub_block.x}, {sub_block.y}, {sub_block.width}, {sub_block.height})"
                        )
                        hover_sub_mb = sub_block

                        # Highlight the macroblock
                        self.highlight_rect_sub_mb = self.img_scene.addRect(
                            QRectF(
                                sub_block.x, sub_block.y, sub_block.width, sub_block.height
                            ),
                            pen = QColor(255, 255, 0, 200),  # Bright yellow with 200 alpha (transparency)
                            brush=QColor(255, 0, 0, 150),  # Semi-transparent red fill
                        )

                if hover_mb is not None or hover_sub_mb is not None:
                    self.hover_label.setText("Hover over a macroblock:"
                                             + str(hover_mb.work_out_index_in_2d_form(self.org_img_width))
                                             + " or sub-block..." + str(hover_sub_mb.index))
                    self.selected_mb = hover_mb
                    self.selected_sub_mb = hover_sub_mb
                    break

    def bake_macroblocks(self, baked_image_path: str):
        """
        Load a pre-baked image as the background and draw macroblocks and sub-macroblocks
        onto it using Pillow. Perform alpha blending and save the result to a pixmap.
        """
        # Load the pre-baked background image
        try:
            baked_image = Image.open(baked_image_path).convert("RGBA")  # Ensure image is in RGBA mode
        except FileNotFoundError:
            raise FileNotFoundError(f"Background image not found at path: {baked_image_path}")

        # Create a copy to draw on
        baked_image_cp = baked_image.copy()

        # Create a drawing context
        draw = ImageDraw.Draw(baked_image_cp, "RGBA")

        # Perform alpha blending between the original image and the drawn image
        blended_image = Image.alpha_composite(baked_image, baked_image_cp)

        # Optionally save to a file (if required)
        blended_image.save("blended_output.png")

        # Convert the updated image to a QPixmap and set as the scene background
        baked_pixmap = QPixmap("blended_output.png")
        self.image_item.setPixmap(baked_pixmap)
        self.default_pix_map = baked_pixmap

    def showEvent(self, event):
        self.img_view.fitInView(self.img_scene.sceneRect(), Qt.IgnoreAspectRatio)

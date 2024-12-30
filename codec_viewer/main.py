import sys
from PyQt5.QtWidgets import QApplication
from macroblock_visualizer import MacroblockVisualizer
from macroblock import Macroblock
from segmentation import BlockSegmentation
from macroblock_template import MacroBlockTemplate,SubMacroBlockTemplate
from PIL import Image

def get_image_metadata(image_path):
    """
    Retrieve metadata information of an image.

    Args:
        image_path (str): Path to the image file.

    Returns:
        dict: A dictionary containing metadata like width, height, format, mode, etc.
    """
    try:
        # Open the image
        with Image.open(image_path) as img:
            # Get basic metadata
            metadata = {
                "width": img.width,
                "height": img.height,
                "format": img.format,  # e.g., JPEG, PNG
                "mode": img.mode,      # e.g., RGB, RGBA, CMYK
                "info": img.info       # Additional metadata (e.g., EXIF data)
            }
        return metadata
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    app = QApplication(sys.argv)

    # Initialize the visualizer
    image_path = "../wrinkles.png"
    visualizer = MacroblockVisualizer(image_path)
    metadata = get_image_metadata(image_path)

    segmentation_process = BlockSegmentation(MacroBlockTemplate(32, 32), SubMacroBlockTemplate(8,8))
    mb_list = segmentation_process.go_segmentation(metadata["width"], metadata["height"])

    for mb in mb_list:
        visualizer.add_macroblock(mb)

    visualizer.bake_macroblocks(image_path)

    # Reset the view to show the entire scene
    visualizer.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
from macroblock import Macroblock
from macroblock_template import MacroBlockTemplate, SubMacroBlockTemplate
from typing import List
from sub_macroblock import SubMacroblock

class BlockCalculation:
    @staticmethod
    def get_rect_from_block_list(block_list):
        """
        Calculates the bounding rectangle that encompasses all blocks in the block_list.

        Args:
            block_list (list): A list of blocks, where each block has properties
                               x, y, width, and height.

        Returns:
            tuple: A tuple (x, y, width, height) representing the bounding rectangle.
        """
        if not block_list:
            return None  # Return None if the list is empty

        # Initialize the bounding rectangle with the first block's values
        min_x = block_list[0].x
        min_y = block_list[0].y
        max_x = block_list[0].x + block_list[0].width
        max_y = block_list[0].y + block_list[0].height

        # Iterate through the rest of the blocks to expand the bounding rectangle
        for block in block_list:
            min_x = min(min_x, block.x)
            min_y = min(min_y, block.y)
            max_x = max(max_x, block.x + block.width)
            max_y = max(max_y, block.y + block.height)

        # Calculate the width and height of the bounding rectangle
        bounding_width = max_x - min_x
        bounding_height = max_y - min_y

        # Return the rectangle as (x, y, width, height)
        return min_x, min_y, bounding_width, bounding_height


class BlockSegmentation:
    """
    Encapsulates different segmentation strategies for arranging macroblocks and sub-macroblocks.
    """

    def __init__(self, macroblock_template: MacroBlockTemplate, sub_macroblock_template: SubMacroBlockTemplate):
        """
        Initialize with predefined macroblock and sub-macroblock templates.
        """
        self.macroblock_template = macroblock_template
        self.sub_macroblock_template = sub_macroblock_template

    def default_segmentation(self, image_width: int, image_height: int):
        """
        Default segmentation strategy: Divide the image into sub-macroblocks.
        """
        sub_macro_blocks = []

        # Subdivide each pic into sub-macroblocks
        for sub_y in range(0, image_height, self.sub_macroblock_template.height):
            for sub_x in range(0, image_width, self.sub_macroblock_template.width):
                sub_width = min(self.sub_macroblock_template.width, image_width - sub_x)
                sub_height = min(self.sub_macroblock_template.height, image_height - sub_y)
                sub_macro_blocks.append(SubMacroblock(sub_x, sub_y, sub_width, sub_height))

        return {"sub_macro_blocks": sub_macro_blocks}

    # Additional segmentation strategies can be added here as methods

    def h261_macro_blocks_segmentation_from_blocks_rgb(self, sub_macro_blocks: List[SubMacroblock]):
        import macroblock
        macroblock_list: List[Macroblock] = []
        sub_mb_list_temp = []
        for index, sub_macro_block in enumerate(sub_macro_blocks):
            if index % 4 == 0 and index != 0:
                rect = BlockCalculation.get_rect_from_block_list(sub_mb_list_temp)
                temp_mb = Macroblock(rect[0], rect[1], rect[2], rect[3], int(index / 4 - 1))
                temp_mb.add_sub_block_list(sub_mb_list_temp)
                sub_mb_list_temp.clear()
                macroblock_list.append(temp_mb)

            sub_macro_block.set_index(index % 4)
            sub_mb_list_temp.append(sub_macro_block)

        return macroblock_list



    def go_segmentation(self, img_width:int, img_height:int):
        default_seg_result = self.default_segmentation(img_width, img_height)
        mb_list = self.h261_macro_blocks_segmentation_from_blocks_rgb(default_seg_result["sub_macro_blocks"])

        return mb_list


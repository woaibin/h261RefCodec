from typing import List, Tuple
from sub_macroblock import SubMacroblock


class Macroblock:
    """
    Represents a macroblock with position, size, and sub-macroblock information.
    """

    def __init__(self, x: int, y: int, width: int, height: int, index_1d: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.index_1d = index_1d
        self.sub_blocks: List[SubMacroblock] = []

    def add_sub_block(self, x: int, y: int, width: int, height: int):
        """
        Add a sub-macroblock to the macroblock.

        Args:
            x (int): Top-left x-coordinate of the sub-macroblock.
            y (int): Top-left y-coordinate of the sub-macroblock.
            width (int): Width of the sub-macroblock.
            height (int): Height of the sub-macroblock.
        """
        self.sub_blocks.append(SubMacroblock(x, y, width, height))

    def add_sub_block_list(self, sub_mb_list):
        """
        Add a sub-macroblock to the macroblock.

        Args:
            x (int): Top-left x-coordinate of the sub-macroblock.
            y (int): Top-left y-coordinate of the sub-macroblock.
            width (int): Width of the sub-macroblock.
            height (int): Height of the sub-macroblock.
        """
        for sub_mb in sub_mb_list:
            self.sub_blocks.append(sub_mb)

    def work_out_index_in_2d_form(self, grid_width: int) -> Tuple[int, int]:
        """
        Convert the 1D index of the macroblock to a 2D (row, col) index.

        Args:
            grid_width (int): The total number of columns in the grid.

        Returns:
            Tuple[int, int]: The (row, col) index in 2D form.
        """
        row = self.index_1d // grid_width  # Integer division to get the row
        col = self.index_1d % grid_width  # Modulus to get the column
        return row, col

from typing import List, Tuple


class SubMacroblock:
    """
    Represents a macroblock with position, size, and sub-macroblock information.
    """

    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.index = 0

    def set_index(self, index):
        self.index = index

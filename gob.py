from macroblock import MacroblockParser, Macroblock
import globalVar
from typing import List  # Import List for type hinting

class GOB:
    """
    A class to represent a Group of Blocks (GOB) in H.261.

    Attributes:
    -----------
    start_bit_position : int
        The position in the bitstream where the GOB start code was found.
    gn : int
        Group number (4 bits).
    gquant : int
        Quantizer information (5 bits).
    gei : bool
        Extra insertion information (1 bit).
    gspare_size : int
        Size of the GSPARE field in bits.
    macroblocks : list
        List of Macroblock objects parsed within the GOB.
    """

    def __init__(self, start_bit_position, gn, gquant, gei, gspare_size):
        self.start_bit_position = start_bit_position
        self.gn = gn
        self.gquant = gquant
        self.gei = gei
        self.gspare_size = gspare_size
        self.macroblocks: List[Macroblock] = []  # List to hold parsed macroblocks
        self.enable_print = False

    def __str__(self):
        if not self.enable_print:
            return ""

        macroblock_str = "\n\t".join([str(mb) for mb in self.macroblocks])
        return (f"GOB(start_bit_position={self.start_bit_position}, gn={self.gn}, "
                f"gquant={self.gquant}, gei={self.gei}, gspare_size={self.gspare_size}, "
                f"macroblocks=\n\t{macroblock_str})")


class GOBParser:
    """
    A parser for GOBs (Group of Blocks) in H.261 bitstreams.
    """

    GOB_START_CODE = '0000000000000001'  # 16-bit GOB Start Code

    def __init__(self):
        self.macroblock_parser = MacroblockParser()

    def parse_gob(self, bit_string, start_index, end_index):
        """
        Parse a GOB header and its macroblocks from the bitstream.

        :param bit_string: The bitstream as a bit string.
        :param start_index: The index where the GOB start code is located.
        :param end_index: The index where the GOB parsing should stop.
        :return: A GOB object and the updated index.
        """
        if start_index == end_index:
            return None, end_index

        current_index = start_index

        # Parse GN (Group Number) (4 bits)
        gn = int(bit_string[current_index:current_index + 4], 2)
        current_index += 4

        # Parse GQUANT (Quantizer Information) (5 bits)
        gquant = int(bit_string[current_index:current_index + 5], 2)
        current_index += 5

        # Parse GEI (Extra Insertion Information) (1 bit)
        gei = int(bit_string[current_index], 2) == 1
        current_index += 1

        # Parse GSPARE based on GEI (0, 8, 16... bits)
        gspare_size = 0
        if gei:
            while gei:
                gspare_size += 8  # Each GSPARE chunk is 8 bits
                current_index += 8

                if current_index >= end_index:
                    raise ValueError("Not enough data to check the next GEI bit")
                gei = int(bit_string[current_index], 2) == 1
                current_index += 1

        # Create GOB object
        gob = GOB(start_bit_position=start_index / 8, gn=gn, gquant=gquant, gei=gei, gspare_size=gspare_size)

        # Parse macroblocks within the GOB
        while current_index < end_index:
            last_index = current_index
            #print(f"bxk log out current index: {current_index}")
            macroblock, current_index, mba = self.macroblock_parser._parse_macroblock(bit_string, current_index,
                                                                                      end_index, gquant)
            if macroblock is not None:
                gob.macroblocks.append(macroblock)
            if str(mba) == "MBA stuffing" or str(mba) == "Start code" or mba == -1:
                # stuffing next gob is coming, just return:
                if str(mba) == "Start code":
                    current_index -= 16  # offset back for next gob parsing
                break

        return gob, current_index

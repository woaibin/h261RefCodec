# picture.py

from gob import GOBParser
import globalVar

"""
A class to represent an H.261 picture layer.

Attributes:
-----------
start_bit_position : int
    The position in the bitstream where the picture start code was found.
tr : int
    Temporal reference (5 bits).
ptype : dict
    Type information parsed from the 6-bit PTYPE field.
pei : bool
    Whether PEI (Picture Enhancement Information) exists.
pspare_size : int
    Size of the PSPARE field in bits.
gobs : list
    List of GOB objects parsed within the picture.
"""


class Picture:
    """
    A class to represent an H.261 picture layer.
    """
    def __init__(self, start_bit_position, tr, ptype, pei, pspare_size):
        self.start_bit_position = start_bit_position
        self.tr = tr
        self.ptype = ptype
        self.pei = pei
        self.pspare_size = pspare_size
        self.gobs = []  # To store GOB objects
        self.enable_print = False

    def __str__(self):
        if not self.enable_print:
            return ""

        gob_str = ""
        for gob in self.gobs:
            gob_str += "\n\t\t" + gob.__str__()
        return (f"Picture(start_bit_position={self.start_bit_position}, tr={self.tr}, "
                f"ptype={self.ptype}, peiCnt={self.pei}, pspare_size={self.pspare_size}, "
                f"\n\t\tgobs={gob_str})")


class PictureParser:
    """
    A parser for H.261 pictures.
    """

    PICTURE_START_CODE = '00000000000000010000'  # 20-bit picture start code

    def __init__(self):
        self.gob_parser = GOBParser()

    def parse(self, bit_string, start_index):
        """
        Parse a Picture and its GOBs from the bitstream.

        :param bit_string: The bitstream as a bit string.
        :param start_index: The index where the picture starts.
        :return: A Picture object and the updated index.
        """
        # Parse TR (Temporal Reference) field (5 bits)
        tr, next_index = self._parse_tr(bit_string, start_index)

        # Parse PTYPE (6 bits)
        ptype, next_index = self._parse_ptype(bit_string, next_index)

        # Parse PEI and PSPARE
        pei, pspare_size, next_index = self._parse_pei_and_pspare(bit_string, next_index)

        # Create a new Picture object
        picture = Picture(start_bit_position=start_index / 8, tr=tr, ptype=ptype, pei=pei, pspare_size=pspare_size)

        # Parse GOBs within the picture
        end_index_picture = bit_string.find(PictureParser.PICTURE_START_CODE, next_index);
        while next_index < end_index_picture:
            # Try to find the next GOB start code
            gob_start_index = bit_string.find(GOBParser.GOB_START_CODE, next_index)
            gob_start_index += 16
            if gob_start_index == -1:
                break

            # Define the end index for GOB parsing (e.g., the start of the next picture)
            end_index = bit_string.find(GOBParser.GOB_START_CODE, gob_start_index)
            if end_index == -1:
                break

            # Parse the GOB
            gob, next_index = self.gob_parser.parse_gob(bit_string, gob_start_index, end_index)
            if gob is not None:
                picture.gobs.append(gob)
            else:
                break

        return picture, next_index

    def _parse_tr(self, bit_string, start_index):
        """
        Parse the TR (Temporal Reference) field (5 bits).
        """
        tr = int(bit_string[start_index:start_index + 5], 2)
        return tr, start_index + 5

    def _parse_ptype(self, bit_string, start_index):
        """
        Parse the PTYPE (Type Information) field (6 bits).
        """
        ptype_bits = bit_string[start_index:start_index + 6]
        ptype = {
            "split_screen_indicator": int(ptype_bits[0], 2),
            "document_camera_indicator": int(ptype_bits[1], 2),
            "freeze_picture_release": int(ptype_bits[2], 2),
            "source_format": "CIF" if int(ptype_bits[3], 2) == 1 else "QCIF",  # Bit 4
            "still_image_mode": "off" if int(ptype_bits[4], 2) == 1 else "on"  # Bit 5
        }
        return ptype, start_index + 6

    def _parse_pei_and_pspare(self, bit_string, start_index):
        """
        Parse the PEI and PSPARE fields recursively.
        """
        pei = int(bit_string[start_index], 2) == 1
        pspare_size = 0
        current_index = start_index + 1

        while pei:
            while bit_string[current_index] == '1':
                pspare_size += 1
                current_index += 1
            pspare_size += 1  # Count the final 0 bit that stops the PSPARE sequence

            current_index += 1  # Move to the next PEI bit
            pei = int(bit_string[current_index - 1], 2) == 1

        return pei, pspare_size, current_index
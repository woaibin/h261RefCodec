# Macroblock parsing logic for the H.261 codec
from algorithm import decode_vlc, mba_vlc_table, mtype_vlc_table, mvd_vlc_table, cbp_vlc_table, check_mtype_properties
from block import Block

class Macroblock:
    def __init__(self, mba, mtype, mquant=None, mvd=None, cbp=None, block_data=None):
        """
        Initializes a Macroblock with the parsed values.
        """
        self.mba = mba
        self.mtype = mtype
        self.mquant = mquant
        self.mvd = mvd
        self.cbp = cbp
        self.block_data = block_data

    def __repr__(self):
        return (f"Macroblock(mba={self.mba}, mtype={self.mtype}, mquant={self.mquant}, "
                f"mvd={self.mvd}, cbp={self.cbp}, block_data={self.block_data})")


class MacroblockParser:
    def _parse_macroblock(self, bit_string, start_index, end_index, gquant):
        """
        Parse a macroblock from the bitstream.
        """
        current_index = start_index

        # Parse MBA (Macroblock Address) using VLC table
        mba, current_index, clean_code = decode_vlc(bit_string, current_index, end_index, mba_vlc_table)

        if str(mba) == "MBA stuffing" or str(mba) == "Start code":
            # stuffing next gob is coming, just return:
            return None, current_index, mba

        # Parse MTYPE (Macroblock Type) using VLC table
        mtype, current_index, clean_code = decode_vlc(bit_string, current_index, end_index, mtype_vlc_table)

        # Check MTYPE properties
        mtype_properties = check_mtype_properties(clean_code)

        # Parse MQUANT if indicated by MTYPE
        mquant = None
        if mtype_properties["MQUANT"]:
            if current_index + 5 > end_index:
                raise ValueError("Not enough data to read MQUANT")
            mquant = int(bit_string[current_index: current_index + 5], 2)
            current_index += 5

        # Parse MVD (Motion Vector Data) if indicated by MTYPE
        mvd = None
        if mtype_properties["MVD"]:
            mvd, current_index = self._parse_mvd(bit_string, current_index, end_index)

        # Parse CBP (Coded Block Pattern) if indicated by MTYPE
        cbp = None
        if mtype_properties["CBP"]:
            cbp, current_index, clean_code = decode_vlc(bit_string, current_index, end_index, cbp_vlc_table)

        # Parse Block Data if indicated by MTYPE
        block_data = None
        final_quant = None
        if mquant == None:
            final_quant = gquant
        else:
            final_quant = mquant
        if mtype_properties["TCOEFF"]:
            block_data, current_index = self._parse_block_data(bit_string, current_index, end_index, mtype_properties, final_quant)

        # Create and return a Macroblock object
        macroblock = Macroblock(mba=mba, mtype=mtype, mquant=mquant, mvd=mvd, cbp=cbp, block_data=block_data)
        return macroblock, current_index, mba

    def _parse_mvd(self, bit_string, start_index, end_index):
        """
        Parse motion vector data (MVD) from the bitstream.
        """
        horizontal_mvd, current_index, clean_code = decode_vlc(bit_string, start_index, end_index, mvd_vlc_table)
        vertical_mvd, current_index, clean_code = decode_vlc(bit_string, current_index, end_index, mvd_vlc_table)
        return (horizontal_mvd, vertical_mvd), current_index

    def _parse_block_data(self, bit_string, start_index, end_index, mtype_properties, mquant):
        """
        Parse block data (e.g., transform coefficients) from the bitstream.
        """
        block_data = []
        current_index = start_index

        # Parse each block based on CBP and mtype
        for block_index in range(1, 7):  # H.261 has 6 blocks (4 Y, 1 Cb, 1 Cr)
            isIntra = "Intra" in mtype_properties["Prediction"]
            if isIntra or Block.block_contains_coeffs(mtype_properties["CBP"], block_index):
                block = Block(mtype=mtype_properties, quant=mquant, block_order=block_index)
                block_offset = block._parse_block(bit_string, current_index, end_index)
                block_data.append(block.tCoeffs64)
                current_index += block_offset

        return block_data, current_index
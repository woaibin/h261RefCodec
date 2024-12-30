# Macroblock parsing logic for the H.261 codec
import reconstruct_macro_block
from algorithm import decode_vlc, mba_vlc_table, mtype_vlc_table, mvd_vlc_table, cbp_vlc_table, check_mtype_properties
from block import Block


class Macroblock:
    def __init__(self, mba, mtype, mquant=None, mvd=None, cbp=None, block_data=None):
        """
        Initializes a Macroblock with the parsed values.
        """
        self.mba = mba
        self.mba_abs = -1
        self.mtype = mtype
        self.mquant = mquant
        self.mvd = mvd
        self.mv_abs = None
        self.cbp = cbp
        self.block_data = block_data
        self.enable_print = False

    def __str__(self):
        if not self.enable_print:
            return ""

        return "macroblock"

    def __repr__(self):
        return (f"Macroblock(mba={self.mba}, mtype={self.mtype}, mquant={self.mquant}, "
                f"mvd={self.mvd}, cbp={self.cbp}, block_data={self.block_data})")

    def should_ignore_prev_mvd(self):
        import ref_picture
        mba_abs = Macroblock.get_or_work_out_abs_mba(ref_picture.RefPicInterpreter.get_current_ref_macroblock())
        row_start = mba_abs == 1 or mba_abs == 12 or mba_abs == 23
        discontinue = self.mba != 1
        not_motion_compensation_mb = "MC" not in self.mtype
        if row_start or discontinue or not_motion_compensation_mb:
            return True
        else:
            return False

    def get_abs_motion_vector(self):
        import ref_picture
        # todo: check the three conds that the should ignore the prev mv of previous macro block:
        if self.mv_abs is None:
            if self.should_ignore_prev_mvd():
                temp_mv = [0, 0]
                temp_mvd = list(self.mvd)
                self.mv_abs = self.mvd
                if abs(temp_mvd[0][0]) <= 15:
                    temp_mv[0] = temp_mvd[0][0]
                else:
                    temp_mv[0] = temp_mvd[0][1]

                if abs(temp_mvd[1][0]) <= 15:
                    temp_mv[1] = temp_mvd[1][0]
                else:
                    temp_mv[1] = temp_mvd[1][1]

                self.mv_abs = temp_mv
            else:
                ref_pic = ref_picture.RefPicInterpreter.get_current_processing_pic()
                ref_mb = ref_picture.RefPicInterpreter.get_current_ref_macroblock()
                ref_mvd = ref_mb.frame.mb.get_abs_motion_vector()
                self.mv_abs = [0, 0]
                if abs(self.mvd[0][0] + ref_mvd[0]) <= 15:
                    self.mv_abs[0] = self.mvd[0][0] + ref_mvd[0]
                else:
                    self.mv_abs[0] = self.mvd[0][1] + ref_mvd[0]

                if abs(self.mvd[1][0] + ref_mvd[1]) <= 15:
                    self.mv_abs[1] = self.mvd[1][0] + ref_mvd[1]
                else:
                    self.mv_abs[1] = self.mvd[1][1] + ref_mvd[1]

        return self.mv_abs

    @staticmethod
    def get_or_work_out_abs_mba(current_process_mb_node):
        import ref_picture
        # print("self.mba: ", self.mba)
        # print("self.mba_abs: ", self.mba_abs)
        mb: Macroblock = current_process_mb_node.frame.mb
        if mb.mba_abs == -1 and mb.mba != 1:
            # exec work out proc:
            # 1. get current process pic:
            ref_mb = current_process_mb_node.prev
            mb.mba_abs = Macroblock.get_or_work_out_abs_mba(ref_mb) + mb.mba
            return mb.mba_abs

        elif mb.mba == 1:
            return mb.mba
        else:
            return mb.mba_abs

    def get_or_work_out_abs_mv(self):
        import ref_picture
        import reconstruct_macro_block
        if self.mv_abs is None:
            ref_macroblock: reconstruct_macro_block.ReconstructMacroBlock = ref_picture.RefPicInterpreter.get_current_ref_macroblock()
            self.mv_abs = self.mvd + ref_macroblock.get_mba_abs()
            return self.mba_abs
        else:
            return self.mba_abs


class MacroblockParser:
    def _parse_macroblock(self, bit_string, start_index, end_index, gquant):
        """
        Parse a macroblock from the bitstream.
        """
        current_index = start_index

        # Parse MBA (Macroblock Address) using VLC table
        # handle error ourselves
        mba, current_index, clean_code = decode_vlc(bit_string, current_index, end_index, mba_vlc_table, True)
        if str(mba) == "MBA stuffing" or str(mba) == "Start code":
            # stuffing next gob is coming, just return:
            return None, current_index, mba
        elif mba == -1:
            # check remaining bits:
            # in ffmpeg h261 encoder, it will insert align bits before encoding the picture header:
            if end_index - start_index <= 7:
                current_index += end_index - start_index
                return None, current_index, mba
            else:
                raise ValueError("wrong mba value......")

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
        mvd = ((0, 0), (0, 0))
        if mtype_properties["MVD"]:
            mvd, current_index = self._parse_mvd(bit_string, current_index, end_index)

        # Parse CBP (Coded Block Pattern) if indicated by MTYPE
        cbp = None
        if mtype_properties["CBP"]:
            cbp, current_index, clean_code = decode_vlc(bit_string, current_index, end_index, cbp_vlc_table)
            mtype_properties["CBPValue"] = cbp

        # Parse Block Data if indicated by MTYPE
        block_data = None
        final_quant = None
        if mquant == None:
            final_quant = gquant
        else:
            final_quant = mquant
        if mtype_properties["TCOEFF"]:
            block_data, current_index = self._parse_block_data(bit_string, current_index, end_index, mtype_properties,
                                                               final_quant)

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
        blocks = []
        current_index = start_index

        # Parse each block based on CBP and mtype
        for block_index in range(1, 7):  # H.261 has 6 blocks (4 Y, 1 Cb, 1 Cr)
            isIntra = "Intra" in mtype_properties["Prediction"]
            if isIntra or Block.block_contains_coeffs(mtype_properties["CBPValue"], block_index):
                block = Block(mtype=mtype_properties, quant=mquant, block_order=block_index)
                block_offset = block._parse_block(bit_string, current_index, end_index)
                blocks.append(block)
                current_index += block_offset

        return blocks, current_index

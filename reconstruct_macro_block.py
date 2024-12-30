import numpy as np
import reconstruct_block
import reconstruct_base
import reconstruct_picture
import ref_picture


class ReconstructMacroBlock:
    def __init__(self, mb):
        # Use numpy arrays to store data
        self.y_data = np.array([], dtype=np.int16)  # Y data as signed 8-bit integers
        self.u_data = np.array([], dtype=np.int16)  # U data as signed 8-bit integers
        self.v_data = np.array([], dtype=np.int16)  # V data as signed 8-bit integers
        self.mb = mb

    def go_reconstruction_macro_block(self, org_block: reconstruct_block.ReconstructBlock):
        print("------------------------------reconstruction: macroblock layer start---------------------------------")
        # for every macroblock, separate y, u, and v:
        if org_block.blockInterpreter.block_index < 0:
            print("wrong block index met in macro reconstruction")
            return

        # block 0-3 is luma blocks, 4 is u, 5 is v, all 8x8 (64-element arrays)
        reconstruct_data = np.array(org_block.reconstruct_data, dtype=np.int16)# Ensure data is signed 8-bit integers
        reconstruct_data = reconstruct_data.flatten()
        if org_block.blockInterpreter.block_index <= 3:
            self.y_data = np.concatenate((self.y_data, reconstruct_data))
        elif org_block.blockInterpreter.block_index == 4:
            self.u_data = np.concatenate((self.u_data, reconstruct_data))
        elif org_block.blockInterpreter.block_index == 5:
            self.v_data = np.concatenate((self.v_data, reconstruct_data))

        print("------------------------------reconstruction: macroblock layer end---------------------------------")


    def go_reconstruction_with_motion_compensation(self, ref_pic: ref_picture.RefPicInterpreter, mb):
        mv_abs = mb.get_abs_motion_vector()
        import macroblock
        print(f"--------------------------------mbAddr(abs): {mb.mba_abs}, mbAddr(related): {mb.mba}, mv_abs: {mv_abs}--------------------------------")
        motion_compensated_blks = reconstruct_base.MotionCompensation.apply_motion_compensation(mv_abs, ref_pic, mb)

        # Convert motion-compensated blocks to numpy arrays
        self.y_data = np.concatenate((self.y_data, np.array(motion_compensated_blks[0], dtype=np.int16)))
        self.y_data = np.concatenate((self.y_data, np.array(motion_compensated_blks[1], dtype=np.int16)))
        self.y_data = np.concatenate((self.y_data, np.array(motion_compensated_blks[2], dtype=np.int16)))
        self.y_data = np.concatenate((self.y_data, np.array(motion_compensated_blks[3], dtype=np.int16)))

        self.u_data = np.concatenate((self.u_data, np.array(motion_compensated_blks[4], dtype=np.int16)))
        self.v_data = np.concatenate((self.v_data, np.array(motion_compensated_blks[5], dtype=np.int16)))
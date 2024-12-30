import algorithm
import block
import reconstruct_base
import numpy as np

# for blocks to go reconstruction, they have to be motion compensated
class ReconstructBlock:
    def __init__(self, blockInterpreter: block.Block, index):
        self.blockInterpreter = blockInterpreter
        self.reconstruct_data = np.array([], dtype=np.int16)
        self.index = index

    def go_reconstruction(self):
        # invert zig-zag
        org_order_coeffs = reconstruct_base.InverseZigZagScanning(self.blockInterpreter.tCoeffs64).resume_original_order()

        #print("--------------------------------reconstruction: block layer start-----------------------------------")
        #print("layer index:" + str(self.blockInterpreter.block_index))
        # print("coeffs:")
        # columns = 8
        # for i in range(0, len(org_order_coeffs), columns):
        #     row = org_order_coeffs[i:i + columns]  # Get the next row (8 elements at a time)
        #     print(" ".join(f"{val:4}" for val in row))  # Format each value in the row to be 4 characters wide
        #print("--------------------------------reconstruction: block layer end-----------------------------------")

        #inverse quant:(this process has been
        #performed during the parsing of the block data, will move here in the future

        #idct:
        self.reconstruct_data = reconstruct_base.InverseDiscreteCosineTransform(org_order_coeffs).idct()

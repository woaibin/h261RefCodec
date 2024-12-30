import algorithm
import block
import reconstruct_macro_block
import ref_picture


class InverseQuantization:
    def __init__(self, quantization_parameter):
        """
        Initialize the InverseQuantization class with a quantization parameter.

        :param quantization_parameter: Quantization parameter used in the decoding process.
        """
        self.quantization_parameter = quantization_parameter

    def inverse_quantize(self, quantized_coefficients):
        """
        Perform inverse quantization on the given quantized DCT coefficients.

        :param quantized_coefficients: A list of quantized DCT coefficients.
        :return: A list of inverse-quantized DCT coefficients.
        """
        pass


class InverseZigZagScanning:
    def __init__(self, zig_zag_coeffs):
        """
        Initialize the InverseZigZagScanning class.
        """
        self.zig_zag_coeffs = zig_zag_coeffs

    def resume_original_order(self):
        """
        Convert a 1D array of quantized DCT coefficients back into a 2D block.

        :param quantized_block_1d: A 1D array of quantized DCT coefficients.
        :return: A 2D block (list of lists) of DCT coefficients in the correct zig-zag order.
        """
        original_coeff = [0] * 64
        for order, coeff in enumerate(self.zig_zag_coeffs):
            original_order = algorithm.zig_zag_order[order + 1] - 1  # +1 and -1 is the adjustment for the start index
            original_coeff[original_order] = coeff
        return original_coeff


class InverseDiscreteCosineTransform:
    def __init__(self, dct_coeffs):
        """
        Initialize the InverseDiscreteCosineTransform (IDCT) class.
        """
        self.dct_coeffs = dct_coeffs
        pass

    def idct(self):
        """
        Perform the Inverse Discrete Cosine Transform (IDCT) on a 2D block of DCT coefficients.

        :param dct_block: A 2D block (list of lists) of DCT coefficients.
        :return: A 2D block of pixel values in the spatial domain.
        """
        return algorithm.idct_2d(self.dct_coeffs, False)


class MotionCompensation:

    @staticmethod
    def apply_motion_compensation(motion_vector, reference_frame: ref_picture.RefPicInterpreter,
                                  mb):
        reconstruct_motion_compensation_blks = []
        # Traverse all blocks:
        current_mb_index = ref_picture.RefPicInterpreter.work_out_current_global_mb_index_in_2d_form()
        current_mb_index = ref_picture.RefPicInterpreter.work_out_current_global_mb_index_in_2d_form()

        current_ref_global_mb_index_2d = [a + b for a, b in
                                          zip(current_mb_index,
                                              motion_vector)]
        ref_mb_start_y = current_ref_global_mb_index_2d[1] * 64 * 4 + current_ref_global_mb_index_2d[0] * 64 * 4
        ref_mb_start_u = current_ref_global_mb_index_2d[1] * 64 + current_ref_global_mb_index_2d[0] * 64
        ref_mb_start_v = current_ref_global_mb_index_2d[1] * 64 + current_ref_global_mb_index_2d[0] * 64

        import reconstruct_picture
        if mb.block_data is not None:
            for counter, blockIt in enumerate(mb.block_data):
                real_block: block.Block = blockIt
                ref_pic: reconstruct_picture.ReconstructPicture = reference_frame.get_current_ref_pic()
                if not real_block.has_coeffs():
                    # residual, add up
                    if counter < 4:
                        ref_blk_data_y = ref_pic.get_data("y", ref_mb_start_y + counter * 64, 64)
                        block_complete_y = [x + y for x, y in zip(ref_blk_data_y, real_block.tCoeffs64)]
                        reconstruct_motion_compensation_blks.append(block_complete_y)
                    elif counter == 4:
                        ref_blk_data_u = ref_pic.get_data("u", ref_mb_start_u, 64)
                        block_complete_u = [x + y for x, y in zip(ref_blk_data_u, real_block.tCoeffs64)]
                        reconstruct_motion_compensation_blks.append(block_complete_u)
                    elif counter == 5:
                        ref_blk_data_v = ref_pic.get_data("y", ref_mb_start_v, 64)
                        block_complete_v = [x + y for x, y in zip(ref_blk_data_v, real_block.tCoeffs64)]
                        reconstruct_motion_compensation_blks.append(block_complete_v)
                else:
                    # just use the ref block:
                    if counter < 4:
                        ref_blk_data_y = ref_pic.get_data("y", ref_mb_start_y + counter * 64, 64)
                        reconstruct_motion_compensation_blks.append(ref_blk_data_y)
                    elif counter == 4:
                        ref_blk_data_u = ref_pic.get_data("u", ref_mb_start_u, 64)
                        reconstruct_motion_compensation_blks.append(ref_blk_data_u)
                    elif counter == 5:
                        ref_blk_data_v = ref_pic.get_data("y", ref_mb_start_v, 64)
                        reconstruct_motion_compensation_blks.append(ref_blk_data_v)
        else:
            # all empty, just use the ref blks:
            ref_pic: reconstruct_picture.ReconstructPicture = ref_picture.RefPicInterpreter.get_current_ref_pic().frame
            for i in range(6):
                # just use the ref block:
                if i < 4:
                    ref_blk_data_y = ref_pic.get_data("y", ref_mb_start_y + i * 64, 64)
                    reconstruct_motion_compensation_blks.append(ref_blk_data_y)
                elif i == 4:
                    ref_blk_data_u = ref_pic.get_data("u", ref_mb_start_u, 64)
                    reconstruct_motion_compensation_blks.append(ref_blk_data_u)
                elif i == 5:
                    ref_blk_data_v = ref_pic.get_data("y", ref_mb_start_v, 64)
                    reconstruct_motion_compensation_blks.append(ref_blk_data_v)

        return reconstruct_motion_compensation_blks

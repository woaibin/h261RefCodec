import algorithm
from algorithm import decode_vlc, vlc_table_tcoeff
import warnings

class Block:
    def __init__(self, mtype, quant, block_order, cbp=None):
        self.cbp = cbp
        self.mtype = mtype
        self.quant = quant
        self.tCoeffs64 = [0] * 64  # 64 coeffs
        self.block_order = block_order

    def calculate_rec(self, level, quant):
        """
        Calculate the reconstruction level (REC) based on the level and quant values.

        Parameters:
        - level: The coefficient level (can be positive, negative, or zero).
        - quant: The quantization parameter (ranges from 1 to 31).

        Returns:
        - REC: The reconstructed level, clipped to the range [-2048, 2047].
        """

        # Define the clipping range
        clip_min = -2048
        clip_max = 2047

        # Handle the case where level is zero
        if level == 0:
            return 0

        # Determine if QUANT is odd or even
        is_quant_odd = quant % 2 != 0

        # Apply the formulas based on the sign of the level and whether QUANT is odd or even
        if is_quant_odd:
            # QUANT is odd
            if level > 0:
                rec = quant * (2 * level + 1)
            else:  # level < 0
                rec = quant * (2 * level - 1)
        else:
            # QUANT is even
            if level > 0:
                rec = quant * (2 * level + 1) - 1
            else:  # level < 0
                rec = quant * (2 * level - 1) + 1

        # Clip the result to the range [-2048, 2047]
        rec = max(clip_min, min(clip_max, rec))

        return rec

    @staticmethod
    def block_contains_coeffs(cbp_value, block_index):
        """
        Determines if a given block contains coefficients based on the final CBP value.

        Parameters:
        - cbp_value: The final value from the formula (0 to 63).
        - block_index: The block index (1 to 6).

        Returns:
        - True if the block contains coefficients, False otherwise.
        """
        # Ensure block index is valid (1 to 6)
        if block_index < 1 or block_index > 6:
            raise ValueError("Block index must be between 1 and 6")

        # Shift the CBP value right by (6 - block_index) bits, then check if the least significant bit is 1
        return (cbp_value >> (6 - block_index)) & 1 == 1

    def _parse_block(self, bit_string, start_index, end_index):
        currentCoeffIdx = 0
        currentStrWalkThroughIdx = 0

        # decode the first element:
        if 'Intra' in self.mtype["Prediction"]:
            # if its an intra block, decode the first coeff as fixed 8 bits number:
            eightBitStr = bit_string[start_index: start_index + 8]
            firstCoeff = int(eightBitStr, 2)
            if firstCoeff == 255:
                firstCoeff = 128
            self.tCoeffs64[currentCoeffIdx] = firstCoeff
            currentCoeffIdx += 1
            currentStrWalkThroughIdx += 8
        else:
            # the doc says there're two tables, they only differs in EOB
            # when cbp is available, i.e. > 0, according to the doc, there cant be EOB mark inside it, cause there arent
            # any coeffs, so the block data does not exist. so we wont check for EOB for it, should regard it as the
            # value 1 with a 0 sign bit instead
            twoBitString = bit_string[start_index: start_index + 2]
            currentStrWalkThroughIdx += 2
            currentCoeffIdx += 1
            if twoBitString == "10":
                # positive 1:
                self.tCoeffs64[currentCoeffIdx] = 1
            elif twoBitString == "11":
                # negative 1:
                self.tCoeffs64[currentCoeffIdx] = -1
            else:
                currentStrWalkThroughIdx -= 2
                currentCoeffIdx -= 1

        # now we can traverse the vlc tables:
        # the first table is only for inter blocks
        while True:
            value, current_index, clean_code = decode_vlc(bit_string, start_index + currentStrWalkThroughIdx, end_index,
                                                          vlc_table_tcoeff)
            currentStrWalkThroughIdx += len(clean_code)

            run = None
            level = None

            inEscape = False
            if value[0] == "EOB":
                break
            elif value[0] == "Escape":
                inEscape = True
                # handle escape, run is a 6 bit fixed length code, level is an 8 bit fixed length code:
                run_bit_str = bit_string[start_index + currentStrWalkThroughIdx:start_index + currentStrWalkThroughIdx+6]
                level_bit_str = bit_string[start_index + currentStrWalkThroughIdx:start_index + currentStrWalkThroughIdx+6+8]
                currentStrWalkThroughIdx += 14
                run = int(run_bit_str, 2)
                level = int(level_bit_str, 2)

            # handle sign bit:
            if not inEscape:
                sign_bit_str = bit_string[start_index + currentStrWalkThroughIdx]
                sign_bit = int(sign_bit_str, 2)
                sign = 1
                if sign_bit == 0:
                    sign = 1
                elif sign_bit == 1:
                    sign = -1
                currentStrWalkThroughIdx += 1
                run = value[0]
                level = value[1]
                level = sign * level
            reconstructedLevel = self.calculate_rec(level, self.quant)
            self.tCoeffs64[currentCoeffIdx + run] = reconstructedLevel
            #currentCoeffIdx += run + 1

        # return how much len it has walked through:
        return currentStrWalkThroughIdx

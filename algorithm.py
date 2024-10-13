# VLC tables for MBA, MTYPE, MVD, and CBP
mba_vlc_table = {
    '1': 1,
    '011': 2,
    '010': 3,
    '0011': 4,
    '0010': 5,
    '0001 1': 6,
    '0001 0': 7,
    '0000 111': 8,
    '0000 110': 9,
    '0000 1011': 10,
    '0000 1010': 11,
    '0000 1001': 12,
    '0000 1000': 13,
    '0000 0111': 14,
    '0000 0110': 15,
    '0000 0101 11': 16,
    '0000 0101 10': 17,
    '0000 0101 01': 18,
    '0000 0101 00': 19,
    '0000 0100 11': 20,
    '0000 0100 10': 21,
    '0000 0100 011': 22,
    '0000 0100 010': 23,
    '0000 0100 001': 24,
    '0000 0100 000': 25,
    '0000 0011 111': 26,
    '0000 0011 110': 27,
    '0000 0011 101': 28,
    '0000 0011 100': 29,
    '0000 0011 011': 30,
    '0000 0011 010': 31,
    '0000 0011 001': 32,
    '0000 0011 000': 33,
    # Special codes
    '0000 0001 111': 'MBA stuffing',
    '0000 0000 0000 0001': 'Start code'
}

mtype_vlc_table = {
    '0001': 'Intra',                   # Intra
    '0000 001': 'Intra + MQUANT',       # Intra + MQUANT
    '1': 'Inter',                       # Inter
    '0000 1': 'Inter + MQUANT',         # Inter + MQUANT
    '0000 0000 1': 'Inter + MC',        # Inter + MC
    '0000 0001': 'Inter + MC + MQUANT', # Inter + MC + MQUANT
    '0000 0000 01': 'Inter + MC + MQUANT', # Inter + MC + MQUANT (alternate VLC)
    '001': 'Inter + MC + FIL',           # Inter + MC + FIL
    '01': 'Inter + MC + FIL',           # Inter + MC + FIL
    '0000 01': 'Inter + MC + FIL + MQUANT', # Inter + MC + FIL + MQUANT
}

mvd_vlc_table = {
    '0000 0011 001': (-16, 16),
    '0000 0011 011': (-15, 17),
    '0000 0011 101': (-14, 18),
    '0000 0011 111': (-13, 19),
    '0000 0100 001': (-12, 20),
    '0000 0100 011': (-11, 21),
    '0000 0100 11': (-10, 22),
    '0000 0101 01': (-9, 23),
    '0000 0101 11': (-8, 24),
    '0000 0111': (-7, 25),
    '0000 1001': (-6, 26),
    '0000 1011': (-5, 27),
    '0000 111': (-4, 28),
    '0001 1': (-3, 29),
    '0011': (-2, 30),
    '011': (-1,),
    '1': (0,),
    '010': (1,),
    '0010': (2, -30),
    '0001 0': (3, -29),
    '0000 110': (4, -28),
    '0000 1010': (5, -27),
    '0000 1000': (6, -26),
    '0000 0110': (7, -25),
    '0000 0101 10': (8, -24),
    '0000 0101 00': (9, -23),
    '0000 0100 10': (10, -22),
    '0000 0100 010': (11, -21),
    '0000 0100 000': (12, -20),
    '0000 0011 110': (13, -19),
    '0000 0011 100': (14, -18),
    '0000 0011 010': (15, -17)
}

cbp_vlc_table = {
    '111': 60,               # CBP = 60
    '1101': 4,               # CBP = 4
    '1100': 8,               # CBP = 8
    '1011': 16,              # CBP = 16
    '1010': 32,              # CBP = 32
    '1001 1': 12,            # CBP = 12
    '1001 0': 48,            # CBP = 48
    '1000 1': 20,            # CBP = 20
    '1000 0': 40,            # CBP = 40
    '0111 1': 28,            # CBP = 28
    '0111 0': 44,            # CBP = 44
    '0110 1': 52,            # CBP = 52
    '0110 0': 56,            # CBP = 56
    '0101 1': 1,             # CBP = 1
    '0101 0': 61,            # CBP = 61
    '0100 1': 2,             # CBP = 2
    '0100 0': 62,            # CBP = 62
    '0011 11': 24,           # CBP = 24
    '0011 10': 36,           # CBP = 36
    '0011 01': 3,            # CBP = 3
    '0011 00': 63,           # CBP = 63
    '0010 111': 5,           # CBP = 5
    '0010 110': 9,           # CBP = 9
    '0010 101': 17,          # CBP = 17
    '0010 100': 33,          # CBP = 33
    '0010 011': 6,           # CBP = 6
    '0010 010': 10,          # CBP = 10
    '0010 001': 18,          # CBP = 18
    '0010 000': 34,          # CBP = 34
    '0001 1111': 7,          # CBP = 7
    '0001 1110': 11,         # CBP = 11
    '0001 1101': 19,         # CBP = 19
    '0001 1100': 35,         # CBP = 35
    '0001 1011': 13,         # CBP = 13
    '0001 1010': 49,         # CBP = 49
    '0001 1001': 21,         # CBP = 21
    '0001 1000': 41,         # CBP = 41
    '0001 0111': 14,         # CBP = 14
    '0001 0110': 50,         # CBP = 50
    '0001 0101': 22,         # CBP = 22
    '0001 0100': 42,         # CBP = 42
    '0001 0011': 15,         # CBP = 15
    '0001 0010': 51,         # CBP = 51
    '0001 0001': 23,         # CBP = 23
    '0001 0000': 43,         # CBP = 43
    '0000 1111': 25,         # CBP = 25
    '0000 1110': 37,         # CBP = 37
    '0000 1100': 38,         # CBP = 38
    '0000 1011': 29,         # CBP = 29
    '0000 1010': 45,         # CBP = 45
    '0000 1001': 53,         # CBP = 53
    '0000 1000': 57,         # CBP = 57
    '0000 0111': 30,         # CBP = 30
    '0000 0110': 46,         # CBP = 46
    '0000 0101 1': 31,       # CBP = 31
    '0000 0101 0': 47,       # CBP = 47
    '0000 0100 1': 55,       # CBP = 55
    '0000 0100 0': 59,       # CBP = 59
    '0000 0011 1': 27,       # CBP = 27
    '0000 0011 0': 39,       # CBP = 39
}
# VLC table for TCOEFF as a Python dictionary
vlc_table_tcoeff = {
    '10': ('EOB', None),  # End of Block (EOB)

    '11s': (0, 1),  # The last occurrence of (0, 1) overwrites the earlier '1s'
    '0100s': (0, 2),
    '0010 1s': (0, 3),
    '0000 110s': (0, 4),
    '0010 0110s': (0, 5),
    '0010 0001s': (0, 6),
    '0000 0010 10s': (0, 7),
    '0000 0001 1101s': (0, 8),
    '0000 0001 1000s': (0, 9),
    '0000 0001 0011s': (0, 10),
    '0000 0001 0000s': (0, 11),
    '0000 0000 1101 0s': (0, 12),
    '0000 0000 1100 1s': (0, 13),
    '0000 0000 1100 0s': (0, 14),
    '0000 0000 1011 1s': (0, 15),

    '011s': (1, 1),
    '0001 10s': (1, 2),
    '0010 0101s': (1, 3),
    '0000 0011 00s': (1, 4),
    '0000 0001 1011s': (1, 5),
    '0000 0000 1011 0s': (1, 6),
    '0000 0000 1010 1s': (1, 7),

    '0101s': (2, 1),
    '0000 100s': (2, 2),
    '0000 0010 11s': (2, 3),
    '0000 0001 0100s': (2, 4),
    '0000 0000 1010 0s': (2, 5),

    '0011 1s': (3, 1),
    '0010 0100s': (3, 2),
    '0000 0001 1100s': (3, 3),
    '0000 0000 1001 1s': (3, 4),

    '0011 0s': (4, 1),
    '0000 0011 11s': (4, 2),
    '0000 0001 0010s': (4, 3),

    '0001 11s': (5, 1),
    '0000 0010 01s': (5, 2),
    '0000 0000 1001 0s': (5, 3),

    '0001 01s': (6, 1),
    '0000 0001 1110s': (6, 2),

    '0001 00s': (7, 1),
    '0000 0001 0101s': (7, 2),

    '0000 111s': (8, 1),
    '0000 0001 0001s': (8, 2),

    '0000 101s': (9, 1),
    '0000 0000 1000 1s': (9, 2),

    '0010 0111s': (10, 1),
    '0000 0000 1000 0s': (10, 2),

    '0010 0011s': (11, 1),
    '0010 0010s': (12, 1),
    '0010 0000s': (13, 1),
    '0000 0011 10s': (14, 1),
    '0000 0011 01s': (15, 1),
    '0000 0010 00s': (16, 1),
    '0000 0001 1111s': (17, 1),
    '0000 0001 1010s': (18, 1),
    '0000 0001 1001s': (19, 1),
    '0000 0001 0111s': (20, 1),
    '0000 0001 0110s': (21, 1),
    '0000 0000 1111 1s': (22, 1),
    '0000 0000 1111 0s': (23, 1),
    '0000 0000 1110 1s': (24, 1),
    '0000 0000 1110 0s': (25, 1),
    '0000 0000 1101 1s': (26, 1),

    '0000 01': ('Escape', None)
}
vlc_table_block_order = {
    1: 1, 2: 2, 6: 3, 7: 4, 15: 5, 16: 6, 28: 7, 29: 8,
    3: 9, 5: 10, 8: 11, 14: 12, 17: 13, 27: 14, 30: 15, 43: 16,
    4: 17, 9: 18, 13: 19, 18: 20, 26: 21, 31: 22, 42: 23, 44: 24,
    10: 25, 12: 26, 19: 27, 25: 28, 32: 29, 41: 30, 45: 31, 54: 32,
    11: 33, 20: 34, 24: 35, 33: 36, 40: 37, 46: 38, 53: 39, 55: 40,
    21: 41, 23: 42, 34: 43, 39: 44, 47: 45, 52: 46, 56: 47, 61: 48,
    22: 49, 35: 50, 38: 51, 48: 52, 51: 53, 57: 54, 60: 55, 62: 56,
    36: 57, 37: 58, 49: 59, 50: 60, 58: 61, 59: 62, 63: 63, 64: 64
}
# ESCAPE mode: Run fixed-length codes (6 bits)
escape_run_codes = {
    run: format(run, '06b')  # Convert run to a 6-bit binary string
    for run in range(64)  # Run values from 0 to 63
}

# ESCAPE mode: Level fixed-length codes (8 bits)
# Level range is from -128 to 127, but some values are forbidden
escape_level_codes = {}

# Forbidden codes (forbidden levels: -128, 0)
forbidden_levels = {-128, 0}

# Populate level codes
for level in range(-128, 128):
    if level in forbidden_levels:
        escape_level_codes[level] = "FORBIDDEN"
    else:
        escape_level_codes[level] = format((level + 256) % 256, '08b')  # Convert level to 8-bit signed binary

# New table to define the presence of MQUANT, MVD, CBP, and TCOEFF based on MTYPE VLC
mtype_properties_table = {
    '0001': {'MQUANT': False, 'MVD': False, 'CBP': False, 'TCOEFF': True, "Prediction": "Intra"},  # Intra
    '0000 001': {'MQUANT': True, 'MVD': False, 'CBP': False, 'TCOEFF': True, "Prediction": "Intra + MQUANT"},
    # Intra + MQUANT
    '1': {'MQUANT': True, 'MVD': False, 'CBP': True, 'TCOEFF': True, "Prediction": "Inter"},  # Inter
    '0000 1': {'MQUANT': True, 'MVD': False, 'CBP': True, 'TCOEFF': True, "Prediction": "Inter + MQUANT"},
    # Inter + MQUANT
    '0000 0000 1': {'MQUANT': False, 'MVD': True, 'CBP': False, 'TCOEFF': False, "Prediction": "Inter + MC"},
    # Inter + MC
    '0000 0001': {'MQUANT': False, 'MVD': True, 'CBP': True, 'TCOEFF': True, "Prediction": "Inter + MC + MQUANT"},
    # Inter + MC + MQUANT
    '0000 0000 01': {'MQUANT': True, 'MVD': True, 'CBP': True, 'TCOEFF': True, "Prediction": "Inter + MC + CBP + TCOEFF"},  # Inter + MC + CBP + TCOEFF
    '001': {'MQUANT': False, 'MVD': True, 'CBP': False, 'TCOEFF': False, "Prediction": "Inter + MC + CBP + TCOEFF"},
    '01': {'MQUANT': False, 'MVD': True, 'CBP': True, 'TCOEFF': True, "Prediction": "Inter + MC + FIL + MQUANT"},
    # Inter + MC + FIL + MQUANT
    '0000 01': {'MQUANT': True, 'MVD': True, 'CBP': True, 'TCOEFF': True,
                "Prediction": "Inter + MC + FIL + CBP + TCOEFF"},  # Inter + MC + FIL + CBP + TCOEFF
    # Add remaining MTYPE VLC codes and their corresponding property mappings
}


def decode_vlc(bit_string, start_index, end_index, vlc_table):
    """
    Decode a field encoded with Variable-Length Code (VLC).
    :param bit_string: The bitstream as a bit string.
    :param start_index: The current index in the bitstream.
    :param end_index: The end index for parsing.
    :param vlc_table: The VLC table to use for decoding.
    :return: The decoded value and the updated index.
    """
    current_index = start_index
    for code, value in vlc_table.items():
        # Remove spaces from the encoded VLC key if applicable
        if code is None:
            continue
        clean_code = code.replace(" ", "")
        clean_code = clean_code.replace("s", "") #remove sign mark, they are marked for telling u they exists
        if bit_string[current_index:current_index + len(clean_code)] == clean_code:
            current_index += len(clean_code)
            return value, current_index, clean_code
    raise ValueError("VLC code not found in the table")


def check_mtype_properties(vlc_code):
    """
    Check the presence of MQUANT, MVD, CBP, and TCOEFF for a given MTYPE VLC code.
    :param vlc_code: The VLC code for MTYPE.
    :return: A dictionary indicating the presence of MQUANT, MVD, CBP, and TCOEFF.
    """
    mtype_properties_table_clean = {
        key.replace(' ', ''): value for key, value in mtype_properties_table.items()
    }
    return mtype_properties_table_clean.get(vlc_code, None)

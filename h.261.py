# h261parser.py

import os
from picture import PictureParser


class H261Parser:
    """
    A parser for H.261 bitstreams to extract picture layers and group of blocks (GOBs).
    """

    def __init__(self, bitstream):
        self.bitstream = bitstream
        self.pictures = []  # List to store parsed Picture objects
        self.picture_parser = PictureParser()

    def _bitstream_to_bitstring(self):
        """
        Convert the byte stream to a string of bits for easier parsing.
        """
        return ''.join(f'{byte:08b}' for byte in self.bitstream)

    def parse(self):
        """
        Parse the bitstream to find picture start codes and extract picture layers.
        """
        bit_string = self._bitstream_to_bitstring()

        current_position = 0

        while True:
            start_index = bit_string.find(PictureParser.PICTURE_START_CODE, current_position)

            start_index += 20

            if start_index == -1:
                break

            # Parse the picture
            picture, next_index = self.picture_parser.parse(bit_string, start_index)

            # Add the picture to the list
            self.pictures.append(picture)

            # Move to the next position after the current start code
            current_position = next_index

        return self.pictures


# Accept file path input from the user
def get_file_bitstream():
    """
    Function to get a file path from the user, read the file, and return its content as a bytearray.
    """
    file_path = input("Enter the path to the bitstream file: ")

    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        return None

    try:
        with open(file_path, 'rb') as file:
            bitstream = bytearray(file.read())
        return bitstream
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


# Example usage:
def main():
    bitstream = get_file_bitstream()

    if bitstream:
        parser = H261Parser(bitstream)
        pictures = parser.parse()

        print("\nParsed Pictures:")
        for picture in pictures:
            print(picture)
    else:
        print("No valid bitstream provided.")


if __name__ == "__main__":
    main()
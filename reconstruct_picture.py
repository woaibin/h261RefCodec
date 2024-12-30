import reconstruct_gob
import numpy as np


class ReconstructPicture:
    def __init__(self, pic):
        self.y_data = np.array([], dtype=np.int16)
        self.u_data = np.array([], dtype=np.int16)
        self.v_data = np.array([], dtype=np.int16)
        self.pic = pic

    def go_reconstruction_gob(self, org_gob: reconstruct_gob.ReconstructGOB):
        print("------------------------------reconstruction: pic layer start---------------------------------")
        self.y_data = np.concatenate((self.y_data, org_gob.y_data))
        self.u_data = np.concatenate((self.u_data, org_gob.u_data))
        self.v_data = np.concatenate((self.v_data, org_gob.v_data))
        print("------------------------------reconstruction: pic layer end---------------------------------")

    def get_data(self, plane: str, start_index: int, length: int) -> bytearray:
        """
        Retrieve a specific range of bytes from the specified Y, U, or V plane.

        :param plane: The plane to retrieve data from ('y', 'u', or 'v').
        :param start_index: The starting index to retrieve data from.
        :param length: The number of bytes to retrieve.
        :return: A bytearray containing the requested data.
        :raises ValueError: If the plane is invalid or the range is out of bounds.
        """
        if plane == 'y':
            data = self.y_data
        elif plane == 'u':
            data = self.u_data
        elif plane == 'v':
            data = self.v_data
        else:
            raise ValueError("Invalid plane specified. Choose 'y', 'u', or 'v'.")

        if start_index < 0 or start_index + length > len(data):
            raise ValueError("Specified range is out of bounds.")

        return data[start_index:start_index + length]

    def dump_yuv(self, filename):
        """
        Dump the YUV 420 data to a .yuv file.

        :param filename: The name of the output file to write the YUV data.
        """
        with open(filename, 'wb') as f:
            # Write Y plane (width * height bytes)
            f.write(self.y_data)

            # Write U plane (width/2 * height/2 bytes)
            f.write(self.u_data)

            # Write V plane (width/2 * height/2 bytes)
            f.write(self.v_data)

        print(f"YUV data successfully dumped to {filename}.")
import reconstruct_macro_block
import numpy as np


class ReconstructGOB:
    def __init__(self, gob):
        self.y_data = np.array([], dtype=np.int16)
        self.u_data = np.array([], dtype=np.int16)
        self.v_data = np.array([], dtype=np.int16)
        self.gob = gob

    def go_reconstruction_gob(self, org_mg):
        #print("------------------------------reconstruction: gob layer start---------------------------------")
        self.y_data = np.concatenate((self.y_data, org_mg.y_data))
        self.u_data = np.concatenate((self.y_data, org_mg.u_data))
        self.v_data = np.concatenate((self.y_data, org_mg.v_data))
        #print("------------------------------reconstruction: gob layer start---------------------------------")

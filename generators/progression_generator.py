from utils.midilogger import *

class ProgressionGenerator:

    def __init__(self):
        self.define_constants()

    def define_constants(self):
        MODES = {
            'ION':['ION', 0, 2, 4, 5, 7, 9, 11],        # Ionian - (Major)
            'DOR':['DOR', 0, 2, 3, 5, 7, 9, 10],        # Dorian
            'PHR':['PHR', 0, 1, 3, 5, 7, 8, 10],        # Phrygian	 
            'LYD':['LYD', 0, 2, 4, 6, 7, 9, 11],        # Lydian
            'MIX':['MIX', 0, 2, 4, 5, 7, 9, 10],        # Mixolydian
            'AEO':['AEO', 0, 2, 3, 5, 7, 8, 10],        # Aeolian (Natural Minor)
            'LOC':['LOC', 0, 1, 3, 5, 6, 8, 10]         # Locrian
        }
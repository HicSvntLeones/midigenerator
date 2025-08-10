from utils.midilogger import *

# This generates a list of music commands from the inputed config and passes a list of events to the MetaEncoder.

class CommandGenerator:

    def __init__(self, settings):
        print(settings)
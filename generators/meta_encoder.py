from utils.midilogger import *

# This takes a list of commands from CommandGenerator and passes a list of events sorted by delta_time/track to a MidiEncoder.

class MetaEncoder:

    def write_header(self):
        pass
        

    def __init__(self, event_sheet, metadata):
        stamp(5, f"Initiated MetaEncoder with {metadata}")
        self.input_sheet = event_sheet
        self.metadata = metadata
        self.event_list = []

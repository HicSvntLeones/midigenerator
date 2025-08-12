from utils.midilogger import *

# This takes a list of events sorted by delta_time from the MetaEncoder, turns them into valid MIDI data and encodes into a midi.

class MidiEncoder:
    def __init__(self, event_lists, metadata):
        stamp(4, f"Initiated MidiEncoder with {metadata}")
        self.setup(event_lists, metadata)
        self.main()

    def setup(self, event_lists, metadata):
        self.event_lists = event_lists
        self.metadata = metadata
        self.hexdata = []
        stamp(4, f"MidiEncoder setup complete.")
        stamp(5, f"List of Events:{self.event_lists} across {self.metadata['track_count']+1} tracks.")

    def main(self):
        pass
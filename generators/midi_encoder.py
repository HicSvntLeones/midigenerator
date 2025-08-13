from utils.midilogger import *
from utils.midi_gen_funcs import int_to_hex
from utils.midi_gen_funcs import int_to_VLQ
from math import log2
from pathlib import Path

# This takes a list of event tuples sorted by delta_time from the MetaEncoder, turns them into valid MIDI data and encodes into a midi.

class MidiEncoder:
    def __init__(self, event_lists, metadata):
        stamp(4, f"Initiated MidiEncoder with {metadata}")
        self.setup(event_lists, metadata)
        self.main()

    def setup(self, event_lists, metadata):
        self.event_lists = event_lists
        self.metadata = metadata
        self.hexdata = []
        self.current_event = None
        self.current_track = None
        self.current_time = 0
        stamp(4, f"MidiEncoder setup complete.")
        stamp(5, f"List of Events:{self.event_lists} across {self.metadata['track_count']+1} tracks.")
        stamp(5, f"Metadata:{self.metadata}")

    def main(self):
        self.events_to_hex()
        stamp(4, f"Hex data completed: {self.hexdata}")
        self.create_concatenated_hex()
        self.write_midi()

    def create_concatenated_hex(self):
        self.to_write = ''.join([byte for track in self.hexdata for byte in track])
        stamp(5, f"Hex data concatenated: {self.to_write}")

    def write_midi(self):
        output_dir = Path(__file__).parent.parent / self.metadata['filepath'] 
        output_dir.mkdir(parents=True, exist_ok=True)
        write_midi = Path(__file__).parent.parent / self.metadata['filepath'] / self.metadata['filename']
        with open(write_midi, "wb") as file:
            file.write(bytes.fromhex(self.to_write))
        stamp(5, f"{self.metadata['filename']} created in {self.metadata['filepath']}")

    def events_to_hex(self):
        stamp(3, "Starting hex encoding...")
        for i in range(0, self.metadata['track_count']+1):
            self.encode_track(self.event_lists[i], i)

    def encode_track(self, event_list, track_no):
        stamp(4, f"Encoding track {track_no}...")
        stamp(5, f"... from list: {event_list}")
        self.current_track = track_no
        for event in event_list:
            self.current_event = event
            self.encode_event()
        stamp(5, f"Encoded track {track_no} with {self.hexdata[track_no]}")


    def encode_event(self):
        stamp(4, f"Encoding event type: {self.current_event[0]}")
        match self.current_event[0]:
            case "Control Change":
                self.handle_Control_Change()
            case "End Track":
                self.handle_End_Track()
            case "MThd":
                self.handle_event_MThd()
            case "MTrk":
                self.handle_event_MTrk()
            case "Note On":
                self.handle_event_Note_On()
            case "Note Off":
                self.handle_event_Note_Off()
            case "Program Change":
                self.handle_event_Program_Change()
            case "Set Tempo":
                self.handle_event_Set_Tempo()
            case "Set Time Signature":
                self.handle_event_Set_Time_Signature()
            case _:
                stamp(2, f"Unhandled event in encode_event {self.current_event}")

    def handle_Control_Change(self):
        stamp(5, f"... with parameters {self.current_event[1:]}")
        hex = []
        delta_time = self.delta_delta_time()
        hex = self.hexlist_append(hex, delta_time)
        status_byte = "B" + str(format(self.current_event[2], 'X'))
        controller = int_to_hex(self.current_event[3])
        value = int_to_hex(self.current_event[4])
        hex = self.hexlist_append(hex, status_byte)
        hex = self.hexlist_append(hex, controller)
        hex = self.hexlist_append(hex, value)
        self.hexdata[self.current_track] += hex
        stamp(5, f"Adding {hex} to sub-list of track {self.current_track}")

    def handle_End_Track(self):
        stamp(5, f"... with parameters {self.current_event[1:]}")
        hex = []
        END_TRACK = "00FF2F00"
        hex = self.hexlist_append(hex, END_TRACK)
        self.hexdata[self.current_track] += hex
        self.replace_MTrk_length()
        
    def handle_event_MThd(self):
        stamp(5, f"... with parameters {self.current_event[1:]}")
        hex = []
        MIDI_HEADER = "4D546864"
        HEADER_LENGTH = "00000006"
        FORMAT_TYPE = "0001" #Probably won't support other format types unless I get a reason to do so.
        track_count = int_to_hex(self.current_event[3]+1, 2) #Plus one because MIDI does not zero-index track count.
        division = int_to_hex(self.current_event[4], 2) #Only supports PPQN. Probably won't support SMPTE unless I get a reason to do so.
        hex = self.hexlist_append(hex, MIDI_HEADER)
        hex = self.hexlist_append(hex, HEADER_LENGTH)
        hex = self.hexlist_append(hex, FORMAT_TYPE)
        hex = self.hexlist_append(hex, track_count)
        hex = self.hexlist_append(hex, division)
        stamp(5, f"Appending {hex} to new sub-list of track 0") # Because MThd is always track 0, and always the first event.
        self.hexdata.append(hex)

    def handle_event_MTrk(self):
        stamp(5, f"... with parameters {self.current_event[1:]}")
        hex = []
        TRACK_HEADER = "4D54726B"
        TEMP_LENGTH = "ZZZZZZZZ" #This is a temporary (and invalid) length that will be easy to find later.
        hex = self.hexlist_append(hex, TRACK_HEADER)
        hex = self.hexlist_append(hex, TEMP_LENGTH)
        if self.current_track == 0: # If track 0, MTrk is not the start of the event list. On all other tracks, it is.
            stamp(5, f"Adding {hex} to track 0") 
            self.hexdata[0] += hex
            print(self.hexdata)
            return
        self.hexdata.append(hex)
        stamp(5, f"Adding {hex} to new sub-list of track {self.current_track}") 

    def handle_event_Note_On(self):
        stamp(5, f"... with parameters {self.current_event[1:]}")
        hex = []
        delta_time = self.delta_delta_time()
        hex = self.hexlist_append(hex, delta_time)
        status_byte = "9" + str(format(self.current_event[2], 'X'))
        pitch = int_to_hex(self.current_event[3])
        velocity = int_to_hex(self.current_event[4])
        hex = self.hexlist_append(hex, status_byte)
        hex = self.hexlist_append(hex, pitch)
        hex = self.hexlist_append(hex, velocity)
        self.hexdata[self.current_track] += hex
        stamp(5, f"Adding {hex} to sub-list of track {self.current_track}") 

    def handle_event_Note_Off(self):
        stamp(5, f"... with parameters {self.current_event[1:]}")
        hex = []
        delta_time = self.delta_delta_time()
        hex = self.hexlist_append(hex, delta_time)
        status_byte = "8" + str(format(self.current_event[2], 'X'))
        pitch = int_to_hex(self.current_event[3])
        velocity = int_to_hex(self.current_event[4])
        hex = self.hexlist_append(hex, status_byte)
        hex = self.hexlist_append(hex, pitch)
        hex = self.hexlist_append(hex, velocity)
        self.hexdata[self.current_track] += hex
        stamp(5, f"Adding {hex} to sub-list of track {self.current_track}") 
        
    def handle_event_Program_Change(self):
        stamp(5, f"... with parameters {self.current_event[1:]}")
        hex = []
        delta_time = self.delta_delta_time()
        hex = self.hexlist_append(hex, delta_time)
        status_byte = "C" + str(format(self.current_event[2], 'X'))
        program = int_to_hex(self.current_event[3])
        hex = self.hexlist_append(hex, status_byte)
        hex = self.hexlist_append(hex, program)
        self.hexdata[self.current_track] += hex
        stamp(5, f"Adding {hex} to sub-list of track {self.current_track}") 

    def handle_event_Set_Tempo(self):
        stamp(5, f"... with parameters {self.current_event[1:]}")
        hex = []
        delta_time = self.delta_delta_time()
        hex = self.hexlist_append(hex, delta_time)
        SET_TEMPO = "FF5103"
        tempo = int_to_hex(60000000/self.current_event[2],3)
        hex = self.hexlist_append(hex, SET_TEMPO)
        hex = self.hexlist_append(hex, tempo)
        self.hexdata[self.current_track] += hex
        stamp(5, f"Adding {hex} to sub-list of track {self.current_track}") 

    def handle_event_Set_Time_Signature(self):
        stamp(5, f"... with parameters {self.current_event[1:]}")
        hex = []
        delta_time = self.delta_delta_time()
        hex = self.hexlist_append(hex, delta_time)
        TIME_SIGNATURE = "FF5804"
        numerator = int_to_hex(self.current_event[2], 1) 
        denominator = int_to_hex(int(log2(self.current_event[3])), 1)
        clocks_per_tick = int_to_hex(self.current_event[4], 1)
        thirtyseconds_per_quarter = int_to_hex(self.current_event[5], 1)
        hex = self.hexlist_append(hex, TIME_SIGNATURE)
        hex = self.hexlist_append(hex, numerator)
        hex = self.hexlist_append(hex, denominator)
        hex = self.hexlist_append(hex, clocks_per_tick)
        hex = self.hexlist_append(hex, thirtyseconds_per_quarter)
        self.hexdata[self.current_track] += hex
        stamp(5, f"Adding {hex} to sub-list of track {self.current_track}") 


    def hexlist_append(self, array, string):
        if len(string)%2 != 0:
            stamp(2, "Invalid hex string.")
            return
        string_array = array + [string[i:i+2] for i in range(0, len(string), 2)]
        stamp(5, f"Updated {array} to {string_array}")
        return string_array
    
    def delta_delta_time(self):
        delta_time = self.current_event[1] - self.current_time
        self.current_time+=delta_time
        delta_time = int_to_VLQ(delta_time)
        return delta_time
    
    def replace_MTrk_length(self):
        stamp(5, f"Replacing length of track {self.current_track}")
        track_length = len(self.hexdata[self.current_track]) - 8
        plusheader = 0
        if self.current_track == 0:
            track_length -= 14 #Ignore the MIDI Header on track 0
            plusheader = 14
        stamp(5, f"Current track header {self.hexdata[self.current_track][0+plusheader:8+plusheader]}")
        hex_length = int_to_hex(track_length, 4)
        self.hexdata[self.current_track][4+plusheader:8+plusheader] = [hex_length[i:i+2] for i in range(0, len(hex_length), 2)]
        stamp(5, f"Appended track header {self.hexdata[self.current_track][0+plusheader:8+plusheader]}")

        
        
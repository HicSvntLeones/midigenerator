from utils.midilogger import *
from utils.midi_gen_funcs import *
from generators.meta_encoder import MetaEncoder

# Is used by the ProgressionGenerator to generate a list of music commands passes a list of events to the MetaEncoder.

class CommandGenerator:

    def __init__(self, midi_settings, command):
        stamp(5, f"Initilizing CommandGenerator.")
        self.setup(midi_settings)
        self.parse_command(command)
        self.main()
        
    def setup(self, midi_settings):
        self.midi_settings = midi_settings
        self.event_sheet = []
        self.track_count = 1 #Zero indexed, where 0 is the settings.
        self.metadata = {}
        self.metadata['name'] = ""
        self.metadata['instruments'] = "default"
        self.time_sig = (int(midi_settings['time_num']), int(midi_settings['time_den']))
        self.bpm = int(midi_settings['bpm'])
        self.ppq = int(midi_settings['ppq'])
        self.root_note = get_pitch(self.midi_settings['root_note'])
        self.current_time = (0,0.0)
        stamp(5, f"Setup CommandGenerator with {self.midi_settings}")

    def main(self):
        self.write_metadata()
        self.pass_to_meta_encoder(self.event_sheet, self.metadata)

    def write_metadata(self):
        stamp(5, "Writing metadata for command generator...")
        self.metadata['ppq'] = self.ppq
        self.metadata['bpm'] = self.bpm
        self.metadata['time_sig_num'] = self.time_sig[0]
        self.metadata['time_sig_den'] = self.time_sig[1]
        self.metadata['track_count'] = self.track_count
        stamp(5, f"Generate metadata: {self.metadata}")

    def pass_to_meta_encoder(self, event_sheet, metadata):
        meta_encoder = MetaEncoder(event_sheet, metadata)

    def parse_command(self, command):
        #'Command' is a tuple of an integer and a string.
        match command[0]:
            case 0: #Test commands
                match command[1]:
                    case '0':
                        #Test 5
                        self.test_generate_single_note()
                    case _:
                         stamp(2, f"Unmatched command, {command[1]} of {command}")
            case _:
                stamp(2, f"Unmatched command, {command[0]} of {command}")

    def advance_time(self, length):
        #Can be called as part of a note event to automatically set the current time to after that note ends.
        current_beat = self.current_time[1]
        current_bar = self.current_time[0]
        advance_amount = self.time_sig[1]/length
        current_beat+=advance_amount
        while current_beat >= self.time_sig[0]:
            current_beat -= self.time_sig[1]
            advance_amount -= self.time_sig[1]
            current_bar += 1
            stamp(5, f"Moved to next bar. Current bar {current_bar}, beat {current_beat}, {advance_amount} note length remains.")
        self.current_time = (current_bar, current_beat)

    def get_ppq_time(self, time = (0,0)):
        den_mult = 4/self.time_sig[1]
        ppq_time = time[0] * den_mult * self.ppq * self.time_sig[0]
        ppq_time += time[1] * den_mult * self.ppq
        return int(ppq_time)
    
    def get_ppq_length(self, length = 4):
        return int(1/length * 4 * self.ppq)
        
    def add_note(self, pitch = 60, length = 4, time = -1, velocity = 64, track = 1, channel = 0, advance = True):
        if time == -1:
            time = self.current_time
        note_entry = {
            'type':'note',
            'track':track,
            'channel':channel,
            'ppq_time':self.get_ppq_time(time),
            'time':time,
            'pitch':pitch,
            'length':length,
            'ppq_length':self.get_ppq_length(length),
            'velocity':velocity,
            'encoded':False
        }
        self.event_sheet.append(note_entry)
        if advance:
            self.advance_time(length)

    def test_generate_single_note(self):
        #Used for test 5.
        self.metadata['filename'] = "test_midi_02.mid"
        self.metadata['filepath'] = "assets/generated/tests/"
        self.add_note(pitch = self.root_note, length = 4)
        stamp(5, f"generated single note: {self.event_sheet}")
        




    
        

    




        
        

        
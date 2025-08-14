from utils.midilogger import *
from utils.midi_gen_funcs import *
from generators.meta_encoder import MetaEncoder

# Is used by the ProgressionGenerator to generate a list of music commands passes a list of events to the MetaEncoder.

class CommandGenerator:

    def __init__(self):
        stamp(5, f"Initilizing CommandGenerator.")
        #self.setup(midi_settings)
        #self.main()
        
    def setup(self, metadata):
        self.metadata = metadata
        self.event_sheet = []
        self.track_count = 1 #Zero indexed, where 0 is the settings.
        self.metadata['instruments'] = "default"
        self.time_sig = (4, 4)
        self.bpm = int(metadata['bpm'])
        self.ppq = int(metadata['ppq'])
        self.current_time = (0,0.0)
        stamp(5, f"Setup CommandGenerator with {self.metadata}")

    def run(self):
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
    
    def add_note(self, pitch = 60, length = 4, time = -1, velocity = 64, track = 1, channel = 0, advance = False):
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
        stamp(5, f"CommandGenerator added {note_entry} to event sheet")
        




    
        

    




        
        

        
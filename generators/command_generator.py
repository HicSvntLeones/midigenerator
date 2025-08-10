from utils.midilogger import *
from utils.midi_gen_funcs import *

# This generates a list of music commands from the inputed config and passes a list of events to the MetaEncoder.

class CommandGenerator:

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
        return ppq_time
        

    def add_note(self, pitch = 60, length = 4, time = -1, velocity = 64, track = 1, advance = True):
        if time == -1:
            time = self.current_time
        note_entry = {
            'type':'note',
            'track':track,
            'ppq_time':self.get_ppq_time(time),
            'time':time,
            'pitch':pitch,
            'length':length,
            'velocity':velocity
        }
        self.event_sheet.append(note_entry)
        if advance:
            self.advance_time(length)

    def generate_single_note(self):
        #Used for testing purposes.
        self.add_note(pitch = self.root_note, length = 4)
        stamp(5, f"generated single note: {self.event_sheet}")

    def __init__(self, midi_settings):
        self.midi_settings = midi_settings
        stamp(5, f"Initiated CommandGenerator with{self.midi_settings}")
        self.event_sheet = []
    
        self.time_sig = (int(midi_settings['time_num']), int(midi_settings['time_den']))
        self.bpm = int(midi_settings['bpm'])
        self.ppq = int(midi_settings['ppq'])
        self.root_note = get_pitch(self.midi_settings['root_note'])
        self.current_time = (0,0.0)
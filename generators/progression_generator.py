from utils.midilogger import *
from generators.command_generator import CommandGenerator

class ProgressionGenerator:

    def __init__(self):
        self.comgen = CommandGenerator()
        self.define_constants()
        self.def_dict = None
        self.generate_def_dict()
        self.prog_dicts = []
        self.command_dicts = []

    def define_constants(self):
        self.MODES = {
            'ION':['ION', 0, 2, 4, 5, 7, 9, 11],        # Ionian - (Major)
            'DOR':['DOR', 0, 2, 3, 5, 7, 9, 10],        # Dorian
            'PHR':['PHR', 0, 1, 3, 5, 7, 8, 10],        # Phrygian	 
            'LYD':['LYD', 0, 2, 4, 6, 7, 9, 11],        # Lydian
            'MIX':['MIX', 0, 2, 4, 5, 7, 9, 10],        # Mixolydian
            'AEO':['AEO', 0, 2, 3, 5, 7, 8, 10],        # Aeolian (Natural Minor)
            'LOC':['LOC', 0, 1, 3, 5, 6, 8, 10]         # Locrian
        }

        self.NOTES = {
            'Cb': -1, 'C':0, 'Cs':1, 
            'Db':1, 'D':2, 'Ds':3, 
            'Eb':3, 'E':4, 'Es':5, 
            'Fb':4, 'F':5, 'Fs':6, 
            'Gb':6, 'G':7, 'Gs':8, 
            'Ab':8,'A':9, 'As':10, 
            'Bb':10,'B':11, 'Bs':12 
        }

        self.PATTERNS = {
            'root':[{'time':(0,0), 'length':1, 'degree':1, 'velocity': 64}],
            'triad':[{'time':(0,0), 'length':1, 'degree':1, 'velocity': 64}, 
                     {'time':(0,0), 'length':1, 'degree':3, 'velocity': 64}, 
                     {'time':(0,0), 'length':1, 'degree':5, 'velocity': 64}],
        }
        self.DEFINITION_DICT_TEMPLATE = {
            'filepath': "",
            'filename': "",
            'def_string': None,
            'prog':None,
            'ppq': 960,
            'time_sig': (4,4),
            'prog_length': 0,
            'length': 4,
            'bpm':120
        }

        self.PROG_DICT_TEMPLATE = {
            'position':None, #Order of when this dict plays, integer
            'start_time':None, #Tuple of the starting bar/beat
            'root': ['C'], #List of root notes of each step in the progression
            'mode': ['ION'], #List of modes of each step in the progression
            'prog': ['I'], #List of chord degrees of each step in the progression
            'patterns':['triad'], #List of patterns included (multiple means they're layered)
            'octaves':[4] #List of octaves of the patters (integers)
        }

        self.COMMAND_DICT_TEMPLATE = { #turn this into straight up note and pass to the generator
            'root': 48,
            'mode': "ION",
            'degree':'I',
            'pattern':"triad"
        }

    def generate_def_dict(self):
        self.def_dict = self.DEFINITION_DICT_TEMPLATE.copy()

    def generate_prog_dict(self):
        return self.PROG_DICT_TEMPLATE.copy()

    def execute(self, arguments): #Entry point for most calls.
        print(f"Progression generator starting with arguments: {arguments}")
        self.handle_arguments(arguments)
        self.begin_main_process()

    def handle_arguments(self, arguments):
        if arguments == []:
            arguments = ['default']
        args = len(arguments)
        match arguments[0]:
            case "test":
                if args == 1:
                    print("Missing test number: Aborting.")
                else:
                    match arguments[1]:
                        case "1"|"one":
                            print("Running test 1...")
                            self.def_dict['def_string'] = "CION-I-VI-IV-V_"
                            self.def_dict['filename'] = "CION-I-VI-IV-V.mid"
                            self.def_dict['filepath'] = "assets/generated/tests"
                            stamp(5, f"Set defstring to {self.def_dict['def_string']}")
                        case _:
                            print("Unrecognized test number: Aborting.")
            
            case "default":
                print("Not finished yet, but this will be the default entry.")

            case _:
                print("Unrecognized argument: Aborting.")
        
    def begin_main_process(self):
        stamp(4, f"Beginning main procress with {self.def_dict}")
        self.read_def_string()
        self.generate_primary_dicts()
        self.comgen.setup(self.def_dict)

    def read_def_string(self):
        stamp(5, f"Processing defstring {self.def_dict['def_string']}")
        current_note = None
        current_mode = None
        prog_array = []
        current_prog = None
        expected_next = 'note'
        defarray = list(self.def_dict['def_string'])
        marker = 0
        array_length = len(defarray)
        while marker < array_length and defarray[marker] != '_':
            if expected_next == 'note':
                if defarray[marker+1] in {'b','s'}:
                    current_note = ''.join(defarray[marker:marker+2])
                    stamp(5, f"Note: {current_note}")
                    expected_next = 'mode'
                    marker+=2
                elif defarray[marker] in self.NOTES:
                    current_note = defarray[marker]
                    stamp(5, f"Note: {current_note}")
                    expected_next = 'mode'
                    marker+=1
                else:
                    stamp(2, f"Invalid note: {defarray[marker]}, skipping ahead.")
                    marker+=1
            if expected_next == 'mode':
                if ''.join(defarray[marker:marker+3]) in self.MODES:
                    current_mode = ''.join(defarray[marker:marker+3])
                    stamp(5, f"Mode: {current_mode}")
                    marker +=3
                    expected_next = 'prog'
                else:
                    stamp(2, f"Invalid mode: {defarray[marker]}, skipping ahead.")
                    marker+=1
            if expected_next == 'prog':
                if defarray[marker] == '-':
                    marker += 1
                    scan = 0
                    while defarray[marker+scan] in {'I', 'V'}:
                        scan+=1
                    current_prog = ''.join(defarray[marker:marker+scan])
                    stamp(5, f"Prog: {current_prog}")
                    prog_array.append((current_note, current_mode, current_prog))
                    expected_next = 'prog'
                    marker+=scan
                else:
                    stamp(5, f"Not prog {defarray[marker]} looping back to note.")
                    expected_next = 'note'
        self.def_dict['prog'] = prog_array
        self.def_dict['prog_length'] = len(prog_array)
        self.def_dict['length'] = len(prog_array)*8
        stamp(4, f"Finished writing prog array to def_dict: {self.def_dict['prog']}, length {self.def_dict['prog_length']}")

    def generate_primary_dicts(self):
        stamp(4, "Generating primary dicts.")
        for i in range (0, 4):
            new_dict = self.generate_prog_dict()
            note_array, mode_array, prog_array = [], [], []
            new_dict['position'] = i
            new_dict['start_time'] = (i,0)
            for j in range (0, self.def_dict['prog_length']):
                note_array.append(self.def_dict['prog'][j][0])
                mode_array.append(self.def_dict['prog'][j][1])
                prog_array.append(self.def_dict['prog'][j][2])
            new_dict['root'] = note_array
            new_dict['mode'] = mode_array
            new_dict['prog'] = prog_array
            self.prog_dicts.append(new_dict)
        self.prog_dicts[0]['pattern'] = ['triad']
        self.prog_dicts[0]['octave'] = [4]
        self.prog_dicts[1]['pattern'] = ['root','scale']
        self.prog_dicts[1]['octave'] = [4, 3]
        self.prog_dicts[2]['pattern'] = ['maj7']
        self.prog_dicts[2]['octave'] = [4]
        self.prog_dicts[3]['pattern'] = ['arp']
        self.prog_dicts[3]['octave'] = [4]
        stamp(5, f"Prog dicts stack is now: {self.prog_dicts}")

from utils.midilogger import stamp
from generators.progression_generator import ProgressionGenerator
from random import randint
from random import choice

#This generates a defstring and passes it to the Progression Generator

class DefstringGenerator:

    def __init__(self):
        self.define_constants()
        prog_gen = ProgressionGenerator()
        self.prog_gen = prog_gen
        self.set_default_gen_settings()
        self.gen_settings = self.gen_setting_dicts['basic']
        self.note_dicts = {}
        self.generate_note_dicts()
        self.similarity_dicts = {}
        self.generate_defstring()
        self.set_metadata()
        self.prog_gen.def_dict.update(self.metadata)
        self.prog_gen.begin_main_process()

    def set_metadata(self):
        self.metadata = {
            'version': 'rev1',
            'filepath': 'assets/generated/rev1',
            'def_string':self.defstring,
            'filename': f"{self.defstring}.mid"
        }

    def set_default_gen_settings(self):
        self.gen_setting_dicts = {}
        self.gen_setting_dicts['basic'] = {
            'gentype':'basic',
            'min_prog_length': 4,
            'max_prog_length': 10,
            'mode_change_chance':20,
            'root_change_chance':20,
            'mode_change_increase':0,
            'root_change_increase':0,
            'weighting':'unweighted',
            'current_root':None,
            'current_mode':None,
            'current_prog':None,
            'root_changes':['random'],
            'mode_changes':['random'],
            'prog_changes':['random'],
            'all_changes':['random']
        }

    def generate_note_dicts(self):
        for i, note in enumerate(self.prog_gen.PITCHES):
                for j, mode in enumerate(self.prog_gen.MODES):
                    key = f"{self.prog_gen.PITCHES[i]}{mode}"
                    notes = []
                    for k, pitch in enumerate(self.prog_gen.MODES[mode][1:]):
                        notes.append(self.prog_gen.PITCHES[(note+pitch)%12])
                    self.note_dicts[key] = notes
        stamp(4, "Note dicts written.")

    def generate_similarity_dict(self, key):
        self.similarity_dicts[key] = {}
        base = self.note_dicts[key]
        for i, scale in enumerate(self.note_dicts):
            diff = 0
            for j, note in enumerate(self.note_dicts[scale]):
                if note in base:
                    diff +=1
            self.similarity_dicts[key][scale] = diff
        stamp(4, f"Generated similarity report for {key}")
        stamp(5, self.similarity_dicts[key])

    def mutate_all(self):
        stamp(5, "Mutating all.")
        if self.gen_settings['current_root'] == None:
            return self.mutate_all_random()
        roll =  choice(self.gen_settings['all_changes'])
        match roll:
            case 'random':
                return self.mutate_all_random()
            case _:
                stamp(2, f"Unmatched mutate_all case {roll}")
                return
       
    def mutate_all_random(self):
        root_note = self.gen_settings['current_root'] = self.read_weighted_dict(self.PITCHES['unweighted'])
        mode = self.gen_settings['current_mode'] = self.read_weighted_dict(self.MODES['unweighted'])
        prog = self.gen_settings['current_prog'] = self.read_weighted_dict(self.DEGREES['unweighted'])
        self.generate_similarity_dict(f"{root_note}{mode}")
        stamp(4, f"Root note set to {root_note}, mode {mode}, prog {prog}")
        return f"{root_note}{mode}-{prog}"


    def mutate_root(self):
        stamp(5, "Mutating root.")
        roll =  choice(self.gen_settings['root_changes'])
        match roll:
            case 'random':
                return self.mutate_root_random()
            case _:
                stamp(2, f"Unmatched mutate_all case {roll}")
                return
    
    def mutate_root_random(self):
        root_note = self.gen_settings['current_root'] = self.read_weighted_dict(self.PITCHES['unweighted'])
        mode = self.gen_settings['current_mode']
        prog = self.gen_settings['current_prog']
        self.generate_similarity_dict(f"{root_note}{mode}")
        stamp(4, f"Root note set to {root_note}, mode {mode}, prog {prog}")
        return f"{root_note}{mode}-{prog}"

    def mutate_mode(self):
        stamp(5, "Mutating mode.")
        roll =  choice(self.gen_settings['mode_changes'])
        match roll:
            case 'random':
                return self.mutate_mode_random()
            case _:
                stamp(2, f"Unmatched mutate_all case {roll}")
                return
            
    def mutate_mode_random(self):
        root_note = self.gen_settings['current_root']
        mode = self.gen_settings['current_mode'] = self.read_weighted_dict(self.MODES['unweighted'])
        prog = self.gen_settings['current_prog']
        self.generate_similarity_dict(f"{root_note}{mode}")
        stamp(4, f"Root note set to {root_note}, mode {mode}, prog {prog}")
        return f"{root_note}{mode}-{prog}"

    def mutate_prog(self):
        stamp(5, "Mutating prog.")
        roll =  choice(self.gen_settings['prog_changes'])
        match roll:
            case 'random':
                return self.mutate_prog_random()
            case _:
                stamp(2, f"Unmatched mutate_all case {roll}")
                return
            
    def mutate_prog_random(self):
        prog = self.gen_settings['current_prog'] = self.read_weighted_dict(self.DEGREES['unweighted'])
        stamp(4, f"Prog set to {prog}")
        return f"-{prog}"
    
    def generate_defstring(self):
        weighting = self.gen_settings['weighting']
        length_goal = randint(self.gen_settings['min_prog_length'],self.gen_settings['max_prog_length'])
        length = 0
        spree = 0
        stamp(5, f"Target length {length_goal}")
        self.gen_state = 'all'
        defstring = ''
        while length_goal > length:
            match self.gen_state:
                case 'all':
                    defstring += self.mutate_all()
                    self.gen_state = self.roll_genstate(spree)
                    length +=1
                    spree = 0
                case 'mode':
                    defstring += self.mutate_mode()
                    self.gen_state = self.roll_genstate(spree)
                    length +=1
                    spree = 0
                case 'note':
                    defstring += self.mutate_root()
                    self.gen_state = self.roll_genstate(spree)
                    length +=1
                    spree = 0
                case 'prog':
                    defstring += self.mutate_prog()
                    self.gen_state = self.roll_genstate(spree)
                    length +=1
                    spree +=1
                case _: 
                    stamp(2, f"Unmatched gen_state. {self.gen_state}")
                    break
            stamp(5, f"defstring: {defstring}")
        defstring += "_"
        self.defstring = defstring
        stamp(4, "defstring ready")

    def roll_genstate(self, spree):
        stamp(5, f"Rolling genstate with spree {spree}")
        new_root = randint(0,100) <= self.gen_settings['root_change_chance']+(self.gen_settings['root_change_increase']*spree)
        new_mode = randint(0,100) <= self.gen_settings['mode_change_chance']+(self.gen_settings['mode_change_increase']*spree)
        if new_root and new_mode:
            return 'all'
        if new_root:
            return 'note'
        if new_mode:
            return 'mode'
        return 'prog'
        
    def read_weighted_dict(self, dictionary):
        total = 0
        counter = 0
        for key in dictionary:
            total += dictionary[key]
        counter = randint(1,total)
        for key in dictionary:
            counter -= dictionary[key]
            if counter <= 0:
                return key

    def define_constants(self): #Change these into dicts of dicts
        self.DEGREES = {}
        self.DEGREES['unweighted'] = {
            'I':1, 'II':1, 'III':1, 'IV':1, 'V':1, 'VI':1, 'VII':1
        }
        self.MODES= {}
        self.MODES['unweighted'] = {
            'ION':1, 'DOR':1, 'PHR':1, 'LYD':1, 'MIX':1, 'AEO':1, 'LOC':1
        }
        self.PITCHES = {}
        self.PITCHES['unweighted'] = {
            'C':1, 'Cs':1, 'D':1, 
            'Ds':1, 'E':1, 'F':1,
            'Fs':1, 'G':1, 'Gs':1,
            'A':1, 'As':1, 'B':1,
        }
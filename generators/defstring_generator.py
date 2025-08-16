from utils.midilogger import stamp
from generators.progression_generator import ProgressionGenerator

#This generates a defstring and passes it to the Progression Generator

class DefstringGenerator:

    def __init__(self):
        self.metadata = {}
        self.metadata['version'] = 'rev1'
        prog_gen = ProgressionGenerator()
        self.prog_gen = prog_gen
        self.set_default_gen_settings()
        self.note_dicts = {}
        self.generate_note_dicts()
        self.similarity_dicts = {}
        self.generate_similarity_dict('CsLOC')


    def set_default_gen_settings(self):
        self.gen_settings = {}
        self.gen_settings['basic'] = { 
            'min_prog_length': 4,
            'max_prog_length': 10,
            'mode_change_chance':0,
            'root_change_chance':0
        }

    def generate_note_dicts(self):
        for i, note in enumerate(self.prog_gen.PITCHES):
                for j, mode in enumerate(self.prog_gen.MODES):
                    stamp(5, f"Generating note dict for {self.prog_gen.PITCHES[i]}{mode}")
                    key = f"{self.prog_gen.PITCHES[i]}{mode}"
                    notes = []
                    for k, pitch in enumerate(self.prog_gen.MODES[mode][1:]):
                        notes.append(self.prog_gen.PITCHES[pitch])
                    self.note_dicts[key] = notes
        stamp(4, "Note dicts written.")

    def generate_similarity_dict(self, key):
        self.similarity_dicts[key] = {}
        base = self.note_dicts[key]
        print(base)
        for i, scale in enumerate(self.note_dicts):
            diff = 7
            for j, note in enumerate(self.note_dicts[scale]):
                if note in base:
                    diff -=1
                    print(diff)
            self.similarity_dicts[key][scale] = diff
        print(self.similarity_dicts[key])
            
         
        

    def generate_defstring(self):
        pass

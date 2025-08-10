from pathlib import Path
from utils.midilogger import stamp
from utils.midi_read_funcs import *
from generators.command_generator import *

def midi_test_1():
    try:
        read_test = Path(__file__).parent / 'assets' / 'static' / "read_test.mid"
        with open(read_test, 'rb') as midi_r:
            data = midi_r.read()
    except:
        raise Exception("Problem opening test MIDI. May not exist or filepath changed.")
    hex_data = data.hex().upper()
    expected_result = "4D546864000000060001000203E84D54726B0000001300FF510307A12000FF58040402180800FF2F004D54726B0000002600FF030E41636F7573746963205069616E6F00B0000000C0000090306E876880300000FF2F00"
    print(f"Test midi:{hex_data}")
    print(f"Expected: {expected_result}")
    if hex_data == expected_result:
        print("Test success.")
    else:
        print("Data mismatch.")

def midi_test_2():
    test_midi_data = "4D546864000000060001000203E84D54726B0000001300FF510307A12000FF58040402180800FF2F004D54726B0000002600FF030E41636F7573746963205069616E6F00B0000000C0000090306E876880300000FF2F00"
    try:
        write_test = Path(__file__).parent / 'assets' / 'generated' / 'tests' / "test_midi_01.mid"
        with open(write_test, "wb") as file:
            file.write(bytes.fromhex(test_midi_data))
    except:
        raise Exception("Problem generating test MIDI.")
    if write_test:
        print("File (re)generated.")
    else:
        print("File generation failed.")

def midi_test_4():
    print("Expecting True True False.")
    print(slice_match([1, 2, 3, 4], 1, [1, 2, 3, 4, 5, 6, 7], 1, 3))
    print(slice_match([3,6,2,7,4,7,4,7,3,7,4], 2, [2,7,4,7,6,4,6,7,3], 0, 4))
    print(slice_match([3,4,7,3,8,3,7], 1, [5,8,2,6,4,8,3,2,6,7], 2, 3))

def midi_test_3():
    midi_filepath = Path(__file__).parent / 'assets' / 'static' / "read_test.mid"
    results = disambiguate_midi(midi_filepath)
    print(*results, sep='\n')

def midi_test_5(midi_settings):
    comgen = CommandGenerator(midi_settings)
    comgen.generate_single_note()
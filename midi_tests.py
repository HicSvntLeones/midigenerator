from pathlib import Path
from midilogger import stamp

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
        stamp(5, "Success.")
    else:
        print("Data mismatch.")
        stamp(3, "Data mismatch.")

def midi_test_2():
    test_midi_data = "4D546864000000060001000203E84D54726B0000001300FF510307A12000FF58040402180800FF2F004D54726B0000002600FF030E41636F7573746963205069616E6F00B0000000C0000090306E876880300000FF2F00"
    write_test = Path(__file__).parent / 'assets' / 'generated' / 'tests' / "test_midi_01.mid"
    with open(write_test, "wb") as file:
        file.write(bytes.fromhex(test_midi_data))
    if write_test:
        print("File (re)generated.")
        stamp(5, "Success?")
    else:
        print("File generation failed.")
        stamp(3, "File generation failure.")
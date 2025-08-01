def test_write_c(): # Confirmed to work on ToneJS at least. Actual programs do not like.
    hex_data = (
    "4D546864000000060000000101E0"  # Header chunk: format 0, 1 track, 480 ticks/qn
    "4D54726B0000002F"              # Track chunk header (47 bytes)
    "00FF510307A120"                # Tempo: 120 BPM
    "00C000"                        # Program Change: channel 0, piano
    "00903064"                      # Note On: C3 (note 48), velocity 100
    "8360803040"                    # Delta 480 ticks, Note Off: C3, velocity 64
    "00FF2F00"                      # End of track
    )
    print(f"Writing: {hex_data}")
    with open("testdata/test_c32.mid", "wb") as f:
        f.write(bytes.fromhex(hex_data))

def print_raw_hex(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    # Convert bytes to hex string, uppercase, spaced by two chars for readability
    hex_string = data.hex().upper()
    spaced_hex = ' '.join(hex_string[i:i+2] for i in range(0, len(hex_string), 2))
    print(spaced_hex)
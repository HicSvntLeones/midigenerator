from midilogger import stamp

def midi_to_hex_array(filepath):
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
    except:
        raise Exception("Problem opening test MIDI. May not exist or filepath changed.")
    if not data:
        stamp(2, "MIDI reading failed, returning.")
        return
    hex_string = data.hex().upper()
    hex_array = (' '.join(hex_string[i:i+2] for i in range(0, len(hex_string), 2))).split()
    stamp(4, "Hex array generated.")
    stamp(5, f"Array:{hex_array}")
    return hex_array

def read_hex(hex_array, scan_pos, n=1):
    if len(hex_array) >= scan_pos+n:
        read = hex_array[scan_pos:scan_pos+n]
        stamp(5, f"Read:{read}")
        return read
    stamp(2, "Array out of bounds.")

def pop_hex(hex_array, scan_pos, n=1):
    if len(hex_array) >= scan_pos+n:
        pop = hex_array[scan_pos:scan_pos+n]
        scan_pos += n
        stamp(5, f"Popped:{pop}")
        return pop, scan_pos
    stamp(2, "Array out of bounds.")

def disambiguate_timing(hexes):
    time_type = None
    midi_PPQN = None
    midi_FPS = None
    midi_TPS = None
    byte1 = int(hexes[0], 16)
    byte2 = int(hexes[1], 16)
    signed_byte1 =  byte1 if byte1 < 128 else byte1 - 256

    if signed_byte1 >= 0:
        time_type = "PPQN"
    else:
        time_type = "SMPTE"
    
    match time_type:
        case "PPQN":
            midi_PPQN = (byte1 << 8) + byte2
            stamp(5, f"PPQN: {midi_PPQN}")
        case "SMPTE":
            match signed_byte1:
                case -29:
                    midi_FPS = 29.97
                case _:
                    midi_FPS = -signed_byte1
            midi_TPS = byte2
            stamp(5, f"FPS: {midi_FPS}")
            stamp(5, f"TPS: {midi_TPS}")
        case _: 
            stamp(2,"Time Type Mismatch")
    return time_type, midi_PPQN, midi_FPS, midi_TPS



def disambiguate_header(hex_array, scan_pos, desc_array):
    #Header Marker
    popped, scan_pos = pop_hex(hex_array, scan_pos, 4)
    if popped != ['4D', '54', '68', '64']:
        stamp(2,"Header chunk mismatch: MThd")
        return
    
    #Header Length
    popped, scan_pos = pop_hex(hex_array, scan_pos, 4)
    if popped != ['00', '00', '00', '06']:
        stamp(2,"Header chunk mismatch: Length")
        return
    
    #Midi Format
    popped, scan_pos = pop_hex(hex_array, scan_pos, 1)
    if popped != ['00']:
        stamp(2,"Header chunk mismatch: Format Byte 1")
        return
    popped, scan_pos = pop_hex(hex_array, scan_pos, 1)
    if int(popped[0]) > 2:
        stamp(2,"Header chunk mismatch: Format Byte 2")
        return
    midi_format_type = int(popped[0])
    stamp(5, f"Format:{midi_format_type}")

    #Track Count
    popped, scan_pos = pop_hex(hex_array, scan_pos, 2)
    track_count = int(''.join(popped), 16)
    stamp(5, f"MTrk Count:{track_count}")

    #Timing/Tick Rate (PPQN/SMPTE)
    popped, scan_pos = pop_hex(hex_array, scan_pos, 2)
    time_type, midi_PPQN, midi_FPS, midi_TPS = disambiguate_timing(popped)
    stamp(4,f"Header chunk completed with: {midi_format_type}, {track_count}, {time_type}, {midi_PPQN}, {midi_FPS}, {midi_TPS}")
    
    desc_array.append((1, midi_format_type, track_count, time_type, midi_PPQN, midi_FPS, midi_TPS))
    return scan_pos, desc_array

def slice_match(array_1, index_1, array_2, index_2, comp_length):
    matching = True
    if matching:
        for i in range (0, comp_length):
            if array_1[index_1+i] != array_2[index_2+i]:
                matching = False
    return matching


def validate_body(hex_array, scan_pos, desc_array):
    array_length = len(hex_array)
    header_count = 0
    end_track_count = 0
    stamp(4, f"Validating body with track count of {desc_array[0][2]}")
    while end_track_count < desc_array[0][2]:
        if scan_pos >= array_length:
            return False
        stamp(5, f"Checking for match at {scan_pos}")
        if slice_match(hex_array, scan_pos, ["4D","54","72","6B"], 0, 4):
            header_count += 1
            stamp(5, f"Track header at {scan_pos}")
            popped, scan_pos = pop_hex(hex_array, scan_pos+4, 4)
            stamp(5, f"Track length hex {popped}")
            track_length = int(''.join(popped), 16)
            stamp(5, f"Track length {track_length}")
            scan_pos +=track_length-4
            stamp(5, f"Checking for match at {scan_pos}")
            if slice_match(hex_array, scan_pos+1, ["FF","2F","00"], 0, 3):
                end_track_count += 1
                stamp(5, f"Track end at {scan_pos}")
                scan_pos += 4
            else: 
                stamp(2, f"Expected track end, got {read_hex(hex_array, scan_pos+1, 3)} at position {scan_pos}. Likely malformed MIDI, aborting.")
                return False
    if desc_array[0][2] != end_track_count != header_count:
        return False
    stamp(4, f"Body validated with ({header_count},{end_track_count},{desc_array[0][2]}), all three integers should match.")
    return True


def disambiguate_body(hex_array, scan_pos, desc_array):
    pass


def disambiguate_midi(filepath):
    hex_array = midi_to_hex_array(filepath)
    desc_array = []
    scan_pos = 0
    scan_pos, desc_array = disambiguate_header(hex_array, scan_pos, desc_array)
    if not validate_body(hex_array, scan_pos, desc_array):
        pass

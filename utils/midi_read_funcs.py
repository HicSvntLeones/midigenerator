from utils.midilogger import stamp

#In retrospect, all of this might have been easier to define within a class, but I wasn't expecting this to end up as large as it did. Oh well.
#For the moment, this doesn't (or probably won't) play nice with midi's that have multiple tracks that play in parralel. 
#As this isn't meant to be a full parser, only a debugging tool for my other uses, I probably won't add this functionality.

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

def read_VLQ(hex_array, scan_pos):
    stamp(5, f"Reading VLQ from {scan_pos}")
    total = 0
    byte_count = 0
    end_bit = False
    while end_bit == False:
        byte_count += 1
        popped, scan_pos = pop_hex(hex_array, scan_pos)
        val = int(popped[0],16)
        if val >= 128:
            val-=128
        else:
            end_bit = True
        total =+ val
    stamp(5, f"VLQ resolved: {byte_count} byte(s) with value {total}.")
    return total, scan_pos

def read_hex_as_ascii(hex_array, scan_pos, length):
    string_array = []
    popped, scan_pos = pop_hex(hex_array, scan_pos, length)
    string = ''.join(chr(int(h, 16)) for h in popped)
    stamp(5, f"String read from hex as '{string}'")
    return string, scan_pos



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
    
    desc_array.append((1, midi_format_type, track_count, time_type, midi_PPQN, midi_FPS, midi_TPS, "<MIDI file header>"))
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

def disambiguate_4D(hex_array, scan_pos, desc_array):
    if slice_match(hex_array, scan_pos, ["4D", "54", "72", "6B"], 0, 4):
        popped, scan_pos = pop_hex(hex_array, scan_pos+4, 4) #Since the file has already been validated, skipping right to the length is ok.
        track_length = int(''.join(popped), 16)
        desc_array.append((2, track_length, f"<Track marker. Track is {track_length} bytes long>"))
        return scan_pos, True
    elif slice_match(hex_array, scan_pos, ["4D", "54", "68", "64"], 0, 4):
        stamp(2, "MIDI header somewhere where it really shouldn't be? (Honestly I'm not sure if it's even possible to proc this error.)")
        return scan_pos, False
    else:
        stamp(2, f"Invalid byte format following 4D at {scan_pos}.")
        return scan_pos, False

def disambiguate_FF_51(hex_array, scan_pos, desc_array, total_d):
    popped, scan_pos = pop_hex(hex_array, scan_pos, 2)
    length, scan_pos = read_VLQ(hex_array, scan_pos)
    if length != 3:
        stamp(2, f"Malformed tempo meta event. Expected value 3 received {length}")
        return scan_pos
    popped, scan_pos = pop_hex(hex_array, scan_pos, 3)
    tempo = int(''.join(popped), 16)
    bpm = int(60000000 / tempo)
    stamp(5, f"Tempo of {tempo} / {bpm} BPM")
    desc_array.append((3, total_d, tempo, bpm, f"BPM set to {bpm}"))
    return scan_pos

def disambiguate_FF_58(hex_array, scan_pos, desc_array, total_d):
    popped, scan_pos = pop_hex(hex_array, scan_pos, 2)
    length, scan_pos = read_VLQ(hex_array, scan_pos)
    if length != 4:
        stamp(2, "Malformed tempo meta event.")
        return scan_pos
    popped, scan_pos = pop_hex(hex_array, scan_pos, 1)
    numerator = int(popped[0], 16)
    popped, scan_pos = pop_hex(hex_array, scan_pos, 1)
    denominator = 2**(int(popped[0],16))
    popped, scan_pos = pop_hex(hex_array, scan_pos, 1)
    clocks_per_metronome_tick = int(popped[0], 16)
    popped, scan_pos = pop_hex(hex_array, scan_pos, 1)
    thirtyseconds_per_tick = int(popped[0], 16)
    desc_array.append((4, total_d, numerator, denominator, clocks_per_metronome_tick, thirtyseconds_per_tick, f"Time signature set to {numerator}/{denominator}, {clocks_per_metronome_tick} clocks per metronome, {thirtyseconds_per_tick} 32nd notes per quarter."))
    return scan_pos

def disambiguate_FF_2F(hex_array, scan_pos, desc_array, total_d):
    popped, scan_pos = pop_hex(hex_array, scan_pos, 2)
    length, scan_pos = read_VLQ(hex_array, scan_pos)
    if length != 0:
        stamp(2, f"Malformed end of track event, length should always be 0, received {length}")
    desc_array.append((5, total_d, f"End of track at {total_d}"))
    return scan_pos, False

def disambiguate_FF_03(hex_array, scan_pos, desc_array, total_d):
    popped, scan_pos = pop_hex(hex_array, scan_pos, 2)
    length, scan_pos = read_VLQ(hex_array, scan_pos)
    instrument, scan_pos = read_hex_as_ascii(hex_array, scan_pos, length)
    desc_array.append((6, total_d, instrument, f"Instrument set to {instrument} at {total_d}"))
    return scan_pos
    
def disambiguate_B(hex_array, scan_pos, desc_array, total_d):
    popped, scan_pos = pop_hex(hex_array, scan_pos, 3)
    channel = int(popped[0][1], 16)
    controller = int(popped[1], 16)
    value = int(popped[2], 16)
    match controller:
        case 0:
            controller_name = "Bank Select MSB"
        case 1:
            controller_name = "Mod Wheel"
        case 7:
            controller_name = "Volume"
        case 10:
            controller_name = "Pan"
        case 64:
            controller_name = "Sustain Pedal"
        case 74:
            controller_name = "Brightness"
        case 120:
            controller_name = "All Sound Off"
        case _:
            controller_name = "Undefined"
    desc_array.append((7, total_d, channel, controller, value, controller_name, f"Control change on channel {channel}: {controller} - {controller_name} set to {value}"))
    return scan_pos

def disambiguate_C(hex_array, scan_pos, desc_array, total_d):
    popped, scan_pos = pop_hex(hex_array, scan_pos, 2)
    channel = int(popped[0][1], 16)
    program = int(popped[1], 16)
    desc_array.append((8, total_d, channel, program, f"Program on channel {channel} changed to {program}."))
    return scan_pos     


def disambiguate_9(hex_array, scan_pos, desc_array, total_d):
    popped, scan_pos = pop_hex(hex_array, scan_pos, 3)
    channel = int(popped[0][1], 16)
    pitch = int(popped[1], 16)
    velocity = int(popped[2], 16)
    stamp(5, f"Note on with {channel, pitch, velocity}")
    if velocity == 0:
        stamp(5, "Velocity 0, converting to Note Off")
        on_off_event_conversion(desc_array, total_d, channel, pitch, velocity)
        return scan_pos
    else:
        length = 0
        matched = False
        desc_array.append((0, total_d, channel, pitch, velocity, matched, length, f"Channel {channel} note on, pitch {pitch}, velocity {velocity}."))
        return scan_pos

def on_off_event_conversion(desc_array, total_d, channel, pitch, velocity):
    stamp(5, f"Note off with {channel, pitch, velocity}")
    matched = False
    desc_array.append((9, total_d, channel, pitch, velocity, matched, f"Channel {channel} note off, pitch {pitch}, velocity {velocity}."))


def disambiguate_8(hex_array, scan_pos, desc_array, total_d):
    popped, scan_pos = pop_hex(hex_array, scan_pos, 3)
    channel = int(popped[0][1], 16)
    pitch = int(popped[1], 16)
    velocity = int(popped[2], 16)
    stamp(5, f"Note off with {channel, pitch, velocity}")
    matched = False
    desc_array.append((9, total_d, channel, pitch, velocity, matched, f"Channel {channel} note off, pitch {pitch}, velocity {velocity}."))
    return scan_pos

def disambiguate_body(hex_array, scan_pos, desc_array):
    hex_len = len(hex_array)
    next_hex = ""
    total_d = 0
    in_track = False
    time_type = desc_array[0][3]

    if time_type != "PPQN":
        stamp(1, "Disambiguator currently only supports MIDI that uses PPQN timing, sorry!")
        return

    while scan_pos < hex_len:
        await_delta = True
        if in_track:
            while await_delta:
                popped, scan_pos = pop_hex(hex_array, scan_pos)
                pop_int = int(''.join(popped), 16)
                if pop_int >= 128:
                    total_d += pop_int-128
                else:
                    total_d += pop_int
                    await_delta = False
         
        next_hex = read_hex(hex_array, scan_pos)

        match next_hex: 
            case ['4D']:
                scan_pos, in_track = disambiguate_4D(hex_array, scan_pos, desc_array)
            case ['FF']:
                # FF is the meta event marker, with the type defined by the following byte.
                match read_hex(hex_array, scan_pos+1):
                    case ['03']:
                        scan_pos = disambiguate_FF_03(hex_array, scan_pos, desc_array, total_d)
                    case ['2F']:
                        scan_pos, in_track = disambiguate_FF_2F(hex_array, scan_pos, desc_array, total_d)
                    case ['51']:
                        scan_pos = disambiguate_FF_51(hex_array, scan_pos, desc_array, total_d)
                    case ['58']:
                        scan_pos = disambiguate_FF_58(hex_array, scan_pos, desc_array, total_d)
                    case _:
                        stamp(2, f"Meta event without case hit: {next_hex} {read_hex(hex_array, scan_pos+1)} at {scan_pos}")
                        print(*desc_array, sep='\n')
                        return scan_pos, desc_array
                
            case _:
                # Check for the events that just use the first 4bits as the identifier.
                match next_hex[0][0]:
                    case '8':
                        scan_pos = disambiguate_8(hex_array, scan_pos, desc_array, total_d)
                    case '9':
                        scan_pos = disambiguate_9(hex_array, scan_pos, desc_array, total_d)
                    case 'B':
                        scan_pos = disambiguate_B(hex_array, scan_pos, desc_array, total_d)
                    case 'C':
                        scan_pos = disambiguate_C(hex_array, scan_pos, desc_array, total_d)
                # Finally, check if not case not caught.
                    case _:
                        stamp(2, f"Hex without case hit: {next_hex} at {scan_pos}")
                        print(*desc_array, sep='\n')
                        return scan_pos, desc_array
    desc_array.append((999, total_d, f"End of file at {total_d}"))
    return scan_pos, desc_array

def find_event_match(desc_array, x):
    item_ch = desc_array[x][2]
    item_pitch = desc_array[x][3]
    for i in range (x, len(desc_array)):
        stamp(5, f"Potential match {desc_array[i]}")
        if desc_array[i][0] == 9 and desc_array[i][2] == item_ch and desc_array[i][3] == item_pitch and desc_array[i][5] == False:
            return i
    stamp(2, f"No match found.")
    return 0

def match_notes(desc_array, i, match):
    desc_array[i] = (desc_array[i][0], desc_array[i][1], desc_array[i][2], desc_array[i][3], desc_array[i][4], True, desc_array[match][1] - desc_array[i][1], desc_array[i][7])
    desc_array[match] = (desc_array[match][0], desc_array[match][1], desc_array[match][2], desc_array[match][3], desc_array[match][4], True, desc_array[match][6])
    stamp(5, f"Matched {desc_array[i]} and {desc_array[match]}")

def check_note_strays(desc_array):
    x = 0
    y = 0
    for i in range (0, len(desc_array)):
        if desc_array[i][0] == 0 and desc_array[i][5] == False:
            x+=1
        if desc_array[i][0] == 9 and desc_array[i][5] == False:
            y+=1
    return x, y

def join_note_events(desc_array):
    stamp(5, "Joining note events")
    for i in range (0, len(desc_array)):
        stamp(5, f"Checking item {desc_array[i]}")
        if desc_array[i][0] == 0 and desc_array[i][5] == False:
            stamp(5, f"Unpaired note found at {desc_array[i]}")
            match = find_event_match(desc_array, i)
            if match == 0:
                stamp(2, f"No match for {desc_array[i]}")
            else:
                stamp(5, f"Match at {desc_array[i]}, joining.")
                match_notes(desc_array, i, match)
    remaining_on, remaining_off = check_note_strays(desc_array)
    stamp(4, f"Note events joined with {remaining_on} unmatched on events and {remaining_off} unmatched off events.")


def disambiguate_midi(filepath):
    hex_array = midi_to_hex_array(filepath)
    desc_array = []
    scan_pos = 0
    scan_pos, desc_array = disambiguate_header(hex_array, scan_pos, desc_array)
    if not validate_body(hex_array, scan_pos, desc_array):
        print("MIDI file is invalid or malformed.")
        return desc_array
    scan_pos, desc_array = disambiguate_body(hex_array, scan_pos, desc_array)
    join_note_events(desc_array)
    return desc_array

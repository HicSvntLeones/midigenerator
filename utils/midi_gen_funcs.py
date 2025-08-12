from utils.midilogger import *

#This doesn't handle notes that are lower than MIDI can support cleanly, but I'm not going to be going anywhere near that territory for this project.

def get_pitch(note):
    pitch = 0
    data = list(note)
    if len(note) == 0 or len(note) > 4:
        stamp(2, f"Invalid note received: {note}")
        return pitch
    match data[0]:
        case 'A':
            pitch = 9
        case 'B':
            pitch = 11
        case 'C':
            pitch = 0
        case 'D':
            pitch = 2
        case 'E':
            pitch = 4
        case 'F':
            pitch = 5
        case 'G':
            pitch = 7
        case _:
            stamp(2, f"Invalid note received: {note}")
            return pitch
    if len(data) <= 1:
        pitch += 48
        stamp(5, f"Received note only, treating as 3rd octave: {note}")
        return pitch
    match data[1]:
        case 'b':
            pitch -= 1
        case 's':
            pitch += 1
        case '-':
            if len(data) > 2:
                if data[2] == '1':
                    return pitch
                else:
                    stamp(2, f"Invalid note received: {note}")
                    return 0
            else:
                stamp(2, f"Invalid note received: {note}")
                return 0
        case _:
            try:
                pitch_mod = int(data[1]) + 1 
                pitch += pitch_mod*12
                return pitch
            except: 
                stamp(2, f"Invalid note received: {note}")
                return 0
    if len(data) <= 2:
        pitch += 48
        stamp(5, f"Received note only, treating as 3rd octave: {note}")
        return pitch
    
    match data[2]:
        case '-':
            if len(data) > 3:
                if data[3] == '1':
                    return pitch
                else:
                    stamp(2, f"Invalid note received: {note}")
                    return 0
            else:
                stamp(2, f"Invalid note received: {note}")
                return 0
        case _:
            try:
                pitch_mod = int(data[2]) + 1 
                pitch += pitch_mod*12
                return pitch
            except: 
                stamp(2, f"Invalid note received: {note}")
                return 0
    
def int_to_hex(num, hex_length = 1):
    stamp(5, f"Converting {num} to {hex_length} hex(es)")
    stringed_length = str(hex_length*2)
    hex_string = f"{int(num):0{stringed_length}X}"
    stamp(5, f"Result: {hex_string}")
    return hex_string

def int_to_VLQ(num):
    stamp(5, f"Converting {num} to VLQ hex(es)")
    vlq = [num & 0x7F] #Bitwise AND operation that leaves just the final 7 bits
    num >>= 7 #Shifts num 7 bits to the right (bits shifted past 0 are removed)
    while num:
        next_byte = (num & 0x7F) | 0x80 #Leaves just the final 7 bits, then a bitwise OR adds bit 8
        vlq.insert(0, next_byte) #inserts in byte list at position 0, shifts the rest right
        num >>= 7
    stamp(5, f"Resulted in {vlq}")
    vlq_hex = [format(item, '02X') for item in vlq]
    stamp(5, f"Converted to hex: {vlq_hex}")
    return ''.join(vlq_hex)

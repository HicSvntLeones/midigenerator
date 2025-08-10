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
    

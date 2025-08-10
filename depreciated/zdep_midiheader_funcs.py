def prime_header(primed_hex): # primes a basic header that seems to work
    header_chunk = []
    header_chunk = ("4D 54 68 64 " #MThd - MIDI header
                    "00 00 00 06 " #Header length (number of bytes below this)
                    "00 01 " #Format 1 - Multitrack
                    "00 02 " #2 tracks
                    "03 E8" #Division - 1000 ticks per quarter note (a silly division to use but whatever)
                    ).split()
    print(f"priming basic header: {header_chunk}")
    for hex in header_chunk:
        primed_hex.append(hex)
    
def default_track_settings(primed_hex): #primes some basic settings as its own midi track (seems to work?)
    track_chunk = []
    track_chunk = ("4D 54 72 6B " #MTrk - Track Chunk
                   "00 00 00 13 " #Track length (19 bytes remaining)
                   "00 FF 51 03 07 A1 20 " #Set tempo to 500,000 (120bpm)
                   "00 FF 58 04 04 02 18 08 " #Time signature and some other MIDI defs (clocks/click)
                   "00 FF 2F 00" #End of track
                   ).split()
    print(f"priming basic header: {track_chunk}")
    for hex in track_chunk:
        primed_hex.append(hex)
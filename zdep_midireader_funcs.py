def disambiguate_midi(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    # Convert bytes to upper case hex array
    hex_string = data.hex().upper()
    hex_array = (' '.join(hex_string[i:i+2] for i in range(0, len(hex_string), 2))).split()
    hex_id = 0
    read_header(hex_array, hex_id)

def read_hex(hex_array, hex_id, n=1):
    read = hex_array[hex_id:hex_id+n]
    print(read)
    return read

def pop_hex(hex_array, hex_id, n):
    pop = hex_array[hex_id:hex_id+n]
    hex_id += n
    return hex_id, pop

def read_header(hex_array, hex_id): #MIDI headers follow a consistant format, check format
    if hex_id != 0:
        raise Exception("read_header function called incorrectly")
    #Confirm MThd
    if read_hex(hex_array, hex_id, 4) == ['4D', '54', '68', '64']:
        print("MThd - MIDI header")
        hex_id, last_popped = pop_hex(hex_array, hex_id, 4)
    else:
        raise Exception("Header does not match expected MIDI header")
    
    #Confirm 6 bytes of header data
    if read_hex(hex_array, hex_id, 4) == ['00', '00', '00', '06']:
        print("Six bytes of header data")
        hex_id, last_popped = pop_hex(hex_array, hex_id, 4)
    else:
        raise Exception("Header does not match expected MIDI header format")
    
    #Get format type
    hex_id, last_popped = pop_hex(hex_array, hex_id, 2)
    if int(last_popped[1],16) > 3:
        raise Exception("Invalid Format Type")
    else: 
        print(last_popped)
        print(f"Format type: {int(last_popped[1],16)}")   
    
    #Get number of tracks
        hex_id, last_popped = pop_hex(hex_array, hex_id, 2)
        print(last_popped)
        num = int((last_popped[0]+last_popped[1]),16)
        print(f"Number of Tracks: {num}")  

    #Get division (ticks per quarter note)
        hex_id, last_popped = pop_hex(hex_array, hex_id, 2)
        print(last_popped)
        num = int((last_popped[0]+last_popped[1]),16)
        print(f"Ticks per quarter note: {num}")  

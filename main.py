from pathlib import Path
from midi_test_funcs import print_raw_hex
from midiheader_funcs import prime_header
from midireader_funcs import disambiguate_midi

#primed_hex = []
#prime_header(primed_hex)
#print(primed_hex)
#disambiguate_midi("testdata/C3_test_example.mid")

def main():
    running = True
    print("Enter 'help' for a list of valid commands.")
    while running:
        commandReturn = read_command()
        if commandReturn == "exit":
            running = False
    print("Exit command received. Exiting...")

def read_command(): # Most of the user input processing logic is handled here.
    command = input(">").strip().lower().split()
    match command[0]:
        case "help"|"h":
            display_help()
        case "exit"|"quit"|"q"|"end":
            return "exit"
        case _:
            print("Unknown command.")

def display_help():
    help_file = Path(__file__).parent / "help.md"
    if help_file.exists():
        print(help_file.read_text())
    else:
        print("Help file not found.")

if __name__ == "__main__":
    main()
    
from pathlib import Path
import configparser
from midilogger import *

from midi_test_funcs import print_raw_hex
from midiheader_funcs import prime_header
from midireader_funcs import disambiguate_midi

#primed_hex = []
#prime_header(primed_hex)
#print(primed_hex)
#disambiguate_midi("testdata/C3_test_example.mid")

def main():
    config = load_config()
    apply_config(config)
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

def load_config():
    custom_config = Path(__file__).parent / "customconfig.ini"
    default_config = Path(__file__).parent / "defaultconfig.ini"
    if custom_config.exists():
        config = configparser.ConfigParser()
        config.read(custom_config)
        return config
    elif default_config.exists():
        config = configparser.ConfigParser()
        config.read(default_config)
        return config
    else:
        print("No config file found.")

def apply_config(config):
    set_log_level(config.getint('logger', 'log_level'))
    set_log_time(config.getboolean('logger', 'include_time'))

def write_config(config):
    with open('customconfig.ini', 'w') as configfile:
        config.write(configfile)

if __name__ == "__main__":
    main()
    
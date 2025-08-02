from pathlib import Path
import configparser
from midilogger import *
from input_parsers import *

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
            stamp(4, "Program exit flag triggered.")
            running = False
    print("Exiting...")

def read_command(): # Most of the user input processing logic is handled here.
    command = input(">").strip().lower().split()
    match command[0]:
        case "help"|"h":
            stamp(5, "Received help command.")
            display_help()
        case "config"|"settings"|"c":
            stamp(5, "Received config command.")
            run_config()
        case "exit"|"quit"|"q"|"end":
            stamp(5, "Received exit command.")
            return "exit"
        case _:
            stamp(4, "Received unknown command.")
            print("Unknown command.")

def display_help():
    help_file = Path(__file__).parent / "help.md"
    if help_file.exists():
        print(help_file.read_text())
    else:
        stamp(2, "help.md missing")

def run_config():
    running_config = True
    while running_config:
        config = load_config()
        apply_config(config)
        section_list = config.sections()
        print(f"Found sections: {section_list}")
        print("Type a new key-value pair to edit, type a section to see the keys within, or type exit to exit.")
        command = input(">").strip().lower().split()
        comlen = len(command)
        if command[0] == "exit":
            stamp(5, "Received exit command.")
            running_config = False
            print("Exiting config.")
        elif command[0] in section_list:
            stamp(5, "Received command matching section name.")
            print(dict(config[command[0]].items()))
        elif comlen != 2:
            stamp(3, "Received wrong number of arguments.")
            print("Config keys take exactly 1 argument.")
        else:
            stamp(5, "Received non-section or exit command.")
            match command[0]:
                case "log_level":
                    try:
                        command[1] = parse_int(command[1])
                        if isinstance(command[1], int) and 1 <= command[1] <= 5:
                            print(f"setting log_level to {command[1]}")
                            config.set('logger','log_level',str(command[1]))
                            write_config(config)
                        else:
                            print(f"log_level takes integer between 1 and 5.")
                    except:
                        print(f"log_level takes integer between 1 and 5.")

                case "include_time":
                    try:
                        command[1] = parse_bool(command[1])
                        if isinstance(command[1], bool):
                            print(f"setting include_time to {command[1]}")
                            config.set('logger','include_time',str(command[1]))
                            write_config(config)
                        else:
                            print(f"include_time takes boolean.")
                    except:
                        print(f"include_time takes boolean.")

                case _:
                    stamp(4, "Received command that doesn't match a key.")
                    print("Not a valid section name or key.")

            

def load_config():
    custom_config = Path(__file__).parent / "customconfig.ini"
    default_config = Path(__file__).parent / "defaultconfig.ini"
    if custom_config.exists():
        stamp(4, "Using user-defined config.")
        config = configparser.ConfigParser()
        config.read(custom_config)
        return config
    elif default_config.exists():
        stamp(3, "No user config file. Using default config.")
        config = configparser.ConfigParser()
        config.read(default_config)
        return config
    else:
        stamp(1, "No config files found. Behavior may be unstable.")

def apply_config(config):
    set_log_level(config.getint('logger', 'log_level'))
    set_log_time(config.getboolean('logger', 'include_time'))

def write_config(config):
    with open('customconfig.ini', 'w') as configfile:
        config.write(configfile)
    stamp(4, "User defined config file created.")

if __name__ == "__main__":
    main()
    
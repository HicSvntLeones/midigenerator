from pathlib import Path
import configparser
from midilogger import *
from input_parsers import *
from get_info import *
from midi_tests import *

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
    args = len(command)-1
    match command[0]:
        case "help"|"h":
            stamp(5, "Received help command.")
            if args == 0:
                get_info("help")
            elif args > 0:
                get_info(command[1])
        case "config"|"settings"|"c":
            stamp(5, "Received config command.")
            run_config()
        case "exit"|"quit"|"q"|"end":
            stamp(5, "Received exit command.")
            return "exit"
        case "test":
            if args == 0:
                get_info("test")
            elif args > 0:
                match command[1]:
                    case "1":
                        midi_test_1()
                    case "2":
                        midi_test_2()
                    case "3":
                        midi_test_3()
                    case _:
                        stamp(4, "Received unknown argument.")
                        print("Unknown argument.")
        case _:
            stamp(4, "Received unknown command.")
            print("Unknown command.")

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
            match command[0]: # Config match/case begins here. Going to be pretty gross to look at but that's a problem for future me.
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

# END OF CONFIG MATCH/CASE BLOCK

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
    stamp(5, "Applied all configs.")

def write_config(config):
    with open('customconfig.ini', 'w') as configfile:
        config.write(configfile)
    stamp(4, "User defined config file created.")

if __name__ == "__main__":
    main()
    
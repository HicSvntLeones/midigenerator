from ...hsl_tools import logger
import os
import json

class HSL_CLI_Template:

    def __init__(self, id):
        logger.info("Initializing CLI.", id)
        self.id = id
        self.commands = {
            'exit':self.exit,
            'help':self.help
        }
        self.menu()

    def menu(self):
        self.running = True   
        while self.running:
            user_input = input(">").strip().lower().split()
            
            if not user_input:
                continue

            command, *args = user_input

            if not args:
                args = [""]

            if command in self.commands:
                self.commands[command](args)

            else:
                print("Command not found.")
    
    def exit(self):
        """Exits the program."""
        self.running = False

    def help(self):
        """Prints all available commands.
        help <command> will print the help of that command.
        [square brackets] indicate required arguments.
        <angled brackets> indicate optional arguments."""

class HSL_CLI_Sub:

    def __init__(self, id):
        logger.info("Initializing submenu CLI.", id)
        self.id = id
        self.menu()

    def menu(self):    
        while True:
            command = input(">").strip().lower().split()
            match command[0]:
                case "back":
                    logger.info("Exit command received. Exiting cleanly.", self.id)
                    break
                case _:
                    print("Unrecognized command.")


                



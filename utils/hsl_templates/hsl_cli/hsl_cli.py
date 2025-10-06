from ...hsl_tools import logger

class HSL_CLI_Main:

    def __init__(self):
        logger.info("Initializing CLI.")
        self.menu()

    def menu(self):    
        while True:
            command = input(">").strip().lower().split()
            match command[0]:
                case "exit":
                    logger.info("Exit command received. Exiting cleanly.")
                    break
                case _:
                    print("Unrecognized command.")

class HSL_CLI_Sub:

    def __init__(self):
        logger.info("Initializing submenu CLI.")
        self.menu()

    def menu(self):    
        while True:
            command = input(">").strip().lower().split()
            match command[0]:
                case "back":
                    logger.info("Exit command received. Exiting cleanly.")
                    break
                case _:
                    print("Unrecognized command.")
                



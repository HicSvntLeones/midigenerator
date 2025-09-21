from ..hsl_logger.hsl_logger import logger

class CLI_generic_menu:

    def __init__(self):
        logger.info("Initializing CLI.")

    def menu(self):    
        while True:
            command = input(">").strip().lower().split()
            match command[0]:
                case "exit":
                    logger.info("Exit command received. Exiting cleanly.")
                    break
                case _:
                    pass
                



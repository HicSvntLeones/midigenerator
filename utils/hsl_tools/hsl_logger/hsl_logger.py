#Import LiteLogger from this to create a new instance.

import os
import json

class LiteLogger:
    RED = "\033[31m"
    YELLOW = "\033[33m"
    GREEN = "\033[32m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    def __init__(self):
        self.setup()
        self.info("LiteLogger instance initialized.")

    def setup(self):
            self.dir_path = os.path.dirname(__file__)
            self.settings_path = os.path.join(self.dir_path, "lite_logger_settings.json")
            if not os.path.exists(self.settings_path):
                self.info("LiteLogger settings not found: Creating...")
                self.create_settings()
            self.load_settings()

    def load_settings(self):
        with open(self.settings_path, 'r') as f:
            self.ids = json.load(f)
        self.debug("LiteLoggerDebugTest", "Settings loaded.")

    def create_settings(self):
        self.info("Creating/resetting settings to defaults.")
        default_settings = {
            "LiteLoggerCrit":True,
            "LiteLoggerWarn":True,
            "LiteLoggerInfo":True,
            "LiteLoggerDebugTest":True,
        }

        with open(self.settings_path, 'w') as f:
            json.dump(default_settings, f, indent=4)
        self.info(f"Created {self.settings_path} with default settings.")





    def critical(self, msg = 'no message', id = '', *args):
        if self.ids['LiteLoggerCrit'] is not True:
            return
        tag = "[CRITICAL] "
        tag2 = f"[{id}]" if id != '' else ''
        if args:
            fmsg = msg % args
        else:
            fmsg = msg
        print(self.RED + self.BOLD + tag + tag2 + fmsg + self.RESET)
    


    def warning(self, msg = 'no message', id = '', *args):
        if self.ids['LiteLoggerWarn'] is not True:
            return
        tag = "[WARNING] "
        tag2 = f"[{id}]" if id != '' else ''
        if args:
            fmsg = msg % args
        else:
            fmsg = msg
        print(self.YELLOW + self.BOLD + tag + tag2 + fmsg + self.RESET)



    def info(self, msg = 'no message', id = '', *args):
        if self.ids['LiteLoggerInfo'] is not True:
            return
        tag = "[INFO] "
        tag2 = f"[{id}]" if id != '' else ''
        if args:
            fmsg = msg % args
        else:
            fmsg = msg
        print(self.GREEN + tag + tag2 + fmsg + self.RESET)



    def debug(self, id = 'undefined', msg = 'no message', *args):
        if id not in self.ids:
            self.warning(f"ID not found {id}")
            return
        if self.ids[id] is not True:
            return
        try:
            formatted = msg % args
            print(f"[DEBUG][{id}] {formatted}")
        except:
            self.warning(f"Debug statement formatting error in {id}")

logger = LiteLogger()
    






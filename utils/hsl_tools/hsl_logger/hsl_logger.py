import os
import json

class HSLLogger:
    RED = "\033[31m"
    YELLOW = "\033[33m"
    GREEN = "\033[32m"
    BOLD = "\033[1m"
    RESET = "\033[0m"
    DEFAULTS = {
            "HSLLoggerCrit":True,
            "HSLLoggerWarn":True,
            "HSLLoggerInfo":True,
        }

    def __init__(self):
        self.setup()
        self.info("HSLLogger instance initialized.")

    def setup(self):
            self.dir_path = os.path.dirname(__file__)
            self.settings_path = os.path.join(self.dir_path, "hsl_logger_settings.json")
            if not os.path.exists(self.settings_path):
                self.info("HSLLogger settings not found: Creating...")
                self.create_settings()
            self.load_settings()
            self.validate_settings()

    def load_settings(self):
        try:
            with open(self.settings_path, 'r') as f:
                self.ids = json.load(f)
            self.info("HSLLogger settings loaded.")
        except:
            self.critical("HSL failed to load settings. File may be malformed.")

    def create_settings(self):
        self.info("Creating/resetting settings to defaults.")
        with open(self.settings_path, 'w') as f:
            json.dump(self.DEFAULTS, f, indent=4)
        self.info(f"Created {self.settings_path} with default settings.")

    def validate_settings(self):
        valid = True
        missing_keys = []
        for key in self.DEFAULTS:
            if key not in self.ids:
                valid = False
                missing_keys.append(key)
        if valid:
            self.info("Settings validated.")
            return
        self.warning(f"Critical settings key(s) missing: {missing_keys}")




    def critical(self, msg = 'no message', id = '', *args):
        if self.ids.get('HSLLoggerCrit') is False:
            return
        tag = "[CRITICAL] "
        tag2 = f"[{id}]" if id != '' else ''
        if args:
            fmsg = msg % args
        else:
            fmsg = msg
        print(self.RED + self.BOLD + tag + tag2 + fmsg + self.RESET)
    


    def warning(self, msg = 'no message', id = '', *args):
        if self.ids.get('HSLLoggerWarn') is False:
            return
        tag = "[WARNING] "
        tag2 = f"[{id}]" if id != '' else ''
        if args:
            fmsg = msg % args
        else:
            fmsg = msg
        print(self.YELLOW + self.BOLD + tag + tag2 + fmsg + self.RESET)



    def info(self, msg = 'no message', id = '', *args):
        if self.ids.get('HSLLoggerInfo') is False:
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
    






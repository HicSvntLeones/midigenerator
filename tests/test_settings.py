from utils.midilogger import *

# This is to modify the generator settings for testing purposes, independant of the user settings.

def set_test_settings(input_settings, test_number):
    if test_number == 5:
        overwrite_settings = {
            'ppq':1000
        }
    test_settings = {**input_settings, **overwrite_settings}
    stamp(5, f"Test settings set to {test_settings}")
    return test_settings
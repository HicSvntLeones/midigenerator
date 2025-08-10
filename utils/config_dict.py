from utils.midilogger import *
import configparser

# This takes the config file and gives a dictionary of the generator relvant settings

def generate_config_dict(config):
    setting_dict = {}
    setting_dict['ppq'] = config.getint('midi', 'ppq')
    return setting_dict
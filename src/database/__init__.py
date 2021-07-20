from configparser import ConfigParser

CONFIG_INI_LOCATION = '/Users/ulieschnaithmann/repos/budgeting/src/config/config.ini'

parser = ConfigParser()
parser.read(CONFIG_INI_LOCATION)
constants = {section: {key: val for key, val in parser.items(section)} for section in parser.keys()}

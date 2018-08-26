import os
from collections import OrderedDict
from configparser import ConfigParser, BasicInterpolation

"""  Module 'preferences.py': handles preferences for pylcg parent.
Functions: 
    extract_ordered_dict from config()
    copy_config()
Exceptions:
    InvalidKeysError
Class:
    Preferences: container for preferences. Includes default (permanent) and current versions.
"""


__author__ = "Eric Dose :: New Mexico Mira Project, Albuquerque"


PYLCG_ROOT_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIRECTORY = os.path.join(PYLCG_ROOT_DIRECTORY, "data")
PREFERENCES_INI_FULLPATH = os.path.join(DATA_DIRECTORY, 'preferences.ini')

CONFIG_DELIMITERS = ('=',)  # we avoid ':' because we'll want to specify Windows directory paths.

DEFAULT_CONFIG_TEXT = """
# DEFAULT CONFIG text for pylcg. To be read directly into a python ConfigParser object.
# Note that section keys are case-sensitive, but individual option keys are not. Hey don't ask me.
[Format preferences]
  Plot height = 720
  Plot width = 1280
  Plot style =
  Show Errorbars = Yes
  Show Grid = Yes
  
[Data preferences]
  Bands = B,V,R,I,Vis
  Days = 500
  Last Upload File =
  Last Observer HighLighted = 
  Observer List Columns = Obscode,Name,Count
"""


SUPPORT__________________________________ = 0


def extract_ordered_dict_from_config(source_config):
    """  Extracts a (nested) python OrderedDict from the contents of a ConfigParser object.
    Why python doesn't just provide this is unfathomable.
    :param source_config: config object from which to extract content [ConfigParser object].
    :return: python OrderedDict of config's contents [OrderedDict object].
    """
    config_dict = OrderedDict([(s, OrderedDict(source_config.items(s))) for s in source_config.sections()])
    # config_dict = {s: dict(source_config.items(s)) for s in source_config.sections()}  #unordered py<3.7.
    return config_dict


def copy_config(source_config):
    """  Necessary as python weirdly (ok, typically) forgot BOTH to implement a .copy() method
         and to expose the wrapped OrderedDict --- <eye roll> also... the OrderedDict's field keys
         all get changed to lower case for no reason. </eye roll>).
         Section keys are case-sensitive, but option keys are case-insensitive. Unbelievable.
    :param source_config: configuration to copy [ConfigParser object].
    :return: deep, independent copy of source_config [new ConfigParser object].
    """
    config_dict = extract_ordered_dict_from_config(source_config)
    config_copy = ConfigParser()
    config_copy.read_dict(config_dict)
    return config_copy


def overlay_config_with_config(config_to_change, config_with_new_values):
    """  Make new config_dict by overwriting options in config_dict_to_change by any matching
             options in config_dict_new_values.
         But never overwrites with null or missing values even if present in config_dict_new_values.
         Does NOT alter either config_dict passed in as parameters.
    :param config_to_change: this is the base config to be updated [ConfigParser object].
    :param config_with_new_values: this contains the changes to make [ConfigParser object].
    :return: COPY of updated config_dict_to_change [nested OrderedDict].
    """
    updated_config = copy_config(config_to_change)
    for section_key in config_with_new_values.sections():
        for option_key in config_with_new_values[section_key]:
            value = config_with_new_values[section_key][option_key]
            if value is not None:
                if value.strip() != '':
                    try:
                        updated_config[section_key][option_key] = value
                    except KeyError:
                        raise InvalidKeysError((section_key, option_key))
    return updated_config


CLASSES_EXCEPTIONS__________________________________ = 0


class Error(Exception):
    pass


class InvalidKeysError(Error):
    """  Any key pair not included in defaults is disallowed and must raise this Exception. """
    pass


class Preferences:
    def __init__(self, preferences_ini_path=PREFERENCES_INI_FULLPATH, preferences_ini_string=None):
        """  The repository for pylcg preferences: default (permanent), ini_file, and current. """
        self.preferences_ini_path = preferences_ini_path
        self.preferences_ini_string = preferences_ini_string

        # Default config is defined above in this module, and is IMMUTABLE (read-only):
        self.default_config = ConfigParser(allow_no_value=True, delimiters=CONFIG_DELIMITERS,
                                           interpolation=BasicInterpolation())
        self.default_config.read_string(DEFAULT_CONFIG_TEXT)

        # ini_file config will strictly track contents of preferences.ini file.
        self.ini_file_config = ConfigParser(allow_no_value=True, delimiters=CONFIG_DELIMITERS,
                                            interpolation=BasicInterpolation())
        self.load_ini_file()

        # Current config starts as a copy of ini_file config, later updated as needed by the user (via GUI).
        self.current_config = copy_config(self.ini_file_config)

    def load_ini_file(self):
        ini_file_loaded = False
        if os.path.exists(self.preferences_ini_path):
            if os.path.isfile(self.preferences_ini_path):
                self.ini_file_config.read(self.preferences_ini_path)
                ini_file_loaded = True
        if not ini_file_loaded:
            self.write_defaults_to_ini_file()

    def set(self, section_key, option_key, value):
        if value is not None:
            try:
                self.current_config[section_key][option_key.lower()] = str(value)
            except KeyError:
                raise InvalidKeysError((section_key, option_key))

    def get(self, section_key, option_key):
        """Gets option value from current_dict. The function most used by calling routines."""
        try:
            value = self.current_config[section_key][option_key.lower()]
        except KeyError:
            raise InvalidKeysError((section_key, option_key))
        return value

    def write_current_config_to_ini_file(self):
        """  Always runs when the calling program is closing, but could be called any time."""
        with open(self.preferences_ini_path, 'w') as f:
            self.current_config.write(f)

    def write_defaults_to_ini_file(self):
        """  Facility to recover corrupted preferences.ini, or at user discretion.
             This goes inside class Preferences because it needs access to the relevant ini file path."""
        with open(self.preferences_ini_path, 'w') as f:
            self.default_config.write(f)

    def reset_current_to_default(self):
        self.current_config = copy_config(self.default_config)
        # self.current_dict = extract_ordered_dict_from_config(self.current_config)

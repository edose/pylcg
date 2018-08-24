import os
from collections import OrderedDict
from configparser import ConfigParser, BasicInterpolation

__author__ = "Eric Dose :: New Mexico Mira Project, Albuquerque"


PYLCG_ROOT_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIRECTORY = os.path.join(PYLCG_ROOT_DIRECTORY, "data")
SETTINGS_INI_FULLPATH = os.path.join(DATA_DIRECTORY, 'settings.ini')

CONFIG_DELIMITERS = ('=',)  # we avoid ':' because we'll want to specify Windows directory paths.

DEFAULT_CONFIG_TEXT = """
# DEFAULT CONFIG text for pylcg. To be read directly into a python ConfigParser object.
# Note that section keys are case-sensitive, but individual option keys are not. Hey don't ask me.
#    So lookups on ConfigParser objects are relatively predictable, 
#    but lookups on the dictionary contained in them are not, 
#    and such dict lookups should be avoided.
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


def copy_config_dict(config_dict):
    """  Deep copy a configuration dictionary, returning a wholly independent copy.
    :param config_dict: [nested OrderedDict]
    :return: deep, independent copy of config_dict [nested OrderedDict].
    """
    new_dict = OrderedDict()
    for section_key in config_dict.keys():
        new_dict[section_key] = config_dict[section_key].copy()
    return new_dict


def update_config_dict(config_dict_to_change, config_dict_new_values):
    """  Make new config_dict by overwriting options in config_dict_to_change by any matching
             options in config_dict_new_values.
         But never overwrites with null or missing values even if present in config_dict_new_values.
         Does NOT alter either config_dict passed in as parameters.
    :param config_dict_to_change: this will be updated [nested OrderedDict].
    :param config_dict_new_values: this contains the changes to make to config_dict_to_change
               [nested OrderedDict].
    :return: updated config_dict_to_change [nested OrderedDict].
    """
    updated_config_dict = copy_config_dict(config_dict_to_change)
    for section_key, section_dict in config_dict_new_values.items():
        for option_key, value in config_dict_new_values[section_key].items():
            if value is not None:
                if value != '':
                    try:
                        updated_config_dict[section_key][option_key] = value
                    except KeyError:
                        raise Settings_KeyError(section_key, option_key)
    return updated_config_dict


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


CLASSES__________________________________ = 0


class Settings_KeyError(Exception):
    """  Custom Exception.
    Any setting key not included in defaults must be disallowed and must raise this Exception.
    """
    def __init__(self, section_key, option_key):
        self.value = section_key + ' : ' + option_key


class Settings:
    def __init__(self, settings_ini_path=SETTINGS_INI_FULLPATH, settings_ini_string=None):
        """The repository for CURRENT settings. Many of these may be overwritten when settings file read.
        Internal workings are founded on python OrderedDict objects; ConfigParser objects limited to I/O.
        """
        self.settings_ini_path = settings_ini_path
        self.settings_ini_string = settings_ini_string

        # Default config is defined above in this module, and is IMMUTABLE (read-only):
        self.default_config = ConfigParser(allow_no_value=True, delimiters=CONFIG_DELIMITERS,
                                           interpolation=BasicInterpolation())
        self.default_config.read_string(DEFAULT_CONFIG_TEXT)
        self.default_dict = extract_ordered_dict_from_config(self.default_config)  # filled, immutable.

        # ini_file config will strictly track contents of settings.ini file.
        self.ini_file_config = ConfigParser(allow_no_value=True, delimiters=CONFIG_DELIMITERS,
                                            interpolation=BasicInterpolation())
        self.ini_file_dict = OrderedDict()
        self.load_ini_file()  # fills both ini_file_config and ini_file_dict.

        # Current config starts empty here, and will be initially copied from default_config,
        #    then updated by ini_file_config, and finally updated as needed by the user (via GUI).
        self.current_config = ConfigParser(allow_no_value=True, delimiters=CONFIG_DELIMITERS,
                                           interpolation=BasicInterpolation())
        self.current_dict = update_config_dict(config_dict_to_change=self.default_dict,
                                               config_dict_new_values=self.ini_file_dict)

    def load_ini_file(self):
        ini_file_loaded = False
        if os.path.exists(self.settings_ini_path):
            if os.path.isfile(self.settings_ini_path):
                self.ini_file_config.read(self.settings_ini_path)
                self.ini_file_dict = extract_ordered_dict_from_config(self.ini_file_config)
                ini_file_loaded = True
        if not ini_file_loaded:
            self.reset_ini_file_to_defaults()

    def set(self, section_key, option_key, value):
        if value is not None:
            try:
                self.current_dict[section_key][option_key.lower()] = str(value)
            except KeyError:
                raise Settings_KeyError(section_key, option_key)

    def get(self, section_key, option_key):
        """Gets option value from current_dict. The function most used by calling routines."""
        try:
            value = self.current_dict[section_key][option_key.lower()]
        except KeyError:
            raise Settings_KeyError(section_key, option_key)
        return value

    def save_current_config_to_ini_file(self):
        """  Always runs when the calling program is closing, but could be called any time."""
        with open(self.settings_ini_path, 'w') as f:
            self.current_config.write(f)

    def reset_ini_file_to_defaults(self):
        """  Facility to recover corrupted settings.ini, or at user discretion.
             This goes inside class Settings because it needs access to the relevant ini file path."""
        with open(self.settings_ini_path, 'w') as f:
            self.default_config.write(f)

    def set_current_config_to_default_config(self):
        self.current_config = copy_config(self.default_config)
        self.current_dict = extract_ordered_dict_from_config(self.current_config)

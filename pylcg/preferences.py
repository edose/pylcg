from collections import OrderedDict
from configparser import ConfigParser, MissingSectionHeaderError, ParsingError

__author__ = "Eric Dose :: New Mexico Mira Project, Albuquerque"

"""  Preferences module.
class Prefset: stripped-down container for preferences. 
    Can read and write to .ini files, but does not hold defaults or file locations (client must do those).
    USAGES:
        from Preferences import Prefset
        p = Prefset(my_ordered_dict)
        p2 = p.copy()
        p3 = p.as_updated_by(my_ordered_dict) or (my_prefset_obj)
        p4 = Prefset.from_ini_file(my_fullpath_string)
        p5 = p.write_to_ini_file(my_fullpath_string)
        successful = p.set('my key', 'my new value')  # in-place replacement
        value = p.get('my key')   
"""

# PYLCG_ROOT_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# PREFERENCES_DIRECTORY = os.path.join(PYLCG_ROOT_DIRECTORY, 'pylcg')
# PREFERENCES_INI_FULLPATH = os.path.join(PREFERENCES_DIRECTORY, 'preferences.ini')

CONFIG_DELIMITERS = ('=',)  # we avoid ':' preserves our option to include Windows paths in ini files.

# DEFAULT_CONFIG_TEXT = """
# # DEFAULT CONFIG text for pylcg. To be read directly into a python ConfigParser object.
# # Note that section keys are case-sensitive, but individual option keys are not. Hey don't ask me.
# # So we're going to make ALL the keys lower case. (Values can still be in either case.)
# [style preferences]
#   plot size = Smaller
#   show grid = Yes
#   show errorbars = Yes
#   plot in jd = Yes
#   plot less-thans = No
#
# [data preferences]
#   time span days = 500
#   bands = B,V,R,I,Vis
#   observer code =
#   highlight observer code = No
#   Last Observer Code HighLighted =
# """

# DEFAULT PREFSET for pylcg. Used if no .ini config file available, and ultimate fallback if all fails.
# In the python .ini-file handler (configparser package), Section keys are case-sensitive,
#    but Item keys are case-insensitive
#    (see https://docs.python.org/3.6/library/configparser.html?highlight=configparser#module-configparser
#    section 14.2.4) Hey, don't ask me what they were smoking.
# So we will lump all preference items into a single Section, arbitrarily named as below.
# DEFAULT_PREFSET_ORDERED_DICT = OrderedDict([
#     ('plot size', 'Smaller'),
#     ('show grid', 'Yes'),
#     ('show errorbars', 'Yes'),
#     ('plot in jd', 'Yes'),
#     ('plot less-thans', 'No'),
#     ('time span days', '500'),
#     ('bands', 'B,V,R,I,Vis'),
#     ('observer code', ''),
#     ('highlight observer code', 'No'),
#     ('last observer code', 'No')
# ])
# INI_FILE_SECTION_NAME = 'All Pylcg Preferences'


NEW_PREFSET_CODE__________________________________ = 0


class Prefset:
    """ A collection of user preferences to be used by the main app.
    """
    def __init__(self, ordered_dict=None, ini_section_name='Sole Section'):
        """  Base constructor. Makes a new Prefset from **a copy of** passed-in OrderedDict object.
        :param ordered_dict: [OrderedDict object]
        :param ini_section_name:
        """
        if ordered_dict is None:
            self.ordered_dict = None
            self.ini_section_name = ''
        elif isinstance(ordered_dict, OrderedDict):
            self.ordered_dict = ordered_dict.copy()  # contains None if None was passed in
            self.ini_section_name = ini_section_name
        else:
            self.ordered_dict = None
            self.ini_section_name = ''

    def copy(self):
        """  Returns independent copy of this prefset [Prefset object]. """
        return Prefset(self.ordered_dict.copy(), self.ini_section_name)

    def as_updated_by(self, newer_entries=None):
        """  Returns new prefset composed of this prefset as updated by a second prefset or OrderedDict.
             This is really a constructor, but not a class method (as it depends on a specific Prefset obj).
             Does *not* change either this Prefset (self) or the argument object.
        :param newer_entries: [Prefset object *OR* OrderedDict object]
        :return: new prefset, from this prefset as updated with newer entries [Prefset object]
            Returns None if anything but Prefset or OrderedDict is erroneously passed in.
        """
        if newer_entries is None:
            return self.copy()
        # Prepare and do update of OrderedDict object contained in Prefset:
        updated_ordered_dict = self.ordered_dict.copy()  # next to be updated...
        if isinstance(newer_entries, OrderedDict):
            updated_ordered_dict.update(newer_entries)  # .update() works in place w/o return (groan).
        elif isinstance(newer_entries, Prefset):
            updated_ordered_dict.update(newer_entries.ordered_dict)
        else:
            return Prefset(None)
        return Prefset(updated_ordered_dict, self.ini_section_name)

    @classmethod
    def from_ini_file(cls, fullpath=None):
        """ Reads an .ini file, returns Prefset (or None if .ini file doesn't exist).
        Usage: ini_prefset = Prefset.from_ini_file(fullpath)
        :param fullpath: usually omitted, but if present defines .ini file to be read in.
        :return: preference set from .ini file, or None if .ini file can't be read [Prefset object or None].
        """
        if fullpath is None:
            return None
        ini_file_ordered_dict = OrderedDict()
        config = ConfigParser(delimiters=CONFIG_DELIMITERS)
        try:
            return_value = config.read(fullpath)
        except (MissingSectionHeaderError, ParsingError):
            return None
        if len(return_value) == 0:  # file not successfully parsed (v.probably absent).
            return None
        # If here, we have found a .ini file, now parse it.
        for section_key in config.sections():
            for item_key in config[section_key]:
                value = config[section_key][item_key]
                ini_file_ordered_dict[item_key] = value
        new_prefset = cls(ini_file_ordered_dict, config.sections()[0])
        return new_prefset

    def write_to_ini_file(self, fullpath=None):
        """ Causes this Prefset object to write itself to an .ini file.
        Usage: current_prefset.write_to_ini_file(fullpath='C:/...')
        :param fullpath: fullpath of the .ini file to write to.
        :return: [No return value]
        """
        config = ConfigParser(delimiters=CONFIG_DELIMITERS)
        config[self.ini_section_name] = self.ordered_dict
        with open(fullpath, 'w') as f:
            config.write(f)

    def set(self, key, value, force_string=True):
        """  Set preference with given key to given value. No effect if given key not in Prefset keys.
        Usage: my_prefset.set('obscode', 'DERA'). *** IN-PLACE alteration. ***
        :param key: key of preference to set [string].
        :param value: value of preference to set [ideally a string].
        :param force_string: True if value must be (converted to and) stored as string [boolean].
        :return: True if success, else False.
        """
        if key in self.ordered_dict.keys():
            if force_string:
                self.ordered_dict[key] = str(value)
            else:
                self.ordered_dict[key] = value
            return True
        else:
            return False

    def get(self, key):
        """ Returns corresponding value if key exists, else return None.
        Usage: value = my_prefset.get('obscode')
        """
        return self.ordered_dict.get(key, None)

    # def remove(self, key):
    #     """ Removes corresponding setting (key and value) from this Prefset. Rarely used.
    #     Usage: successful = self.remove('obscode')
    #     :param: key: key of setting to remove [string]
    #     :return: True if successful, else False [boolean].
    #     """
    #     try:
    #         del self.ordered_dict[key]
    #     except KeyError:
    #         return False
    #     return True

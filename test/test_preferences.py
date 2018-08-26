import os
from collections import OrderedDict
from configparser import ConfigParser

import pytest

from pylcg import preferences


__author__ = "Eric Dose :: New Mexico Mira Project, Albuquerque"

PYLCG_ROOT_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEST_TOP_DIRECTORY = os.path.join(PYLCG_ROOT_DIRECTORY, "test")
TEST_PREFERENCES_INI_FULLPATH = os.path.join(TEST_TOP_DIRECTORY, '$data_for_test', 'preferences.ini')

TEST_PREFERENCES_INI_TEXT = """
# /test/$data_for_test/preferences.ini
[Format preferences]
Plot height = 701
Plot width = 125
Plot style = goobers
Show Errorbars = Yes
Show Grid = Yes

[Data preferences]
Bands = B,V,R,I
Days = 250
Last Upload File =
Last Observer HighLighted =
Observer List Columns = Obscode,Name,Count,MoreGoobers"""


HELPER_FUNCTIONS______________________ = 0


def refresh_preferences_ini_file(filepath=TEST_PREFERENCES_INI_FULLPATH):
    with open(filepath, "w") as f:
        f.write(TEST_PREFERENCES_INI_TEXT)


def configs_are_equal(config_1, config_2):
    """   # Helper function for testing."""
    if set(config_1.sections()) != set(config_2.sections()):
        return False
    for section in config_1.sections():
        if set(config_1[section].items()) != set(config_2[section].items()):
            return False
    return True


FUNCTION_TESTS_______________ = 0


# def test_copy_config_dict():
#     # OK 20180823.
#     # Make config_dicts
#     section1 = OrderedDict([('option1', '1'), ('option2', '2')])
#     section2 = OrderedDict([('optiona', 'a'), ('optionb', 'b'), ('optionx', 'x')])
#     cd = OrderedDict([('section1', section1), ('section2', section2)])
#     cd_copy = preferences.copy_config_dict(cd)
#     # Test correctness:
#     assert config_dicts_are_equal(cd_copy, cd)


# def test_update_config_dict():
#     # Make config_dicts:
#     section1 = OrderedDict([('option1', '1'), ('option2', '2')])
#     section2 = OrderedDict([('optiona', 'a'), ('optionb', 'b'), ('optionx', 'x')])
#     cd_base = OrderedDict([('section1', section1), ('section2', section2)])
#     sectionx = OrderedDict([('option1', 'new_1')])
#     sectiony = OrderedDict([('optiona', 'new_a'), ('optionb', ''), ('optionx', 'new_x')])
#     cd_new_values = OrderedDict([('section1', sectionx), ('section2', sectiony)])
#     cd_updated = preferences.update_config_dict(cd_base, cd_new_values)
#     # Test correctness:
#     section1_target = OrderedDict([('option1', 'new_1'), ('option2', '2')])
#     section2_target = OrderedDict([('optiona', 'new_a'), ('optionb', 'b'), ('optionx', 'new_x')])
#     cd_target = OrderedDict([('section1', section1_target), ('section2', section2_target)])
#     assert config_dicts_are_equal(cd_updated, cd_target)


def test_extract_ordered_dict_from_config():
    # OK 20180823.
    config_text = """
    [Section 1]
      One option = xxx
    [Section 23]
      Another option = wxyz
      Yet another = 480
    """
    config = ConfigParser()
    config.read_string(config_text)
    assert config['Section 23']['Yet another'] == '480'
    config_dict = preferences.extract_ordered_dict_from_config(config)
    # NB: ConfigParser option keys always set to LOWER CASE, no matter how the user specifies them. Sigh.
    config_dict_target = OrderedDict([
        ('Section 1',  OrderedDict([('one option', 'xxx')])),
        ('Section 23', OrderedDict([('another option', 'wxyz'), ('yet another', '480')]))])
    config_target = ConfigParser()
    config_target.read_dict(config_dict_target)
    assert configs_are_equal(config, config_target)


def test_copy_config():
    # OK 20180823.
    config_text = """
    [Section 1]
      One option = xxx
    [Section 23]
      Another option = wxyz
      Yet another = 480
    """
    config = ConfigParser()
    config.read_string(config_text)
    assert config['Section 23']['Yet another'] == '480'
    config_copy = preferences.copy_config(config)
    assert configs_are_equal(config_copy, config)
    assert config_copy is not config


CLASS_TESTS___________________ = 0


def test_invalidkeyerror_exception():
    pass


def test_class_preferences():
    # TODO: refactor this into fns that test individual class methods.

    # Ensure absolutely that test preferences.ini file is as needed for these tests:
    refresh_preferences_ini_file()

    # Begin by testing constructor (which also tests Preferences.load_ini_file()):
    s = preferences.Preferences(preferences_ini_path=TEST_PREFERENCES_INI_FULLPATH)

    # Test basic reads via direct reading from config fields:
    assert s.default_config['Format preferences']['plot height'] == '720'
    assert s.ini_file_config['Format preferences']['plot height'] == '701'
    assert s.current_config['Format preferences']['plot height'] == '701'  # same as ini file, to begin
    assert s.current_config['Data preferences']['bands'] == 'B,V,R,I'
    assert s.default_config['Data preferences']['bands'] == 'B,V,R,I,Vis'

    # Test reading current preferences via API (as always recommended), values from .current_config:
    assert s.get('Format preferences', 'pLot hEIGht') == '701'  # option key is case-insensitive
    assert s.get('Data preferences', 'bands') == 'B,V,R,I'

    # Change a preference via API (not directly into dict as class element):
    s.set('Format preferences', 'plot height', 650)
    assert s.get('Format preferences', 'plot height') == '650'  # was changed
    assert s.default_config['Format preferences']['plot height'] == '720'  # unchanged
    assert s.ini_file_config['Format preferences']['plot height'] == '701'  # unchanged

    # Test .reset_current_to_default():
    default_value = s.default_config['Format preferences']['plot height']
    new_value = '12345678xyz=*&^'
    assert default_value != new_value
    s.set('Format preferences', 'plot height', new_value)
    assert s.get('Format preferences', 'plot height') == new_value
    s.reset_current_to_default()
    assert s.get('Format preferences', 'plot height') == default_value

    # Test .write_defaults_to_ini_file(): ___________________________________
    # First, mess up the preferences.ini file:
    good_config = ConfigParser()
    good_config.read_string(preferences.DEFAULT_CONFIG_TEXT)
    bad_config = preferences.copy_config(good_config)
    bad_config['Format preferences']['plot height'] = '12344312^^^^^'
    assert bad_config['Format preferences']['plot height'] != \
           good_config['Format preferences']['plot height']
    with open(s.preferences_ini_path, 'w') as f:
        bad_config.write(f)

    # Verify that preferences.ini file has been messed up:
    config_from_ini_file = ConfigParser()
    config_from_ini_file.read(s.preferences_ini_path)
    assert config_from_ini_file['Format preferences']['plot height'] == \
           bad_config['Format preferences']['plot height']
    assert config_from_ini_file['Format preferences']['plot height'] != \
           good_config['Format preferences']['plot height']

    # Verify that write_defaults_to_ini_file() does reset the file:
    s.write_defaults_to_ini_file()
    config_from_ini_file.read(s.preferences_ini_path)
    assert config_from_ini_file['Format preferences']['plot height'] == \
           good_config['Format preferences']['plot height']

    # Test .write_current_config_to_ini_file():
    s.reset_current_to_default()  # already tested above
    s.write_defaults_to_ini_file()  # already tested above
    default_plot_height = s.get('Format preferences', 'plot height')
    s.set('Format preferences', 'plot height', 'XXX123XXX')  # change to current config
    new_plot_height = s.get('Format preferences', 'plot height')
    assert new_plot_height != default_plot_height  # verify current config changed
    s.write_current_config_to_ini_file()

    config_saved = ConfigParser()
    config_saved.read(s.preferences_ini_path)
    plot_height_saved = config_saved['Format preferences']['plot height']
    assert plot_height_saved == new_plot_height
    assert plot_height_saved != default_plot_height

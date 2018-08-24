import os
from collections import OrderedDict
from configparser import ConfigParser

import pytest

from pylcg import settings



__author__ = "Eric Dose :: New Mexico Mira Project, Albuquerque"

PYLCG_ROOT_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEST_TOP_DIRECTORY = os.path.join(PYLCG_ROOT_DIRECTORY, "test")
TEST_SETTINGS_INI_FULLPATH = os.path.join(TEST_TOP_DIRECTORY, '$data_for_test', 'settings.ini')

test_settings_ini_text = """
# /test/$data_for_test/settings.ini
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


def refresh_settings_ini_file(filepath=TEST_SETTINGS_INI_FULLPATH):
    with open(filepath, "w") as f:
        f.write(test_settings_ini_text)


def config_dicts_are_equal(cd_1, cd_2):
    # Helper function for testing.
    assert len(cd_2.items()) == len(cd_1.items())
    for section in cd_2.keys():
        if not len(cd_2[section].items()) == len(cd_1[section].items()):
            return False
        for key in cd_2[section].keys():
            if not cd_2[section][key] == cd_1[section][key]:
                return False
    return True


FUNCTION_TESTS_______________ = 0


def test_copy_config_dict():
    # OK 20180823.
    # Make config_dicts
    section1 = OrderedDict([('option1', '1'), ('option2', '2')])
    section2 = OrderedDict([('optiona', 'a'), ('optionb', 'b'), ('optionx', 'x')])
    cd = OrderedDict([('section1', section1), ('section2', section2)])
    cd_copy = settings.copy_config_dict(cd)
    # Test correctness:
    assert config_dicts_are_equal(cd_copy, cd)


def test_update_config_dict():
    # Make config_dicts:
    section1 = OrderedDict([('option1', '1'), ('option2', '2')])
    section2 = OrderedDict([('optiona', 'a'), ('optionb', 'b'), ('optionx', 'x')])
    cd_base = OrderedDict([('section1', section1), ('section2', section2)])
    sectionx = OrderedDict([('option1', 'new_1')])
    sectiony = OrderedDict([('optiona', 'new_a'), ('optionb', ''), ('optionx', 'new_x')])
    cd_new_values = OrderedDict([('section1', sectionx), ('section2', sectiony)])
    cd_updated = settings.update_config_dict(cd_base, cd_new_values)
    # Test correctness:
    section1_target = OrderedDict([('option1', 'new_1'), ('option2', '2')])
    section2_target = OrderedDict([('optiona', 'new_a'), ('optionb', 'b'), ('optionx', 'new_x')])
    cd_target = OrderedDict([('section1', section1_target), ('section2', section2_target)])
    assert config_dicts_are_equal(cd_updated, cd_target)


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
    config_dict = settings.extract_ordered_dict_from_config(config)
    # NB: ConfigParser option keys always set to LOWER CASE, no matter how the user specifies them. Sigh.
    config_dict_target = OrderedDict([
        ('Section 1',  OrderedDict([('one option', 'xxx')])),
        ('Section 23', OrderedDict([('another option', 'wxyz'), ('yet another', '480')]))])
    assert config_dicts_are_equal(config_dict, config_dict_target)


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
    config_copy = settings.copy_config(config)
    assert config_dicts_are_equal(config_copy, config)


CLASS_TESTS___________________ = 0


def test_settings_keyerror_exception():
    pass


def test_class_settings():
    # TODO: refactor this into fns that test individual class methods.

    # Ensure absolutely that test settings.ini file is as needed for these tests:
    refresh_settings_ini_file()

    # Begin by testing constructor (which also tests Settings.load_ini_file()):
    s = settings.Settings(settings_ini_path=TEST_SETTINGS_INI_FULLPATH)

    # Test basic reads and merges (read via dicts, NOT recommended outside of this testing):
    assert s.default_dict['Format preferences']['plot height'] == '720'
    assert s.ini_file_dict['Format preferences']['plot height'] == '701'
    assert s.current_dict['Format preferences']['plot height'] == '701'  # same as ini file, to begin
    assert s.default_dict['Data preferences']['bands'] == 'B,V,R,I,Vis'
    assert s.current_dict['Data preferences']['bands'] == 'B,V,R,I'  # from test settings.ini

    # Test reading current settings via API (as always recommended):
    assert s.get('Format preferences', 'pLot hEIGht') == '701'  # option key is case-insensitive
    assert s.get('Data preferences', 'bands') == 'B,V,R,I'

    # Change a setting via API (not directly into dict as class element):
    s.set('Format preferences', 'plot height', 650)
    assert s.default_dict['Format preferences']['plot height'] == '720'  # unchanged
    assert s.ini_file_dict['Format preferences']['plot height'] == '701'  # unchanged
    assert s.get('Format preferences', 'plot height') == '650'  # changed

    # Test .set_current_config_to_default_config():
    s.set('Format preferences', 'plot height', '12345678xyz=*&^')
    assert s.get('Format preferences', 'plot height') != s.default_dict['Format preferences']['plot height']
    s.set_current_config_to_default_config()
    assert s.get('Format preferences', 'plot height') == s.default_dict['Format preferences']['plot height']

    # Test .reset_ini_file_to_defaults(): ___________________________________
    # First, mess up the settings.ini file:
    good_config = ConfigParser()
    good_config.read_string(settings.DEFAULT_CONFIG_TEXT)
    bad_config = settings.copy_config(good_config)
    bad_config['Format preferences']['plot height'] = '12344312^^^^^'
    assert bad_config['Format preferences']['plot height'] != \
           good_config['Format preferences']['plot height']
    with open(s.settings_ini_path, 'w') as f:
        bad_config.write(f)

    # Verify that settings.ini file has been messed up:
    config_from_ini_file = ConfigParser()
    config_from_ini_file.read(s.settings_ini_path)
    assert config_from_ini_file['Format preferences']['plot height'] == \
           bad_config['Format preferences']['plot height']
    assert config_from_ini_file['Format preferences']['plot height'] != \
           good_config['Format preferences']['plot height']

    # Verify that reset_ini_file_to_defaults() does reset the file:
    s.reset_ini_file_to_defaults()
    config_from_ini_file.read(s.settings_ini_path)
    assert config_from_ini_file['Format preferences']['plot height'] == \
           good_config['Format preferences']['plot height']

    # Test .save_current_config_to_ini_file():
    s.set_current_config_to_default_config()  # already tested above
    s.reset_ini_file_to_defaults()  # already tested above
    default_plot_height = s.get('Format preferences', 'plot height')
    s.set('Format preferences', 'plot height', 'XXX123XXX')  # change to current config
    new_plot_height = s.get('Format preferences', 'plot height')
    assert new_plot_height != default_plot_height  # verify current config changed
    s.save_current_config_to_ini_file()

    config_saved = ConfigParser()
    config_saved.read(s.settings_ini_path)
    plot_height_saved = config_saved['Format preferences']['plot height']
    assert plot_height_saved == new_plot_height
    assert plot_height_saved != default_plot_height

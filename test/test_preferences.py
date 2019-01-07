import os
from collections import OrderedDict
from configparser import ConfigParser

# import pytest

from pylcg import preferences as pr

__author__ = "Eric Dose :: New Mexico Mira Project, Albuquerque"

TEST_TOP_DIRECTORY = os.path.dirname(os.path.abspath(__file__))  # the dir holding this (test) .py file.
TEST_DATA_DIRECTORY = os.path.join(TEST_TOP_DIRECTORY, '$data_for_test')
TEST_PREFERENCES_INI_FULLPATH = os.path.join(TEST_DATA_DIRECTORY, 'preferences.ini')
# INI_FILE_SECTION_NAME = pr.INI_FILE_SECTION_NAME
TEST_INI_SECTION_NAME = 'This is the Test Ini Section Name'

HELPER_FUNCTIONS____________________________ = 0


def write_prefset_to_ini_file_for_testing_only(prefset, ini_file_fullpath):
    # Simple function to avoid calling Prefset.write_to_ini_file(), which itself we need to test below.
    config = ConfigParser()
    config[prefset.ini_section_name] = prefset.ordered_dict
    with open(ini_file_fullpath, 'w') as f:
        config.write(f)


TEST_FUNCTIONS____________________________ = 0


class TestClassPrefset:
    def test_init(self):
        # Test native .__init__():
        # Case: return None for absent argument:
        prefset = pr.Prefset()
        assert prefset.ordered_dict is None
        # Case: return new Prefset for proper argument, and must contain a *copy* of argument:
        test_ordered_dict = OrderedDict([('key1', 'value1'), ('keytwo', 'valuetwo')])
        prefset = pr.Prefset(test_ordered_dict)
        assert isinstance(prefset, pr.Prefset)
        assert prefset.ordered_dict == test_ordered_dict
        assert prefset.ordered_dict is not test_ordered_dict

    def test_copy(self):
        test_ordered_dict = OrderedDict([('key1', 'value1'), ('keytwo', 'valuetwo')])
        prefset = pr.Prefset(test_ordered_dict)
        prefset_copy = prefset.copy()
        assert prefset.ordered_dict == prefset_copy.ordered_dict
        assert prefset.ordered_dict is not prefset_copy.ordered_dict

    def test_as_updated_by(self):
        # Case: update with OrderedDict object:
        test_ordered_dict = OrderedDict([('key1', 'value1'), ('keytwo', 'valuetwo')])
        test_prefset = pr.Prefset(test_ordered_dict, ini_section_name='Original Section Name')
        updates_ordered_dict = OrderedDict([('keytwo', 'muahaha'), ('cle_trois', 'donnee_3')])
        new_prefset = test_prefset.as_updated_by(updates_ordered_dict)
        expected_prefset = pr.Prefset(OrderedDict([('key1', 'value1'), ('keytwo', 'muahaha'),
                                                   ('cle_trois', 'donnee_3')]), 'Original Section Name')
        assert new_prefset.ordered_dict == expected_prefset.ordered_dict
        assert new_prefset.ordered_dict is not expected_prefset.ordered_dict
        assert new_prefset.ini_section_name == expected_prefset.ini_section_name
        # Case: update with Prefset object:
        test_ordered_dict = OrderedDict([('key1', 'value1'), ('keytwo', 'valuetwo')])
        test_prefset = pr.Prefset(test_ordered_dict, ini_section_name='Original Section Name')
        updates_prefset = pr.Prefset(OrderedDict([('keytwo', 'muahaha'), ('cle_trois', 'donnee_3')]),
                                     'Updates Section Name')
        new_prefset = test_prefset.as_updated_by(updates_prefset)
        expected_prefset = pr.Prefset(OrderedDict([('key1', 'value1'), ('keytwo', 'muahaha'),
                                                   ('cle_trois', 'donnee_3')]), 'Original Section Name')
        assert new_prefset.ordered_dict == expected_prefset.ordered_dict
        assert new_prefset.ordered_dict is not expected_prefset.ordered_dict
        assert new_prefset.ini_section_name == expected_prefset.ini_section_name

    def test_from_ini_file(self):
        # Case 1a: fullpath is missing from call:
        prefset = pr.Prefset.from_ini_file()
        assert prefset is None

        # Case 1b: no such .ini file available:
        test_ini_fullpath = os.path.join(TEST_DATA_DIRECTORY, 'not_existXXX.ini')
        prefset = pr.Prefset.from_ini_file(test_ini_fullpath)
        assert prefset is None

        # Case 1c: .ini file cannot be parsed (is not really an .ini file):
        test_ini_fullpath = os.path.join(TEST_DATA_DIRECTORY, 'not_an_ini_file.ini')
        prefset = pr.Prefset.from_ini_file(test_ini_fullpath)
        assert prefset is None

        # Case 2: full .ini file is available:
        # Ensure target file is absent:
        test_ini_fullpath = os.path.join(TEST_DATA_DIRECTORY, 'test_from.ini')
        try:
            os.remove(test_ini_fullpath)
        except OSError:
            pass
        # Make Prefset and write to file:
        test_prefset = pr.Prefset(OrderedDict([('key1', 'value1'), ('keytwo', 'valuetwo')]),
                                  'Test Section Name')
        write_prefset_to_ini_file_for_testing_only(test_prefset, test_ini_fullpath)
        # Read .ini file back in & test it:
        prefset_read_in = pr.Prefset.from_ini_file(test_ini_fullpath)
        assert prefset_read_in.ordered_dict == test_prefset.ordered_dict
        assert prefset_read_in.ordered_dict is not test_prefset.ordered_dict
        assert prefset_read_in.ini_section_name == test_prefset.ini_section_name

    def test_write_to_ini_file(self):
        test_ini_fullpath = os.path.join(TEST_DATA_DIRECTORY, 'test_write_to.ini')
        # Ensure target file is absent:
        try:
            os.remove(test_ini_fullpath)
        except OSError:
            pass
        # Make Prefset and write to file:
        test_prefset = pr.Prefset(OrderedDict([('key1', 'value1'), ('keytwowww', 'valuetwoXXX')]),
                                  'Test Section Name ZZZ')
        test_prefset.write_to_ini_file(test_ini_fullpath)
        # Read .ini file back in & test it:
        prefset_read_in = pr.Prefset.from_ini_file(test_ini_fullpath)
        assert prefset_read_in.ordered_dict == test_prefset.ordered_dict
        assert prefset_read_in.ordered_dict is not test_prefset.ordered_dict
        assert prefset_read_in.ini_section_name == test_prefset.ini_section_name

    def test_set(self):
        test_prefset = pr.Prefset(OrderedDict([('key1', 'value1'), ('keytwowww', 'valuetwoXXX')]),
                                  'Test Section Name SET')
        # Normal Case: item to set already exists (change item):
        changed_prefset = test_prefset.copy()
        successful = changed_prefset.set('keytwowww', 'new value WWW')  # changes in place
        expected_prefset = pr.Prefset(OrderedDict([('key1', 'value1'), ('keytwowww', 'new value WWW')]),
                                      'Test Section Name SET')
        assert successful is True
        assert changed_prefset.ordered_dict == expected_prefset.ordered_dict
        assert changed_prefset.ordered_dict is not expected_prefset.ordered_dict
        assert changed_prefset.ini_section_name == expected_prefset.ini_section_name
        # Other Case: item to set does not previously exist (NO CHANGE):
        changed_prefset = test_prefset.copy()
        successful = changed_prefset.set('new key G', 'new value V')  # changes in place
        expected_prefset = test_prefset.copy()  # NO CHANGE when new key not in existing keys.
        assert successful is False
        assert changed_prefset.ordered_dict == expected_prefset.ordered_dict
        assert changed_prefset.ordered_dict is not expected_prefset.ordered_dict
        assert changed_prefset.ini_section_name == expected_prefset.ini_section_name

    def test_get(self):
        test_prefset = pr.Prefset(OrderedDict([('key1', 'value1 A'), ('keytwohaha', 'valuetwo B')]),
                                  'Test Section Name GET')
        # Case: key is in existing keys:
        assert test_prefset.get('key1') == 'value1 A'
        assert test_prefset.get('keytwohaha') == 'valuetwo B'
        # Case: key is absent from existing keys:
        assert test_prefset.get('this key is absent') is None
        assert test_prefset.get('') is None
        assert test_prefset.get(None) is None

import os
from datetime import datetime, timezone, timedelta
from math import nan, isnan

import pytest

from pylcg import util

__author__ = "Eric Dose :: New Mexico Mira Project, Albuquerque"

PYLCG_ROOT_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEST_TOP_DIRECTORY = os.path.join(PYLCG_ROOT_DIRECTORY, "test")

HELPER_FUNCTIONS______________________ = 0


FUNCTION_TESTS_______________ = 0


def test_make_safe_star_id():
    assert util.make_safe_star_id('Alcor') == 'Alcor'
    assert util.make_safe_star_id('000-BFD-123') == '000-BFD-123'
    assert util.make_safe_star_id('ST Tri') == 'ST+Tri'
    assert util.make_safe_star_id('1RXS J064434.5+334451') == '1RXS+J064434.5%2B334451'


def test_jd_from_datetime_utc():
    """  This test imported from test_util.py of photrix (E. Dose)."""
    one_second = 1.0 / (24.0 * 3600.0)  # tolerance of 1 second, in days (for JD)
    datetime_j2000 = datetime(2000, 1, 1, 0, 0, 0).replace(tzinfo=timezone.utc)
    assert util.jd_from_datetime_utc(datetime_j2000) == pytest.approx(2451544.5, abs=one_second)

    assert util.jd_from_datetime_utc(None) is None
    assert util.jd_from_datetime_utc() is None

    datetime_1 = datetime(2017, 1, 9, 15, 23, 53).replace(tzinfo=timezone.utc)
    assert util.jd_from_datetime_utc(datetime_1) == pytest.approx(2457763.14158398, abs=one_second)
    datetime_2 = datetime(2020, 7, 9, 6, 23, 53).replace(tzinfo=timezone.utc)
    assert util.jd_from_datetime_utc(datetime_2) == pytest.approx(2459039.76658403, abs=one_second)
    datetime_3 = datetime(1986, 10, 11, 3, 12, 7).replace(tzinfo=timezone.utc)
    assert util.jd_from_datetime_utc(datetime_3) == pytest.approx(2446714.63341273, abs=one_second)


def test_jd_from_mmddyyyy():
    # Normal cases:
    assert util.jd_from_mmddyyyy('02/04/2018') == \
           util.jd_from_datetime_utc(datetime(2018, 2, 4).replace(tzinfo=timezone.utc))
    # Error cases (return None):
    assert util.jd_from_mmddyyyy('02.04/2018') is None
    assert util.jd_from_mmddyyyy('04/2018') is None
    assert util.jd_from_mmddyyyy('00/04/2018') is None
    assert util.jd_from_mmddyyyy('02/33/2018') is None
    assert util.jd_from_mmddyyyy('02/3.5/2018') is None
    assert util.jd_from_mmddyyyy('02/04/-5') is None


def test_jd_from_ddmmyyyy():
    # Normal cases:
    assert util.jd_from_ddmmyyyy('04-02-2018') == \
           util.jd_from_datetime_utc(datetime(2018, 2, 4).replace(tzinfo=timezone.utc))
    assert util.jd_from_ddmmyyyy('04.02.2018') == \
           util.jd_from_datetime_utc(datetime(2018, 2, 4).replace(tzinfo=timezone.utc))
    assert util.jd_from_ddmmyyyy('02-04-1915') == \
           util.jd_from_datetime_utc(datetime(1915, 4, 2).replace(tzinfo=timezone.utc))
    assert util.jd_from_ddmmyyyy('02-04-1915') == \
           util.jd_from_datetime_utc(datetime(1915, 4, 2).replace(tzinfo=timezone.utc))
    # Error cases (return None):
    assert util.jd_from_ddmmyyyy('02.04/2018') is None
    assert util.jd_from_ddmmyyyy('04-2018') is None
    assert util.jd_from_ddmmyyyy('00-04-2018') is None
    assert util.jd_from_ddmmyyyy('02-33-2018') is None
    assert util.jd_from_ddmmyyyy('02-3-4-2018') is None


def test_jd_from_any_date_string():
    # Normal cases:
    assert util.jd_from_any_date_string('04/02/2018') == \
           util.jd_from_datetime_utc(datetime(2018, 4, 2).replace(tzinfo=timezone.utc))
    assert util.jd_from_any_date_string('02.04.2018') == \
           util.jd_from_datetime_utc(datetime(2018, 4, 2).replace(tzinfo=timezone.utc))
    assert util.jd_from_any_date_string('02-04-2018') == \
           util.jd_from_datetime_utc(datetime(2018, 4, 2).replace(tzinfo=timezone.utc))
    # Error cases (return None):
    assert util.jd_from_any_date_string('13/02/2018') is None
    assert util.jd_from_any_date_string('04-13-2018') is None
    assert util.jd_from_any_date_string('04-13-2018') is None


def test_get_star_ids_from_upload_file():
    # Test on valid Extended format upload file:
    # Necessarily this more or less repeats the function, but at least backs up against code corruption.
    filename = 'AAVSOreport-20180813.txt'
    fullpath = os.path.join(TEST_TOP_DIRECTORY, '$data_for_test', filename)
    with open(fullpath) as f:
        lines = f.readlines()
    delimiter = ','  # known for this test upload file.
    star_ids_read_directly = []
    for line in lines:
        if not line.strip().startswith('#'):
            star_ids_read_directly.append(line.strip().split(delimiter)[0].strip())
    star_ids_from_fn = util.get_star_ids_from_upload_file(fullpath)
    assert set(star_ids_read_directly) == set(star_ids_from_fn)

    # Test with valid Visual format upload file:
    filename = 'Visual_upload_1.txt'
    fullpath = os.path.join(TEST_TOP_DIRECTORY, '$data_for_test', filename)
    star_ids_from_fn = util.get_star_ids_from_upload_file(fullpath)
    known_star_ids = ['SS CYG', 'XX XXX']
    assert set(star_ids_from_fn) == set(known_star_ids)

    # Test with file that is not an upload:
    filename = 'preferences.ini'
    fullpath = os.path.join(TEST_TOP_DIRECTORY, '$data_for_test', filename)
    assert util.get_star_ids_from_upload_file(fullpath) == []


def test_class_minidataframe():
    # Test main constructor failures:
    d = None
    assert util.MiniDataFrame(d).dict is None
    d = 'x'  # not a dict
    assert util.MiniDataFrame(d).dict is None
    d = ['x']  # not a dict
    assert util.MiniDataFrame(d).dict is None
    d = {'x'}  # a set, not a dict
    assert util.MiniDataFrame(d).dict is None
    d = {}  # no keys
    assert util.MiniDataFrame(d).dict is None
    d = {'a': [1, 2], 'b': 'x'}  # 2nd value not a list
    assert util.MiniDataFrame(d).dict is None
    d = {'a': [1, 2], 'b': ['x']}  # lists of unequal length
    assert util.MiniDataFrame(d).dict is None

    # Test valid construction from dict/OrderedDict & methods.
    d = {'a': [1, 2, 3], 'b': ['x', 'y', 'z']}
    mdf = util.MiniDataFrame(d)
    assert mdf.ncol() == 2
    assert mdf.len() == 3
    assert set(mdf.column_names()) == {'a', 'b'}
    assert mdf.column('a') == [1, 2, 3]

    # Test .set_column():
    d = {'a': [1, 2, 3], 'b': ['x', 'y', 'z']}
    mdf = util.MiniDataFrame(d)
    mdf.set_column('new', [6, 7, 8])
    assert set(mdf.column_names()) == {'a', 'b', 'new'}
    assert mdf.column('a') == [1, 2, 3]
    assert mdf.column('new') == [6, 7, 8]
    mdf.set_column('a', [66, 77, 88])
    assert set(mdf.column_names()) == {'a', 'b', 'new'}
    assert mdf.column('a') == [66, 77, 88]
    assert mdf.column('new') == [6, 7, 8]

    # Test .row_subset():
    d = {'a': [1, 2, 3, 4, 5], 'b': ['x', 'y', 'z', 'zz', 'zzz']}
    mdf = util.MiniDataFrame(d)
    selection = [len(item) <= 1 for item in mdf.column('b')]
    assert selection == [True, True, True, False, False]
    mdf2 = mdf.row_subset(selection)
    assert set(mdf.column_names()) == set(mdf2.column_names())
    assert mdf2.column('a') == [1, 2, 3]
    assert mdf2.column('b') == ['x', 'y', 'z']

    # Test .to_float():
    d = {'a': ['1.1', 2, '', 'x', '5'], 'b': ['x', 'y', 'z', 'zz', 'zzz']}
    mdf = util.MiniDataFrame(d)
    col_a = mdf.column('a')
    assert col_a[0] != 1.1
    assert col_a[1] == 2.0
    assert col_a[4] != 5.0
    mdf.to_float('a')
    col_a = mdf.column('a')
    is_nan = [isnan(x) for x in col_a]
    assert is_nan == [False, False, True, True, False]
    assert col_a[0] == 1.1
    assert col_a[1] == 2.0
    assert col_a[4] == 5.0
    assert mdf.column('b') == ['x', 'y', 'z', 'zz', 'zzz']


def test_class_targetlist():
    tl = util.TargetList()
    assert tl.is_empty() is True
    assert tl.n() == 0
    assert tl.prev_exists() is False
    assert tl.next_exists() is False
    assert tl.current() is None
    assert tl.go_next() is None
    assert tl.go_prev() is None
    tl.add('ST Tri')
    assert tl.n() == 1
    assert tl.prev_exists() is False
    assert tl.next_exists() is False
    assert tl.current() == 'ST Tri'
    assert tl.go_prev() is None
    assert tl.current() == 'ST Tri'
    assert tl.go_next() is None
    assert tl.current() == 'ST Tri'

    one_target = 'xyz'
    tl = util.TargetList(one_target)
    assert tl.is_empty() is False
    assert tl.n() == 1
    assert tl.prev_exists() is False
    assert tl.next_exists() is False
    assert tl.current() == one_target
    assert tl.go_prev() is None
    assert tl.go_next() is None
    tl.add('ST Tri')
    assert tl.n() == 2
    assert tl.prev_exists() is True
    assert tl.next_exists() is False
    assert tl.current() == 'ST Tri'
    assert tl.go_prev() == one_target
    assert tl.current() == one_target
    assert tl.go_next() == 'ST Tri'
    assert tl.current() == 'ST Tri'

    several_targets = ['first', 'a', 'b', 'c', 'd e4', 'last']
    tl = util.TargetList(several_targets)
    assert tl.is_empty() is False
    assert tl.n() == len(several_targets)
    assert tl.prev_exists() is False
    assert tl.next_exists() is True
    assert tl.current() == several_targets[0]
    assert tl.go_prev() is None
    assert tl.go_next() == several_targets[1]
    assert tl.go_next() == several_targets[2]
    tl.add('ST Tri')
    assert tl.current() is 'ST Tri'
    assert tl.go_prev() == several_targets[2]
    assert tl.go_prev() == several_targets[1]
    assert tl.go_prev() == several_targets[0]
    assert tl.go_prev() is None
    assert tl.current() == several_targets[0]
    for i in range(len(several_targets)):
        assert tl.go_next() == ['first', 'a', 'b', 'ST Tri', 'c', 'd e4', 'last'][i + 1]
    assert tl.prev_exists() is True
    assert tl.next_exists() is False
    assert tl.go_next() is None

    # Pathological cases:
    # Add an empty list:
    tl = util.TargetList()
    tl.add([])
    assert tl.is_empty()
    several_targets = ['first', 'a', 'b', 'c', 'd e4', 'last']
    tl = util.TargetList(several_targets)
    tl.add([])
    assert tl.n() == len(several_targets)

    # Add something neither string nor list:
    tl = util.TargetList(several_targets)
    tl.add(14)
    assert tl.n() == len(several_targets)
    tl.add(16.55)
    assert tl.n() == len(several_targets)










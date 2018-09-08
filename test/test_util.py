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


def test_get_star_ids_from_upload_file():
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

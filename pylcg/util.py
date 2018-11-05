from datetime import datetime, timezone, timedelta
from collections import OrderedDict   # OrderedDict removes duplicates while preserving order
#                                       (NB: in py 3.7+, native python dictionaries will do this too.)
import csv
import urllib.request
from math import nan


__author__ = "Eric Dose :: New Mexico Mira Project, Albuquerque"


def make_safe_star_id(star_id):
    """  Make a star id that is safe to include in a URL.
    :param star_id: star id that may contain spaces or plus signs [string].
    :return: star_id safe to include in a URL [string].
    """
    return star_id.replace("+", "%2B").replace(" ", "+")


def jd_from_datetime_utc(datetime_utc=None):
    """  Converts a UTC datetime to Julian date. Imported from photrix (E. Dose).
    :param datetime_utc: date and time (in UTC) to convert [python datetime object]
    :return: Julian date corresponding to date and time [float].
    """
    if datetime_utc is None:
        return None
    datetime_j2000 = datetime(2000, 1, 1, 0, 0, 0).replace(tzinfo=timezone.utc)
    jd_j2000 = 2451544.5
    seconds_since_j2000 = (datetime_utc - datetime_j2000).total_seconds()
    return jd_j2000 + seconds_since_j2000 / (24*3600)


def datetime_utc_from_jd(jd=None):
    """  Converts a Julian Date to UTC datetime. Imported from photrix (E. Dose).
    :param jd: Julian date to be converted [float].
    :return: UTC datetime from Julian Date [python datetime object].
    """
    if jd is None:
        return datetime.now(timezone.utc)
    datetime_j2000 = datetime(2000, 1, 1, 0, 0, 0).replace(tzinfo=timezone.utc)
    jd_j2000 = 2451544.5
    seconds_since_j2000 = 24 * 3600 * (jd - jd_j2000)
    return datetime_j2000 + timedelta(seconds=seconds_since_j2000)


def jd_now():
    """  Returns Julian date of moment this function is called. Imported from photrix (E. Dose).
    :return: Julian date for immediate present per system clock [float].
    """
    return jd_from_datetime_utc(datetime.now(timezone.utc))


def jd_from_mmddyyyy(date_string):
    """  Get Julian Date from US-format date string.
    :param date_string: US-format UTC date mm/dd/yyyy, e.g. '12/01/2018' (string).
    :return: Julian Date corresponding to date_string (at 00:00:00 UTC).
    """
    substrings = date_string.split('/')
    if len(substrings) != 3:
        return None
    try:
        terms = [int(s) for s in substrings]  # list of integers representing month, day, year
        this_date = datetime(terms[2], terms[0], terms[1], 0, 0, 0).replace(tzinfo=timezone.utc)
    except ValueError:
        return None
    return jd_from_datetime_utc(this_date)


def jd_from_ddmmyyyy(date_string):
    """  Get Julian Date from European-format date string.
    :param date_string: European-format UTC date dd-mm-yyyy or dd.mm.yyyy,
               e.g. '01-20-2018' or '01.20.2018' (string).
    :return: Julian Date corresponding to date_string (at 00:00:00 UTC).
    """
    substrings = date_string.split('-')
    if len(substrings) != 3:
        substrings = date_string.split('.')
        if len(substrings) != 3:
            return None
    try:
        terms = [int(s) for s in substrings]  # list of integers representing month, day, year
        this_date = datetime(terms[2], terms[1], terms[0], 0, 0, 0).replace(tzinfo=timezone.utc)
    except ValueError:
        return None
    return jd_from_datetime_utc(this_date)


def jd_from_any_date_string(date_string):
    """  Parse any legit date string (US, Euro, or JD format), return Julian Date.
    :param date_string: Any legit date in US, Euro, or JD format (string).
    :return: Julian Date (float), or None if error.
    """
    try:
        jd = float(date_string)
    except ValueError:
        jd = None
    if jd is not None:  # is a Julian Date.
        return jd
    jd = jd_from_mmddyyyy(date_string)
    if jd is not None:  # is a US-format date.
        return jd
    return jd_from_ddmmyyyy(date_string)  # is a European-format date, or None if altogether invalid.


def get_star_ids_from_upload_file(fullpath):
    """  Get and return all star ids from a given WebObs upload text file.
    :param fullpath: upload text file name [string].
    :return: list of all star IDs, no duplicates, preserving order found in file [list of strings].
    """
    try:
        with open(fullpath) as f:
            lines = f.readlines()
    except FileNotFoundError:
        return list()

    # Ensure file declares itself to be either Extended or Visual format:
    type_line_found = False
    for line in lines:
        if line.upper().startswith('#TYPE='):
            type_line_found = True
            type_string = line.split('=')[1].strip()
            if type_string.upper() not in ['EXTENDED', 'VISUAL']:
                return list()
    if not type_line_found:
        return list()

    # Get delimiter, comma as default:
    delimiter = ','  # default if #DELIM line not found.
    for line in lines:
        if line.upper().startswith('#DELIM='):
            delimiter = line.split('=')[1].strip()
            if delimiter.lower() == 'comma':
                delimiter = ','
            break

    # Extract and return star_ids:
    lines = [line for line in lines if not line.startswith('#')]  # keep only observation text lines.
    star_ids_as_found = [line.split(delimiter)[0].strip() for line in lines]  # may contain duplicates.
    star_ids = list(OrderedDict.fromkeys(star_ids_as_found))  # no duplicates, order preserved.
    return star_ids


class TargetList:
    """  List of targets to service the Target 'Prev' and 'Next' buttons [list of strings]."""
    def __init__(self, target_or_list=None):
        self.targets = []  # this will become a list of PlotTarget objects.
        self.target_index = None  # points to currently plotted target.
        if target_or_list is not None:
            if isinstance(target_or_list, str):
                self.add([target_or_list])  # handling python's pitiful str/list confusions.
            else:
                self.add(target_or_list)

    def n(self):
        """  Return number of entries."""
        return len(self.targets)

    def is_empty(self):
        return self.n() <= 0

    def add(self, target_or_list=None):
        """  Add a target (string) or target list after current position."""
        if target_or_list is None:
            return
        # Ensure that target(s) comprise a list:
        if isinstance(target_or_list, str):
            new_targets = [target_or_list]  # handling python's pitiful str/list confusions.
        elif isinstance(target_or_list, list):
            if len(target_or_list) == 0:
                return
            new_targets = target_or_list
        else:
            return
        # Insert the list:
        if self.is_empty():
            # Add new targets and point to first one:
            self.targets.extend(new_targets)
            self.target_index = 0
        else:
            # Insert all new targets and point to first one:
            self.targets = self.targets[:self.target_index + 1] + new_targets + \
                           self.targets[self.target_index + 1:]
            self.target_index += 1

    def prev_exists(self):
        """  Return True iff there exists a target just before current position. """
        if self.is_empty() or self.target_index is None:
            return False
        if not (0 < self.target_index <= self.n() - 1):
            return False
        return True

    def next_exists(self):
        """  Return True iff there exists a target just after current position. """
        if self.is_empty() or self.target_index is None:
            return False
        if not (0 <= self.target_index < self.n() - 1):
            return False
        return True

    def go_prev(self):
        """  Go to previous position, and return target found there. """
        if not self.prev_exists():
            return None
        self.target_index -= 1
        return self.targets[self.target_index]

    def go_next(self):
        """  Go to next position, and return target found there. """
        if not self.next_exists():
            return None
        self.target_index += 1
        return self.targets[self.target_index]

    def current(self):
        """  Return target at current position. """
        if self.is_empty() or self.target_index is None:
            return None
        return self.targets[self.target_index]


class Error(Exception):
    pass


class UnequalLengthError(Error):
    pass


class MiniDataFrame:
    """  Tiny subset of pandas DataFrame facility. Holds a dict of equal-length lists.
    """
    def __init__(self, dict_of_lists=None):
        self.dict = dict_of_lists  # even if is None.
        # Verify is a dict or OrderedDict:
        if (not isinstance(dict_of_lists, dict)) and (not isinstance(dict_of_lists, OrderedDict)):
            self.dict = None
        # Verify dict has keys:
        if self.dict is not None:
            keys = list(self.dict.keys())
            if len(keys) == 0:
                self.dict = None
        # Verify all dict values are lists:
        if self.dict is not None:
            for key in keys:
                if not isinstance(self.dict[key], list):
                    self.dict = None
                    break
        # Verify all lists are equal length:
        if self.dict is not None:
            first_length = len(self.dict[keys[0]])
            for key in keys:
                if len(self.dict[key]) != first_length:
                    self.dict = None
                    break
        # Here, self.dict is either valid or None.

    def ncol(self):
        """  Return number of columns."""
        return len(self.column_names())

    def len(self):
        """  Return length of lists, similar to pandas.DataFrame.len()."""
        return len(self.dict[list(self.dict.keys())[0]])

    def column_names(self):
        """  Return list of column names."""
        return list(self.dict.keys())

    def column(self, column_name):
        """  Return list of values in this column. """
        return self.dict[column_name]

    def set_column(self, new_column_name, new_list):
        """  Add or replace column with new_list.
        :param new_column_name: column name to add or replace [string]
        :param new_list: value for new column [list].
        :return: No return; changes this MiniDataFrame object in-place.
        """
        if len(new_list) != self.len():
            raise UnequalLengthError
        else:
            self.dict[new_column_name] = new_list.copy()

    def to_float(self, column_name):
        """  Convert one column's data into floats; if not possible make value math.nan.
        :param column_name: name of column to convert to floats [string].
        :return: No return; changes this MiniDataFrame object in-place.
        """
        floats = []
        for x in self.column(column_name):
            try:
                float_x = float(x)
            except ValueError:
                float_x = nan
            floats.append(float_x)
        self.dict[column_name] = floats

    @staticmethod
    def from_url(url, delimiter):
        """  Constructor: read data from url, parse into MiniDataFrame object, and return it.
        :param url: URL from which to get data [string].
        :param delimiter: delimiter to use in making request [1-character string].
        :return: newly constructed object [MiniDataFrame object].
        """
        # get nested list of data from URL:
        byte_text = urllib.request.urlopen(url)
        text = [line.decode('utf-8') for line in byte_text]
        reader = csv.reader(text, delimiter=delimiter)
        data = [row for row in reader]
        # return data
        # Now, parse nested list into a dict:
        this_dict = dict()
        if len(data) == 0:
            return None
        column_names = []
        for column_name in data[0]:
            column_names.append(column_name)
            this_dict[column_name] = []
        for row in data[1:]:
            for i_col, column_name in enumerate(column_names):
                this_dict[column_name].append(row[i_col])
        return MiniDataFrame(this_dict)

    def row_subset(self, boolean_list):
        """  Return new MiniDataFrame object with rows selected by boolean_list; rows are copies.
        :param boolean_list: True iff row is to be kept in subset [list of booleans,
            length must equal length of this MiniDataFrame.
        :return: subset MiniDataFrame [MiniDataFrame object].
        """
        if len(boolean_list) != self.len():
            return None
        new_dict = OrderedDict()
        for column_name in self.column_names():
            zipped = zip(self.column(column_name), boolean_list)
            new_list = [item for (item, boolean) in zipped if boolean is True]
            new_dict[column_name] = new_list
        return MiniDataFrame(new_dict)

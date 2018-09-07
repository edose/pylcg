from datetime import datetime, timezone

from collections import OrderedDict   # OrderedDict removes duplicates while preserving order
#                                       (NB: in py 3.7+, native python dictionaries will do this too.)

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


def jd_now():
    """  Returns Julian date of moment this function is called. Imported from photrix (E. Dose).
    :return: Julian date for immediate present per system clock [float].
    """
    return jd_from_datetime_utc(datetime.now(timezone.utc))


def get_star_ids_from_upload_file(filename):
    """  Get and return all star ids from a given WebObs upload text file.
    :param filename: upload text file name [string].
    :return: list of all star IDs, no duplicates, preserving order found in file [list of strings].
    """
    with open(filename) as f:
        lines = f.readlines()

    # Get delimiter:
    delimiter = ','  # default if #DELIM line not found.
    for line in lines:
        if line.upper().startswith('#DELIM='):
            delimiter = line.split('=')[1].strip()  # this doesn't yet handle 'comma', etc
            break

    # Extract and return star_ids:
    lines = [line for line in lines if not line.startswith('#')]  # keep only observation text lines.
    star_ids_as_found = [line.split(delimiter)[0].strip() for line in lines]  # may contain duplicates.
    star_ids = list(OrderedDict.fromkeys(star_ids_as_found))  # no duplicates, order preserved.
    return star_ids


class Error(Exception):
    pass


class UnequalLengthError(Error):
    pass


class MiniDataFrame:
    """  Tiny subset of pandas DataFrame facility. Holds a dict of equal-length lists.


    """
    def __init__(self, dict_of_lists):
        self.dict = dict_of_lists
        # Verify is a dict or OrderedDict:
        if (not isinstance(dict_of_lists, dict)) or (not isinstance(dict_of_lists, OrderedDict)):
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

    def column(self, column_name):
        """  Return list. """
        return self.dict[column_name]

    def len(self):
        """  Return length of lists, similar to pandas.DataFrame.len()."""
        return len(self.dict[self.dict.keys()[0]])

    def column_names(self):
        """  Return list of column names."""
        return list(self.dict.keys())

    def ncol(self):
        """  Return number of columns."""
        return len(self.column_names())

    def set_column(self, new_column_name, new_list):
        """  Add or replace column with new_list.
        :param new_column_name: column name to add or replace [string]
        :param new_list: value for new column [list].
        :return:
        """
        if len(new_list) != self.dict.len():
            raise UnequalLengthError
        else:
            self.dict[new_column_name] = new_list.copy()

    def from_url(self, url):
        """  Constructor: read data from url, parse into MiniDataFrame object, and return it.
        :param url: URL from which to get data.
        :return: newly constructed object [MiniDataFrame object].
        """
        pass

    def row_subset(self, boolean_list):
        """  Return new MiniDataFrame object with rows selected by boolean_list; rows are copies.
        :param boolean_list: True iff row is to be kept in subset [list of booleans,
            length must equal length of this MiniDataFrame.
        :return: subset MiniDataFrame [MiniDataFrame object].
        """
        pass

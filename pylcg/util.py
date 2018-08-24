__author__ = "Eric Dose :: New Mexico Mira Project, Albuquerque"

from datetime import datetime, timezone
# OrderedDict removes duplicates while preserving order.
#    (NB: in py 3.7+, native py dictionaries will do this too.)
from collections import OrderedDict


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

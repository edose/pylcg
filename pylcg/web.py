__author__ = "Eric Dose :: New Mexico Mira Project, Albuquerque"

import urllib
import webbrowser

import pandas as pd

import pylcg.util as util

VSX_DELIMITERS = ['$', '`', '^', '%']  # NB: delim of ',' will fail as obsName values already have a comma.
REPO_URL = 'https://www.github.com/edose/pylcg'


class Error(Exception):
    pass


class WebAddressNotAvailableError(Error):
    pass


class NoDataError(Error):
    pass


def get_vsx_obs(star_id, max_num_obs=None, jd_start=None, jd_end=None, num_days=500):
    #  simply returns an pandas dataframe containing data,
    #   no parsing or cacheing. If star ID not in webobs, this returns a dataframe with no rows.
    """
    Downloads observations from AAVSO's webobs for ONE star (not fov), returns pandas dataframe.
       If star not in AAVSO's webobs site, return a dataframe with no rows.
       Columns: target_name, date_string, filter, observer, jd, mag, error.
    :param star_id: the STAR id (not the fov's name).
    :param max_num_obs: maximum number of observations to get [int].  --  NOT YET IMPLEMENTED.
    :param jd_start: optional Julian date.
    :param jd_end: optional JD.
    :return: simple pandas dataframe containing data for 1 star, 1 row per observation downloaded,
        (empty DataFrame if there was some problem).
    """
    url_header = 'https://www.aavso.org/vsx/index.php?view=api.delim'
    parm_ident = '&ident=' + util.make_safe_star_id(star_id)
    if jd_end is None:
        jd_end = util.jd_now()
    parm_tojd = '&tojd=' + '{:20.5f}'.format(jd_end).strip()
    if jd_start is None:
        jd_start = jd_end - num_days
    parm_fromjd = '&fromjd=' + '{:20.5f}'.format(jd_start).strip()

    dataframe = None  # default if all delimiters fail
    df_is_ok = False  # "
    for delimiter in VSX_DELIMITERS:  # we try all limiters until one succeeds or (error) all have failed.
        parm_delimiter = '&delimiter=' + delimiter
        url = url_header + parm_ident + parm_tojd + parm_fromjd + parm_delimiter
        try:
            dataframe = pd.read_csv(url, sep=delimiter)
        except urllib.error.URLError:
            raise WebAddressNotAvailableError(url_header)
        if dataframe_has_data(dataframe):
            if dataframe_data_appear_valid(dataframe):
                df_is_ok = True
                break
    if not df_is_ok:
        raise NoDataError(star_id)
    return dataframe


def dataframe_has_data(dataframe):
    if dataframe is None:
        return False
    if dataframe.shape[0] == 0:
        return False
    return True


def dataframe_data_appear_valid(dataframe):
    if dataframe.shape[1] < 20:
        return False
    if 'uncert' not in dataframe.columns:
        return False
    if not dataframe['uncert'].dtype.name == 'float64':
        return False
    return True


def browse_repo():
    webbrowser.open_new_tab(REPO_URL)
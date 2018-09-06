import urllib
import webbrowser
import functools

import pandas as pd

import pylcg.util as util

__author__ = "Eric Dose :: New Mexico Mira Project, Albuquerque"

VSX_OBSERVATIONS_HEADER = 'https://www.aavso.org/vsx/index.php?view=api.delim'
VSX_DELIMITERS = ['$', '`', '^', '%']  # NB: delim of ',' will fail as obsName values already have a comma.
PYLCG_REPO_URL = 'https://www.github.com/edose/pylcg'
VSX_URL_STUB = 'https://www.aavso.org/vsx/index.php?view=results.get&ident='
WEBOBS_URL_STUB = 'https://www.aavso.org/apps/webobs/results?star='


class Error(Exception):
    pass


class WebAddressNotAvailableError(Error):
    pass


@functools.lru_cache(maxsize=100, typed=False)
def get_vsx_obs(star_id, max_num_obs=None, jd_start=None, jd_end=None, num_days=500):
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
    # url_header = 'https://www.aavso.org/vsx/index.php?view=api.delim'
    parm_ident = '&ident=' + util.make_safe_star_id(star_id)
    if jd_end is None:
        jd_end = util.jd_now()
    parm_tojd = '&tojd=' + '{:20.5f}'.format(jd_end).strip()
    if jd_start is None:
        jd_start = jd_end - num_days
    parm_fromjd = '&fromjd=' + '{:20.5f}'.format(jd_start).strip()

    dataframe = pd.DataFrame()  # empty dataframe if no data (all delimiters tried fail to deliver obs)
    for delimiter in VSX_DELIMITERS:  # we try all limiters until one succeeds or (error) all have failed.
        parm_delimiter = '&delimiter=' + delimiter
        url = VSX_OBSERVATIONS_HEADER + parm_ident + parm_tojd + parm_fromjd + parm_delimiter
        try:
            dataframe = pd.read_csv(url, sep=delimiter)
            # print(url, 'queried.')
        except urllib.error.URLError:
            raise WebAddressNotAvailableError(url)
        if dataframe_has_data(dataframe):
            if dataframe_data_appear_valid(dataframe):
                break
    return dataframe


def dataframe_has_data(dataframe):
    """  Determines whether Dataframe (from observation download) has data in it or not.
    :param dataframe: dataframe to test [pandas Dataframe].
    :return: True iff dataframe has data [boolean].
    """
    if dataframe is None:
        return False
    if dataframe.shape[0] == 0:
        return False
    return True


def dataframe_data_appear_valid(dataframe):
    """  Determines whether Dataframe (from observation download) appears valid for use in pylcg, or not.
    :param dataframe: dataframe to test [pandas Dataframe].
    :return: True iff dataframe appears valid for use in pylcg [boolean].
    """
    if dataframe.shape[1] < 20:
        return False
    if 'uncert' not in dataframe.columns:
        return False
    if not dataframe['uncert'].dtype.name == 'float64':
        return False
    return True


def webbrowse_repo():
    webbrowser.open_new_tab(PYLCG_REPO_URL)


def webbrowse_vsx(star_id):
    url = VSX_URL_STUB + util.make_safe_star_id(star_id)
    webbrowser.open_new_tab(url)


def webbrowse_webobs(star_id):
    url = WEBOBS_URL_STUB + util.make_safe_star_id(star_id)
    webbrowser.open_new_tab(url)

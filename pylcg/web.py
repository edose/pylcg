import urllib
import webbrowser
import functools

import pylcg.util as util

__author__ = "Eric Dose :: New Mexico Mira Project, Albuquerque"

VSX_OBSERVATIONS_HEADER = 'https://www.aavso.org/vsx/index.php?view=api.delim'
VSX_DELIMITERS = ['$', '`', '^', '%']  # NB: delim of ',' will fail as obsName values already have a comma.
PYLCG_REPO_URL = 'https://www.github.com/edose/pylcg'
VSX_URL_STUB = 'https://www.aavso.org/vsx/index.php?view=results.get&ident='
WEBOBS_URL_STUB = 'https://www.aavso.org/apps/webobs/results?star='


@functools.lru_cache(maxsize=100, typed=False)
def get_vsx_obs(star_id, max_num_obs=None, jd_start=None, jd_end=None, num_days=500):
    """
    Downloads observations from AAVSO's webobs for ONE star (not fov), returns MiniDataFrame.
       If star not in AAVSO's webobs site, return a dataframe with no rows.
       Columns: target_name, date_string, filter, observer, jd, mag, error.
    :param star_id: the STAR id (not the fov's name).
    :param max_num_obs: maximum number of observations to get [int].  --  NOT YET IMPLEMENTED.
    :param jd_start: optional Julian date.
    :param jd_end: optional JD.
    :return: MiniDataFrame containing data for 1 star, 1 row per observation downloaded,
        (or None if there was some problem).
    """
    # url_header = 'https://www.aavso.org/vsx/index.php?view=api.delim'
    parm_ident = '&ident=' + util.make_safe_star_id(star_id)
    if jd_end is None:
        jd_end = util.jd_now()
    parm_tojd = '&tojd=' + '{:20.5f}'.format(jd_end).strip()
    if jd_start is None:
        jd_start = jd_end - num_days
    parm_fromjd = '&fromjd=' + '{:20.5f}'.format(jd_start).strip()

    minidataframe = None  # if no data (all delimiters tried fail to deliver obs).
    for delimiter in VSX_DELIMITERS:  # we try all limiters until one succeeds or (error) all have failed.
        parm_delimiter = '&delimiter=' + delimiter
        url = VSX_OBSERVATIONS_HEADER + parm_ident + parm_tojd + parm_fromjd + parm_delimiter
        minidataframe = util.MiniDataFrame.from_url(url, delimiter=delimiter)
        if minidataframe_has_data(minidataframe):
            if minidataframe_data_appear_valid(minidataframe):
                for column_name in ['JD', 'mag', 'uncert']:
                    minidataframe.to_float(column_name)
                break
    return minidataframe


def minidataframe_has_data(minidataframe):
    """  Determines whether MiniDataframe (from observation download) has data in it or not.
    :param minidataframe: minidataframe to test [MiniDataframe object].
    :return: True iff minidataframe has data [boolean].
    """
    if minidataframe.dict is None:
        return False
    if minidataframe.len() == 0:
        return False
    return True


def minidataframe_data_appear_valid(minidataframe):
    """  Determines whether MiniDataframe (from observation download) appears valid for use in pylcg.
    :param minidataframe: minidataframe to test [MiniDataframe object].
    :return: True iff minidataframe appears valid for use in pylcg [boolean].
    """
    if minidataframe.ncol() < 20:
        return False
    for column_name in ['uncert', 'JD', 'mag', 'band']:
        if column_name not in minidataframe.column_names():
            return False
    if not isinstance(minidataframe.column('uncert')[0], str):
        return False
    try:
        _ = float(minidataframe.column('uncert')[0])
    except ValueError:
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

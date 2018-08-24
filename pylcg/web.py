__author__ = "Eric Dose :: New Mexico Mira Project, Albuquerque"

import pandas as pd
import webbrowser

import pylcg.util as util

VSX_DELIMITERS = ['$', '`', '^', '%']  # NB: ',' as delim will fail as all obsName values have comma.
REPO_URL = 'https://www.github.com/edose/pylcg'


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
    for delimiter in VSX_DELIMITERS:
        parm_delimiter = '&delimiter=' + delimiter
        url = url_header + parm_ident + parm_tojd + parm_fromjd + parm_delimiter
        try:
            dataframe = pd.read_csv(url, sep=delimiter)
        except:
            print('...delimiter ' + delimiter + ' gives exception')
            continue
        if dataframe_appears_ok(dataframe):
            break

    if not dataframe_appears_ok(dataframe):
        print('>>>>> all delimiters failed. Stopping right here.')
    return dataframe


def dataframe_appears_ok(dataframe):
    if dataframe is None:
        print('dataframe could not be constructed.')
        return False
    if (dataframe.shape[0] == 0) or (dataframe.shape[1] < 10):
        print('dataframe appears corrupted (size).')
        return False
    if 'uncert' not in dataframe.columns:
        print('dataframe appears corrupted (uncertainties missing).')
        return False
    if not dataframe['uncert'].dtype.name == 'float64':
        print('dataframe appears corrupted (uncertainties not numeric).')
        return False
    return True


def browse_repo():
    webbrowser.open_new_tab(REPO_URL)
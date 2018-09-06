import matplotlib
matplotlib.use('TkAgg')  # this must immediately follow 'import matplotlib', even if IDE complains.

import tkinter as tk
from tkinter import ttk
from math import isnan

import pandas as pd

import pylcg.util as util


__author__ = "Eric Dose :: New Mexico Mira Project, Albuquerque"

BAND_DEFAULT_COLORS = {'V': 'xkcd:kelley green',
                       'R': 'xkcd:ruby',
                       'I': 'xkcd:violet red',
                       'B': 'xkcd:vibrant blue',
                       'Vis.': 'xkcd:almost black'}
BAND_DEFAULT_COLOR_DEFAULT = 'gray'
BAND_MARKERS = {'V': 'o', 'R': 'o', 'I': 'o', 'B': 'o', 'Vis.': 'v'}
BAND_MARKERS_DEFAULT = 'x'

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)
PLOT_TITLE_FONT = ('consolas', 20)
PLOT_TITLE_COLOR = 'gray'
GRID_COLOR = 'lightgray'


def redraw_plot(canvas, df, star_id, bands_to_plot,
                show_errorbars=True, show_grid=True,
                jd_start=None, jd_end=None, num_days=None):
    """  Reformat data for matplotlib, then clear and redraw plot area only, and trigger replacement of
    the old plot by the new plot within the containing tkinter Frame.
    Do not touch other areas of main page, and do not change any external data.
    :param canvas: canvas containing LCG plot [matplotlib FigureCanvasTkAgg object].
    :param df: data to plot [pandas DataFrame].
    :param star_id: star ID to plot [string].
    :param bands_to_plot: AAVSO codes of bands to draw, e.g., ['V', 'Vis.'] [list of strings].
    :param show_errorbars: True to plot errorbars with datapoints, else False [boolean].
    :param show_grid: True to plot grid behind plot, else False [boolean].
    ==== User, via the GUI, needs to supply 2 of the following 3 values to define x-range of plot:
    :param jd_start: JD to be at plot's left edge [float].
    :param jd_end:  JD to be at plot's right edge, often the current JD [float].
    :param num_days:  number of days to plot [int or float]
    :return [None]
    """
    if len(df) <= 0:
        message_popup('No observations found for ' + star_id + ' in this date range.')
        return False

    # Build plot data:
    x = df['JD']
    y = df['mag']
    uncert = [0.0 if isnan(u) else float(u) for u in df['uncert']]  # set any unknown uncertainties to zero.
    uncert = [max(0.0, u) for u in uncert]  # cast uncertainties to floats, zero any negatives.
    uncert = pd.Series(uncert)  # a Series, to ensure alignment with x and y during selection in errorbar().

    # Construct plot elements:
    ax = canvas.figure.axes[0]
    ax.clear()
    ax.set_title(star_id.upper(), color=PLOT_TITLE_COLOR, fontname='Consolas', fontsize=16, weight='bold')
    ax.set_xlabel('JD')
    ax.set_ylabel('Magnitude')
    if show_grid:
        ax.grid(True, color=GRID_COLOR, zorder=-1000)  # zorder->behind everything else.
    if show_errorbars:
        is_to_be_drawn = [b in bands_to_plot for b in df['band']]
        ax.errorbar(x=x[is_to_be_drawn], y=y[is_to_be_drawn], xerr=0.0, yerr=uncert[is_to_be_drawn],
                    fmt='none', ecolor='gray', capsize=2, alpha=1,
                    zorder=+900)  # zorder->behind datapoint markers, above grid.
    legend_labels = []
    for band in bands_to_plot:
        band_color = BAND_DEFAULT_COLORS.get(band, BAND_DEFAULT_COLOR_DEFAULT)
        band_marker = BAND_MARKERS.get(band, BAND_MARKERS_DEFAULT)
        is_band = [b == band for b in df['band']]
        if sum(is_band) >= 1:
            ax.scatter(x=x[is_band], y=y[is_band], color=band_color, marker=band_marker,
                       s=25, alpha=0.9, zorder=+1000)  # zorder->on top of everything.
            legend_labels.append(band)
    if jd_end is None:
        x_high = util.jd_now()
    else:
        x_high = jd_end
    if jd_start is None:
        x_low = x_high - num_days
    else:
        x_low = jd_start
    ax.set_xlim(x_low, x_high)
    ax.get_xaxis().get_major_formatter().set_useOffset(False)  # possibly improve this later.
    # To follow convention of brighter (=lesser value) manitudes to be plotted toward plot top.
    # The next lines are a kludge, due to ax.invert_yaxis() repeatedly inverting on successive calls.
    y_low, y_high = ax.set_ylim()
    ax.set_ylim(max(y_low, y_high), min(y_low, y_high))
    ax.legend(labels=legend_labels, scatterpoints=1,
              bbox_to_anchor=(0, 1.02, 1, .102), loc=3, ncol=2, borderaxespad=0)
    canvas.draw()


def quit_and_destroy(window_object):
    """ Both quit() and destroy() are required, at least in Windows, to close a popup window gracefully.
    And program response to a tkinter button press is limited to a single function...so here it is.
    :param window_object: the tkinter window to close [tkinter.Tk object].
    :return [None]
    """
    window_object.quit()
    window_object.destroy()

def message_popup(message):
    """  Draws popup window displaying message to user.
    :param message: the text to display to user [string].
    :return [None]
    """
    this_window = tk.Tk()
    this_window.wm_title('pylcg MESSAGE TO USER')
    label = ttk.Label(this_window, text=message, font=NORM_FONT)
    label.pack(side='top', fill='x', pady=10)
    button_ok = ttk.Button(this_window, text='OK', command=lambda: quit_and_destroy(this_window))
    button_ok.pack()
    this_window.mainloop()

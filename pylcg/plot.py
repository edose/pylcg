import matplotlib
matplotlib.use('TkAgg')  # this must immediately follow 'import matplotlib', even if IDE complains.

from datetime import datetime, timedelta, timezone

import tkinter as tk
from tkinter import ttk
from math import isnan

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
HIGHLIGHT_COLOR = '#ffe090'  # very light orange

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)
PLOT_TITLE_FONT = ('consolas', 20)
PLOT_TITLE_COLOR = 'gray'
GRID_COLOR = 'lightgray'


def redraw_plot(canvas, mdf, star_id, bands_to_plot, show_errorbars=True, show_grid=True,
                show_lessthans=False, observer_selected='',
                highlight_observer=False, plot_observer_only=False,
                plot_in_jd=True, jd_start=None, jd_end=None, num_days=None):
    """  Reformat data for matplotlib, then clear and redraw plot area only, and trigger replacement of
    the old plot by the new plot within the containing tkinter Frame.
    Do not touch other areas of main page, and do not change any external data.
    :param plot_in_jd:
    :param canvas: canvas containing LCG plot [matplotlib FigureCanvasTkAgg object].
    :param mdf: data to plot [MiniDataFrame object].
    :param star_id: star ID to plot [string].
    :param bands_to_plot: AAVSO codes of bands to draw, e.g., ['V', 'Vis.'] [list of strings].
    :param show_errorbars: True to plot errorbars with datapoints, else False [boolean].
    :param show_grid: True to plot grid behind plot, else False [boolean].
    :param show_lessthans: True to plot "less-than" datapoints as normal ones, else omit [boolean].
    :param observer_selected: observer code whose observations to highlight ('' means none) [string].
    :param highlight_observer: True iff observations from obscode_to_highlight to be highlighted [boolean].
    :param plot_observer_only: True iff only observations from obscode_to_highlight to be plotted [boolean].
    :param plot_in_jd: True to plot x-axis in Julian Data, False for US-format calendar dates [boolean].
    ==== User, via the GUI, needs to supply 2 of the following 3 values to define x-range of plot:
    :param jd_start: JD to be at plot's left edge [float].
    :param jd_end:  JD to be at plot's right edge, often the current JD [float].
    :param num_days:  number of days to plot [int or float]
    :return [None]
    """
    if mdf.dict is None:
        message_popup('No observations found for ' + star_id + ' in this date range.')
        return False
    if mdf.len() <= 0:
        message_popup('No observations found for ' + star_id + ' in this date range.')
        return False

    # Clean up uncertainty data:
    uncert = [0.0 if isnan(u) else u for u in mdf.column('uncert')]  # set any missing values to zero.
    uncert = [max(0.0, u) for u in uncert]  # set any negatives to zero.
    mdf.set_column('uncert', uncert)

    # Remove less-than observations if flag dictates:
    if not show_lessthans:
        is_not_lessthan = [f == '0' for f in mdf.column('fainterThan')]
        mdf = mdf.row_subset(is_not_lessthan)

    # Construct plot elements:
    ax = canvas.figure.axes[0]
    ax.clear()
    ax.set_title(star_id.upper(), color=PLOT_TITLE_COLOR, fontname='Consolas', fontsize=16, weight='bold')
    if plot_in_jd:
        ax.set_xlabel('JD')
    else:
        ax.set_xlabel('Date (UTC)')
    ax.set_ylabel('Magnitude')
    if show_grid:
        ax.grid(True, color=GRID_COLOR, zorder=-1000)  # zorder->behind everything else.
    if show_errorbars:
        is_to_be_drawn = [b in bands_to_plot for b in mdf.column('band')]
        mdf_to_be_drawn = mdf.row_subset(is_to_be_drawn)
        if plot_observer_only:
            is_observer = [o.upper() == observer_selected.upper() for o in mdf_to_be_drawn.column('by')]
            mdf_to_be_drawn = mdf_to_be_drawn.row_subset(is_observer)
        ax.errorbar(x=mdf_to_be_drawn.column('JD'), y=mdf_to_be_drawn.column('mag'),
                    xerr=0.0, yerr=mdf_to_be_drawn.column('uncert'),
                    fmt='none', ecolor='gray', capsize=2, alpha=1,
                    zorder=+900)  # zorder->behind datapoint markers, above grid.
    legend_handles, legend_labels = [], []  # defaults if no points to plot
    x_to_highlight, y_to_highlight = [], []
    for band in bands_to_plot:
        band_color = BAND_DEFAULT_COLORS.get(band, BAND_DEFAULT_COLOR_DEFAULT)
        band_marker = BAND_MARKERS.get(band, BAND_MARKERS_DEFAULT)
        is_band = [b == band for b in mdf.column('band')]
        mdf_band = mdf.row_subset(is_band)
        if plot_observer_only:
            is_observer = [o.upper() == observer_selected.upper() for o in mdf_band.column('by')]
            mdf_band = mdf_band.row_subset(is_observer)
        if mdf_band is not None:
            if mdf_band.len() >= 1:
                if plot_in_jd:
                    x_plot = mdf_band.column('JD')  # use Julian Dates just as they are.
                else:
                    x_plot = [util.datetime_utc_from_jd(jd) for jd in mdf_band.column('JD')]  # to datetime.
                y_plot = mdf_band.column('mag')
                ax.scatter(x=x_plot, y=y_plot,
                           color=band_color, marker=band_marker,
                           s=25, alpha=0.9, zorder=+1000)  # zorder->on top.
                legend_labels.append(band)
                # Before we leave this band, store x and y for any points to be highlighted for observer:
                if highlight_observer:
                    if observer_selected is not None:
                        if observer_selected.strip() != '':
                            is_obscode = [u.upper() == observer_selected.upper()
                                          for u in mdf_band.column('by')]
                            if sum(is_obscode) >= 1:
                                x_highlight_this_band = [xx for (xx, keep) in zip(x_plot, is_obscode)
                                                         if keep]
                                y_highlight_this_band = [yy for (yy, keep) in zip(y_plot, is_obscode)
                                                         if keep]
                                x_to_highlight.extend(x_highlight_this_band)
                                y_to_highlight.extend(y_highlight_this_band)

    # Plot legend here, before more scatter plots can mess it up:
    ax.legend(labels=legend_labels,
              scatterpoints=1, bbox_to_anchor=(0, 1.02, 1, .102), loc=3, ncol=2, borderaxespad=0)

    # Highlight observer's points, if requested:
    if len(x_to_highlight) >= 1:
        ax.scatter(x=x_to_highlight, y=y_to_highlight,
                   color=HIGHLIGHT_COLOR, marker='o',
                   s=200, alpha=0.75, zorder=+800)  # under point marker and errorbar.

    # Compute x-axis limits:
    if jd_end is None:
        x_high = util.jd_now()
    else:
        x_high = jd_end
    if jd_start is None:
        x_low = x_high - num_days
    else:
        x_low = jd_start
    if not plot_in_jd:
        x_high = util.datetime_utc_from_jd(x_high)
        x_low = util.datetime_utc_from_jd(x_low)
    x_range = abs(x_high - x_low)
    # print(x_low, x_high, x_range)
    ax.set_xlim(x_low - 0.00 * x_range, x_high + 0.00 * x_range)

    # Format x-axis labels:
    if plot_in_jd:
        ax.get_xaxis().get_major_formatter().set_useOffset(False)  # possibly improve this later.
    else:
        for label in ax.get_xticklabels():
            label.set_ha("right")
            label.set_rotation(30)

    # Arrange the y-axis limits (not trivial as we follow convention of brighter =lesser value magnitudes
    #    to be plotted toward top of plot.
    # We don't use ax.invert_yaxis() as it has side-effect of repeatedly inverting y on successive calls.
    y_low, y_high = ax.set_ylim()
    ax.set_ylim(max(y_low, y_high), min(y_low, y_high))
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

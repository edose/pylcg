import matplotlib
matplotlib.use('TkAgg')  # this must immed follow 'import matplotlib' (even if IDE complains).
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# from matplotlib.figure import Figure
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
    """  Clear and redraw plot area only. Do not touch other areas of main page.
    :param canvas: canvas containing LCG plot [matplotlib FigureCanvasTkAgg object].
    :param df: data to plot [pandas DataFrame].
    :param star_id: star ID to plot [string].
    :param bands_to_plot: AAVSO codes of bands to draw, e.g., ['V', 'Vis.'] [list of strings].
    :param show_errorbars: True to plot errorbars with datapoints, else False [boolean].
    :param show_grid: True to plot grid behind plot, else False [boolean].
    :param jd_start:
    :param jd_end:
    :param num_days:
    :return: True if successful, else False (prob when there are no points to plot) [boolean].
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
    :return: (nothing)
    """
    window_object.quit()
    window_object.destroy()

def message_popup(message):
    """  Draws popup window displaying message to user.
    :param message: the text to display to user [string].
    :return: [None]
    """
    this_window = tk.Tk()
    this_window.wm_title('pylcg MESSAGE TO USER')
    label = ttk.Label(this_window, text=message, font=NORM_FONT)
    label.pack(side='top', fill='x', pady=10)
    button_ok = ttk.Button(this_window, text='OK', command=lambda: quit_and_destroy(this_window))
    button_ok.pack()
    this_window.mainloop()

# def lcg(star_id, max_num_obs=None, jd_start=None, jd_end=None, num_days=500):
#     """  Make and display a plot resembling AAVSO's hallowed Light Curve Generator V1.
#          Gets data from AAVSO VSX, extracts the data needed, and plots.
#     :param star_id: ID of the target star to plot [string].
#     :param max_num_obs: maximum number of points to plot [int] -- NOT YET IMPLEMENTED.
#     :param jd_start: earliest Julian date to plot [float].
#     :param jd_end: latest Julian date to plot, or None for now [float/None].
#     :param num_days: set earliest Julian date to jd_end - num_days [int/float].
#     :return: no return value; this function makes and displays a plot similar to LCG V1.
#     """
#     df_obs_data = web.get_vsx_obs(star_id, max_num_obs, jd_start, jd_end, num_days)
#     if len(df_obs_data) <= 0:
#         print('>>>>> No observations found for ' + star_id + ' in this date range.')
#         return
#
#     # Build plot data:
#     x = df_obs_data['JD']
#     y = df_obs_data['mag']
#     uncert = pd.Series([max(0.0, float(u)) for u in df_obs_data['uncert']])
#     colors = [COLOR_BY_BAND[band] for band in df_obs_data['band']]
#
#     # Construct plot:
#     fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(FIGURE_WIDTH_INCHES, FIGURE_HEIGHT_INCHES))
#     ax.grid(True, color='lightgray', zorder=-1000)
#     ax.set_title('plot for ' + star_id.upper() + '  (py app_entry_manual)',
#                  color='darkblue', fontsize=20, weight='bold')
#     ax.set_xlabel('JD')
#     ax.set_ylabel('Magnitude')
#     ax.errorbar(x=x, y=y, xerr=0.0, yerr=uncert, fmt='none', ecolor='gray',
#                 capsize=2, alpha=1, zorder=+900)
#     for band in COLOR_BY_BAND.keys():
#         band_color = COLOR_BY_BAND[band]
#         band_marker = MARKER_BY_BAND[band]
#         is_color = [color == band_color for color in colors]
#         ax.scatter(x=x[is_color], y=y[is_color], color=band_color, marker=band_marker,
#                    s=25, alpha=0.9, zorder=+1000)
#         # ax.scatter(x=x, y=y, color=colors, marker=markers, alpha=0.8, zorder=+1000)
#     plt.gca().invert_yaxis()  # per custom of plotting magnitudes brighter=upward
#     fig.canvas.set_window_title(star_id)
#     plt.draw()
#
#
# def go(filename=r'./data/AAVSOreport-20180813.txt',
#        max_num_obs=None, jd_start=None, jd_end=None, num_days=500):
#     """  Sequentially make LCG plots for each target star reported
#              in an app_entry_upload file.
#          Typical use: in-context lightcurve review of each target star
#              in recently uploaded submission file.
#     :param filename: full path of uploaded submission file.
#     :param max_num_obs: maximum number of points to plot [int] -- NOT YET IMPLEMENTED.
#     :param jd_start: earliest Julian date to plot [float].
#     :param jd_end: latest Julian date to plot, or None for now [float/None].
#     :param num_days: set earliest Julian date to jd_end - num_days [int/float].
#     :return: no return value; this function makes and displays multiple plots similar to LCG V1.
#     """
#     # Heavily adapted from https://matplotlib.org/examples/user_interfaces/embedding_in_tk.html .
#
#     global exit_cause
#     exit_cause = None
#     star_ids = util.get_star_ids_from_upload_file(filename)
#
#     root = tk.Tk()
#     fig = Figure(figsize=(FIGURE_WIDTH_INCHES, FIGURE_HEIGHT_INCHES))
#     # Construct a tk.DrawingArea:
#     canvas = FigureCanvasTkAgg(fig, master=root)
#     canvas.show()
#     canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
#
#     toolbar = NavigationToolbar2TkAgg(canvas, root)
#     toolbar.update()
#     canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
#
#     for i, star_id in enumerate(star_ids):
#         root.wm_title(star_id.upper() + ":     app_entry_manual plot # " +
#             str(i + 1) + ' of ' + str(len(star_ids)))
#
#         df_obs_data = web.get_vsx_obs(star_id, max_num_obs, jd_start, jd_end, num_days)
#         if len(df_obs_data) <= 0:
#             print('>>>>> No observations found for ' + star_id + ' in this date range.')
#             return
#
#         # Build plot data:
#         x = df_obs_data['JD']
#         y = df_obs_data['mag']
#         uncert = pd.Series([max(0.0, u) for u in df_obs_data['uncert']])
#         colors = [COLOR_BY_BAND.get(band, None) for band in df_obs_data['band']]
#
#         # Construct axes and other structure of the plot:
#         ax = fig.add_subplot(111)
#         ax.clear()
#         ax.grid(True, color='lightgray', zorder=-1000)
#         ax.set_title('plot for ' + star_id.upper() + '  (py app_entry_manual)',
#                      color='darkblue', fontsize=20, weight='bold')
#         ax.set_xlabel('JD')
#         ax.set_ylabel('Magnitude')
#         ax.errorbar(x=x, y=y, xerr=0.0, yerr=uncert, fmt='none', capsize=2, alpha=1, zorder=+900)
#
#         # Draw points, one observation band (point color) at a time:
#         # [We must loop this way because matplotlib allows only one marker shape per call to .scatter().]
#         for band in COLOR_BY_BAND.keys():
#             band_color = COLOR_BY_BAND[band]
#             band_marker = MARKER_BY_BAND[band]
#             is_color = [color == band_color for color in colors]
#             ax.scatter(x=x[is_color], y=y[is_color], color=band_color, marker=band_marker,
#                        s=25, alpha=0.9, zorder=+1000)
#         ax.invert_yaxis()  # to follow convention of brighter (=lesser) magnitudes -> upward.
#         plt.show()
#
#         # # Construct a tk.DrawingArea:
#         # canvas = FigureCanvasTkAgg(fig, master=root)
#         # canvas.show()
#         # canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
#         #
#         # toolbar = NavigationToolbar2TkAgg(canvas, root)
#         # toolbar.update()
#         # canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
#
#         root.focus_set()
#         root.focus_set()  # twice seems to set focus more reliably.
#
#         def _quit():
#             root.quit()  # stops mainloop
#             root.destroy()  # prevents Fatal Python Error: PyEval_RestoreThread: NULL tstate
#             print('Quit was pressed...stopping now.')
#             global exit_cause
#             exit_cause = 'quit'
#
#         def _next():
#             # root.quit()  # stops mainloop
#             # root.destroy()  # prevents Fatal Python Error: PyEval_RestoreThread: NULL tstate
#             global exit_cause
#             exit_cause = 'next'
#             ax.clear()
#
#         def on_key_event(event):
#             # print('you pressed %s' % event.key)
#             _next()
#             # key_press_handler(event, canvas, toolbar)
#
#         cid = canvas.mpl_connect('key_release_event', on_key_event)
#
#         button_quit = tk.Button(master=root, text='Quit all plots', command=_quit)
#         button_quit.pack(side=tk.RIGHT)
#         button_next = tk.Button(master=root, text='Go to next plot', command=_next)
#         button_next.pack(side=tk.BOTTOM)
#
#         root.focus_force()  # give this window focus so that keystrokes work.
#         root.mainloop()  # wait until user does something, then close window.
#
#         # Window has closed; now move on to next plot or get out.
#         # canvas.mpl_disconnect(cid)  # cleanup precaution
#         if exit_cause == 'quit':
#             break  # just get out
#         elif exit_cause == 'next':
#             continue  # next star if any.
#         else:
#             print('we have a problem.')
#             break


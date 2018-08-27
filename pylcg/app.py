from collections import OrderedDict

import matplotlib
matplotlib.use('TkAgg')  # graphics backend
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import style
from matplotlib import pyplot as plt

import tkinter as tk
from tkinter import ttk

import pandas as pd

import pylcg.preferences as prefs
import pylcg.plot as plotter
import pylcg.web as web
from pylcg.util import jd_now

__author__ = "Eric Dose :: New Mexico Mira Project, Albuquerque"

ALL_BANDS = ['U', 'B', 'V', 'R', 'I', 'Vis.', 'TG', 'J', 'H', 'K', 'TB', 'TR', 'CV', 'CR', 'CBB',
             'SZ', 'SU', 'SG', 'SR', 'SI', 'STU', 'STV', 'STB', 'STY', 'STHBW', 'STHBN',
             'MA', 'MB', 'MI', 'ZS', 'Y', 'HA', 'HAC']
PYLCG_LOGO = 'pylcg v0.1'
PYLCG_LOGO_FONT = ('consolas', 20)
PYLCG_SUB_LOGO = 'for local testing only'
PYLCG_SUB_LOGO_FONT = ('consolas', 9)


class ApplicationPylcg(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.iconbitmap(self, default='pylcg-icon16.ico')  # must be an icon file
        tk.Tk.wm_title(self, 'pylcg  -- Light Curve Generator in python 3')
        self.resizable(True, True)

        # main_frame (fills entire application window):
        self.main_frame = tk.Frame(self)
        self.main_frame.grid()
        self.main_frame.pack(side="top", fill="both", expand=True)

        self.make_menu()

        self.preferences = prefs.Preferences()  # load preferences from file .\data\preferences.ini.

        display_frame = self.subdivide_main_frame()

        plot_frame, toolbar_frame = self.subdivide_display_frame(display_frame)

        # Assign matplotlib scatter plot to plot frame:
        fig = Figure(figsize=(10.24, 7.20), dpi=100)
        ax = fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(fig, plot_frame)
        self.canvas.show()
        # To change size, consider:
        #    fig.set_size_inches(new_width, new_height, forward=True)
        #    fig.set_dpi(100)

        # Assign navigation buttons to toolbar frame:
        # note: NavigationToolbar2TkAgg must be isolated in its own frame.
        toolbar = NavigationToolbar2TkAgg(self.canvas, toolbar_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.update()

        self.build_control_frame()

        # # Plot the first star (without waiting for button press):
        # self._plot_star(self.star_ids[0], get_obs_data=True)
        # if self.i_star >= len(self.star_ids) - 1:
        #     self.button_next.config(state='disabled')

    def make_menu(self):
        # Build menu bar:
        menubar = tk.Menu(self.main_frame)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label='Exit', command=quit)
        menubar.add_cascade(label='File', menu=file_menu)
        preferences_menu = tk.Menu(menubar, tearoff=0)
        preferences_menu.add_command(label='Reload User Preferences',
                                     command=prefs.Preferences.load_ini_file)
        preferences_menu.add_command(label='Set all Preferences to Defaults',
                                     command=prefs.Preferences.reset_current_to_default)
        menubar.add_cascade(label='Preferences', menu=preferences_menu)
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label='Browse pylcg repo', command=web.browse_repo)
        help_menu.add_command(label='About', command=self._about_window)
        menubar.add_cascade(label='Help', menu=help_menu)
        tk.Tk.config(self, menu=menubar)

    def subdivide_main_frame(self):
        self.main_frame.grid_rowconfigure(0, weight=1)  # display_frame expandable.
        self.main_frame.grid_columnconfigure(0, weight=1)  # "
        display_frame = tk.Frame(self.main_frame)
        self.control_frame = tk.Frame(self.main_frame, width=300)
        display_frame.grid(row=0, column=0, sticky='nsew')
        self.control_frame.grid(row=0, column=1, sticky='ns')
        return display_frame

    def subdivide_display_frame(self, display_frame):
        display_frame.grid_rowconfigure(0, weight=1)  # plot_frame expandable.
        display_frame.grid_columnconfigure(0, weight=1)  # "
        plot_frame = tk.Frame(display_frame)
        toolbar_frame = tk.Frame(display_frame)
        plot_frame.grid(row=0, column=0, sticky='nsew')
        toolbar_frame.grid(row=1, column=0, padx=125, sticky='w')
        plot_frame.grid_rowconfigure(0, weight=1)
        plot_frame.grid_columnconfigure(0, weight=1)
        return plot_frame, toolbar_frame

    def build_control_frame(self):
        # Control Frame:
        self.control_frame.grid_rowconfigure(1, weight=1)
        self.control_frame.grid_columnconfigure(0, weight=1)

        # Subframe 'logo_frame':
        logo_frame = ttk.Frame(self.control_frame)
        logo_frame.grid(row=0, column=0, padx=20, pady=15)
        label_logo = tk.Label(logo_frame, text='\n' + PYLCG_LOGO, font=PYLCG_LOGO_FONT, fg='gray')
        label_logo.grid(sticky='sew')
        label_logo = tk.Label(logo_frame, text=PYLCG_SUB_LOGO, font=PYLCG_SUB_LOGO_FONT, fg='black')
        label_logo.grid(sticky='sew')
        # Subframe 'control_subframe1':

        control_subframe1 = ttk.Frame(self.control_frame, padding=5)
        control_subframe1.grid(row=1, column=0, sticky=tk.N)
        control_subframe1.grid_columnconfigure(0, weight=1)
        control_subframe1.grid_columnconfigure(1, weight=1)
        # Star labelframe:
        star_labelframe = tk.LabelFrame(control_subframe1, text=' Star ', padx=10, pady=10)
        star_labelframe.grid(pady=15, sticky='ew')
        self.star_entered = tk.StringVar()
        self.star_entered.set('UZ Cam')  # dummy star just to get started.
        # self.this_star.trace("w", lambda name, index, mode: print(self.star_entered.get()))
        self.star_entry = ttk.Entry(star_labelframe, textvariable=self.star_entered)
        self.star_entry.grid(row=0, columnspan=2, sticky='ew')
        self.button_plot_this_star = ttk.Button(star_labelframe, text='Plot this star',
                                                command=lambda: self._plot_star(self.star_entered.get(),
                                                                                True))
        self.button_plot_this_star.grid(row=1, column=0, columnspan=2, sticky='ew')
        self.star_entry.bind('<Return>', lambda d: self.button_plot_this_star.invoke())
        self.prev_star = tk.StringVar()  # reserve name for label, later.
        self.button_prev = ttk.Button(star_labelframe, text='Prev', command=self._prev_star)
        self.button_prev.grid(row=2, column=0, sticky='e')
        self.next_star = tk.StringVar()  # reserve name for label, later.
        self.button_next = ttk.Button(star_labelframe, text='Next', command=self._next_star)
        self.button_next.grid(row=2, column=1, sticky='w')
        self.button_prev.config(state='disabled')  # For now
        self.button_next.config(state='disabled')  # For now
        # Time span labelframe:
        timespan_labelframe = tk.LabelFrame(control_subframe1, text=' Time span ', padx=10, pady=10)
        timespan_labelframe.grid(pady=15, sticky='ew')
        timespan_labelframe.grid_columnconfigure(1, weight=1)
        self.days_to_plot = tk.StringVar()
        self.days_to_plot.set(self.preferences.get('Data preferences', 'Days'))
        self.days_entry = ttk.Entry(timespan_labelframe, width=6, justify=tk.RIGHT,
                                    textvariable=self.days_to_plot)
        self.days_entry.grid(row=0, column=1, sticky='e')
        self.days_entry.bind('<Return>', lambda d: self.button_plot_this_star.invoke())
        days_label = tk.Label(timespan_labelframe, text=' days')
        days_label.grid(row=0, column=2)

        jdstart_label = ttk.Label(timespan_labelframe, text='JD Start: ')
        jdstart_label.grid(row=1, column=0)
        self.jdstart = tk.StringVar()
        self.jdstart.set('')
        self.jdstart_entry = ttk.Entry(timespan_labelframe, width=12, justify=tk.RIGHT,
                                       textvariable=self.jdstart)
        self.jdstart_entry.grid(row=1, column=1, columnspan=2, sticky='ew')
        jdend_label = ttk.Label(timespan_labelframe, text='JD End: ')
        jdend_label.grid(row=2, column=0)
        self.jdend = tk.StringVar()
        self.jdend.set('{:20.6f}'.format(jd_now()).strip())
        self.jdend_entry = ttk.Entry(timespan_labelframe, width=12, justify=tk.RIGHT,
                                     textvariable=self.jdend)
        self.jdend_entry.grid(row=2, column=1, columnspan=2, sticky='ew')
        use_now_button = ttk.Button(timespan_labelframe, text='JD End = Now', command=self._use_now)
        use_now_button.grid(row=3, column=1, columnspan=2, sticky='ew')

        # Bands labelframe:
        self.bands_labelframe = tk.LabelFrame(control_subframe1, text=' Bands ', padx=15, pady=10)
        self.bands_labelframe.grid(pady=15, sticky='ew')
        self.bands_labelframe.grid_columnconfigure(0, weight=1)
        self.bands_labelframe.grid_columnconfigure(1, weight=1)

        self.band_flags = OrderedDict()
        self.band_flags['U'] = tk.BooleanVar()
        self.band_flags['V'] = tk.BooleanVar()
        self.band_flags['B'] = tk.BooleanVar()
        self.band_flags['R'] = tk.BooleanVar()
        self.band_flags['I'] = tk.BooleanVar()
        self.band_flags['Vis.'] = tk.BooleanVar()
        self.band_flags['TG'] = tk.BooleanVar()
        self.band_flags['others'] = tk.BooleanVar()
        self.band_flags['ALL'] = tk.BooleanVar()
        # Make dict of key=band, value=True iff band has its own checkbutton.
        band_individually_selectable = [(band, (band in self.band_flags.keys())) for band in ALL_BANDS]
        self.band_individually_selectable = OrderedDict((key, value)
                                                        for (key, value) in band_individually_selectable)
        self.bands_to_plot = self.preferences.get('Data preferences', 'bands')

        self._set_band_flags_from_preferences()
        self.band_u_checkbutton = ttk.Checkbutton(self.bands_labelframe, text='U      ',
                                                  variable=self.band_flags['U'],
                                                  command=self._update_bands_to_plot)
        self.band_b_checkbutton = ttk.Checkbutton(self.bands_labelframe, text='B',
                                                  variable=self.band_flags['B'],
                                                  command=self._update_bands_to_plot)
        self.band_v_checkbutton = ttk.Checkbutton(self.bands_labelframe, text='V',
                                                  variable=self.band_flags['V'],
                                                  command=self._update_bands_to_plot)
        self.band_r_checkbutton = ttk.Checkbutton(self.bands_labelframe, text='R',
                                                  variable=self.band_flags['R'],
                                                  command=self._update_bands_to_plot)
        self.band_i_checkbutton = ttk.Checkbutton(self.bands_labelframe, text='I',
                                                  variable=self.band_flags['I'],
                                                  command=self._update_bands_to_plot)
        self.band_vis_checkbutton = ttk.Checkbutton(self.bands_labelframe, text='Vis.',
                                                    variable=self.band_flags['Vis.'],
                                                    command=self._update_bands_to_plot)
        self.band_tg_checkbutton = ttk.Checkbutton(self.bands_labelframe, text='TG',
                                                   variable=self.band_flags['TG'],
                                                   command=self._update_bands_to_plot)
        self.band_others_checkbutton = ttk.Checkbutton(self.bands_labelframe, text='others',
                                                       variable=self.band_flags['others'],
                                                       command=self._update_bands_to_plot)
        self.band_all_checkbutton = ttk.Checkbutton(self.bands_labelframe, text='ALL',
                                                    variable=self.band_flags['ALL'],
                                                    command=self._update_bands_to_plot)
        self.band_u_checkbutton.grid(row=0, column=0, sticky='w')
        self.band_b_checkbutton.grid(row=1, column=0, sticky='w')
        self.band_v_checkbutton.grid(row=2, column=0, sticky='w')
        self.band_r_checkbutton.grid(row=3, column=0, sticky='w')
        self.band_i_checkbutton.grid(row=4, column=0, sticky='w')
        self.band_vis_checkbutton.grid(row=0, column=1, sticky='w')
        self.band_tg_checkbutton.grid(row=1, column=1, sticky='w')
        self.band_others_checkbutton.grid(row=2, column=1, sticky='w')
        self.band_all_checkbutton.grid(row=4, column=1, sticky='w')

        button_preferences = ttk.Button(control_subframe1, text='Preferences...',
                                        command=self._preferences_window)
        button_preferences.grid(pady=5, sticky='ew')
        button_listobservers = ttk.Button(control_subframe1, text='List Observers',
                                          command=self._listobservers_window)
        button_listobservers.grid(pady=5, sticky='ew')

        # Subframe quit_frame:
        quit_frame = tk.Frame(self.control_frame, height=60)
        quit_frame.grid(row=2, column=0, pady=10)
        self.quit_button = ttk.Button(quit_frame, text='QUIT pylcg', width=16, cursor='pirate',
                                      command=self._quit_window)
        self.quit_button.grid(row=0, column=0)

    def _preferences_window(self):
        # 'transient' window style (not modal).
        # Lay out window elements:
        preferences_window = tk.Toplevel(self)
        tk.Label(preferences_window, text='pylcg Preferences').pack(sticky='new')
        preferences_window.transient(self)
        frame1 = ttk.Frame(preferences_window)
        frame1.pack(sticky='ew')
        show_errorbars = ttk.Checkbutton(frame1, text='show errorbars')
        show_errorbars.grid(row=0, column=0)
        show_grid = ttk.Checkbutton(frame1, text='show grid')
        show_grid.grid(row=1, column=0)
        # plot_style = tk.Listbox(frame1, )
        # Put data in window elements:


        # On window close, (1) write preferences, (2) close gracefully.

    def _about_window(self):
        pass

    def _listobservers_window(self):
        pass

    def _quit_window(self):
        print('Quit was pressed...stopping now.')
        self.quit_button.config(state='disabled')
        # plotter.message_popup("You're leaving me???")
        self.preferences.write_current_config_to_ini_file()
        self.quit()     # stop mainloop
        self.destroy()  # prevent Fatal Python Error: PyEval_RestoreThread: NULL tstate

    def _prev_star(self):
        print('Prev was pressed.')
        self.i_star = max(0, self.i_star - 1)
        self.button_prev.config(state=(tk.DISABLED if self.i_star == 0 else tk.NORMAL))
        self.button_next.config(state=(tk.DISABLED if self.i_star >= len(self.star_ids) - 1 else tk.NORMAL))
        self._plot_star(self.star_ids[self.i_star])

    def _next_star(self):
        print('Next was pressed.')
        self.i_star = min(len(self.star_ids) - 1, self.i_star + 1)
        self.button_prev.config(state=(tk.DISABLED if self.i_star == 0 else tk.NORMAL))
        self.button_next.config(state=(tk.DISABLED if self.i_star >= len(self.star_ids) - 1 else tk.NORMAL))
        self._plot_star(self.star_ids[self.i_star])

    def _use_now(self):
        self.jdend.set('{:20.6f}'.format(jd_now()).strip())

    def _update_bands_to_plot(self):
        if self.band_flags['ALL'].get() is True:
            self.bands_to_plot = ALL_BANDS
        else:
            self.bands_to_plot = [band for band in ALL_BANDS
                                  if (self.band_individually_selectable[band] is True)
                                  and (self.band_flags[band].get() is True)]
            if self.band_flags['others'].get() is True:
                self.bands_to_plot.extend([band for band in ALL_BANDS
                                           if self.band_individually_selectable[band] is False])
        # print(len(self.bands_to_plot), self.bands_to_plot)

    def _set_band_flags_from_preferences(self):
        for band in self.band_flags.keys():
            self.band_flags[band].set(band in self.bands_to_plot)

    def _plot_star(self, star_id, must_get_obs_data=True):
        self._update_bands_to_plot()  # ensure sync with checkbuttons.
        self.preferences.set('Data preferences', 'bands', self.bands_to_plot)  # ensure bands are stored.
        jd_start = None if self.jdstart.get().strip() == '' else float(self.jdstart.get())
        jd_end = None if self.jdend.get().strip() == '' else float(self.jdend.get())
        if self.days_to_plot.get().strip() != '':
            num_days = float(self.days_to_plot.get().strip())
        else:
            if jd_end is None:
                self.days_to_plot.set(self.preferences.default_config('Data preferences', 'days'))
                num_days = float(self.days_to_plot.get())
            else:
                num_days = None
        if must_get_obs_data:
            self.df_obs_data = web.get_vsx_obs(star_id=star_id,
                                               jd_start=jd_start, jd_end=jd_end, num_days=num_days)
        plotter.redraw_plot(self.canvas, self.df_obs_data, star_id, bands_to_plot=self.bands_to_plot,
                            show_errorbars=self.preferences.get('Format preferences', 'show errorbars'),
                            show_grid=self.preferences.get('Format preferences', 'show grid'),
                            jd_start=jd_start, jd_end=jd_end, num_days=num_days)


# ***** Python file entry here. *****
# We must do without entry via functions, because tkinter just can't do that right.
# Thus, enter via this python file. We'll add arguments later, if necessary.
# Sigh.
# Well, at least this might later facilitate the making of executables for distribution.
if __name__ == "__main__":
    app = ApplicationPylcg()
    app.mainloop()

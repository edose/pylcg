from collections import OrderedDict

import matplotlib
# next line (.use()) *must* come before other matplotlib/tkinter imports, even if IDE complains.
matplotlib.use('TkAgg')  # graphics backend
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import style
from matplotlib import pyplot as plt

import sys
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkm
from tkinter import filedialog

import pylcg.preferences as prefs
import pylcg.plot as plotter
import pylcg.web as web
from pylcg.util import jd_now, MiniDataFrame, TargetList, get_star_ids_from_upload_file, \
    jd_from_any_date_string, jd_from_datetime_utc

__author__ = "Eric Dose :: New Mexico Mira Project, Albuquerque"

"""  pylcg, a proposed replacement for AAVSO's venerable but doomed Light Curve Generator LCG V1.
     Plots light curve for a star having data in AAVSO's AID database.
         This program retrieves data from AAVSO and plots the light curve in the customary
         fashion, and very similarly to AAVSO's LCG V1(x=date, y=magnitude inverted).
     This program provided as an executable file suitable for Windows 7/8/10.
     Software built in python 3.6, executable includes the same.
         GUI built with python's built-in package tkinter.
         Web access built with python's built-in packages urllib and webbrowser.
         Data cacheing built with python's built-in package functools.     
         Plotting built with package matplotlib v 2.0.2.
         [pandas dependence removed Sept 7 2018 in favor of local 'MiniDataFrame' class.]
     This pylcg version: 0.1 BETA, September 6, 2018.
     Eric Dose, Albuquerque, New Mexico, USA
"""

ALL_BANDS = ['U', 'B', 'V', 'R', 'I', 'Vis.', 'TG', 'J', 'H', 'K', 'TB', 'TR', 'CV', 'CR', 'CBB',
             'SZ', 'SU', 'SG', 'SR', 'SI', 'STU', 'STV', 'STB', 'STY', 'STHBW', 'STHBN',
             'MA', 'MB', 'MI', 'ZS', 'Y', 'HA', 'HAC']
BETA_CHARACTER = '\u03B2'  # unicode 'small beta'

PYLCG_LOGO = 'pylcg v0.2' + BETA_CHARACTER
PYLCG_LOGO_FONT = ('consolas', 20)
PYLCG_SUB_LOGO = 'October 11 2018'
PYLCG_SUB_LOGO_FONT = ('consolas', 9)

PYLCG_VERSION = '0.2 BETA'
PYLCG_VERSION_DATE = 'October 11, 2018'

PYLCG_REPO_URL = r'https://github.com/edose/pylcg'
PYLCG_REPO_FONT = ('consolas', 8, 'underline')
ABOUT_AUTHOR = 'Made in Albuquerque, New Mexico, USA\n'\
               'by Eric Dose, for the AAVSO.\n'
ABOUT_AUTHOR_FONT = ('verdana', 7, 'italic')

EMPTY_MARK = '-'
VALID_MARK = '\u2714'  # unicode 'heavy check mark'
INVALID_MARK = '\u2718'  # unicode 'heavy ballot X'
VALIDITY_TO_MARK = {None: EMPTY_MARK, True: VALID_MARK, False: INVALID_MARK}
VALIDITY_MARK_FONT = ('consolas', 10, 'bold')

MIN_JD_ALLOWABLE = jd_from_any_date_string('1/1/1800')  # earliest imaginable plot-start date.
MAX_JD_ALLOWABLE = jd_now() + 1 * 365.25  # latest plot-start date: one year from now.


class ApplicationPylcg(tk.Tk):
    """  Main pylcg program."""
    def __init__(self):
        tk.Tk.__init__(self)

        self.iconbitmap(self, default='pylcg-icon.ico')  # must be an icon file
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

        self.target_list = TargetList()

        # Assign matplotlib scatter plot to plot frame:
        fig = Figure(figsize=(10.24, 7.20), dpi=100)
        ax = fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(fig, plot_frame)
        self.canvas.show()
        # To change size, alternatively:
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

    def make_menu(self):
        """  Build the GUI's menu. No return value."""
        # Build menu bar:
        menubar = tk.Menu(self.main_frame)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label='Exit', command=self._quit_window)
        menubar.add_cascade(label='File', menu=file_menu)
        preferences_menu = tk.Menu(menubar, tearoff=0)
        preferences_menu.add_command(label='Reload User Preferences',
                                     command=prefs.Preferences.load_ini_file)
        preferences_menu.add_command(label='Set all Preferences to Defaults',
                                     command=prefs.Preferences.reset_current_to_default)
        menubar.add_cascade(label='Preferences', menu=preferences_menu)
        preferences_menu.entryconfig('Reload User Preferences', state='disabled')
        preferences_menu.entryconfig('Set all Preferences to Defaults', state='disabled')
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label='Browse pylcg repo and README', command=web.webbrowse_repo)
        help_menu.add_command(label='About', command=self._about_window)
        menubar.add_cascade(label='Help', menu=help_menu)
        tk.Tk.config(self, menu=menubar)

    def subdivide_main_frame(self):
        """  Divides the program's entire GUI frame (main_frame) into a left-side display frame
        and a right-side control frame.
        :return: display_frame [tkinter Frame object].
        """
        self.main_frame.grid_rowconfigure(0, weight=1)  # display_frame expandable.
        self.main_frame.grid_columnconfigure(0, weight=1)  # "
        display_frame = tk.Frame(self.main_frame)
        self.control_frame = tk.Frame(self.main_frame, width=300)
        display_frame.grid(row=0, column=0, sticky='nsew')
        self.control_frame.grid(row=0, column=1, sticky='ns')
        return display_frame

    def subdivide_display_frame(self, display_frame):
        """  Divides the large frame (display_frame) on left side of program's window into a large
        plot frame (plot_frame) and a much smaller (toolbar_frame).
        Greatly stabilizes operation of both windows.
        :param display_frame: the Frame containing left side of program window [tkinter Frame object].
        :return: plot_frame, toolbar_frame [a 2-tuple of tkinter Frame objects].
        """
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
        """  Build the entire tall frame along right side of program's main window.
        :return: [None]
        """
        # Control Frame:
        self.control_frame.grid_rowconfigure(1, weight=1)
        self.control_frame.grid_columnconfigure(0, weight=1)

        # Subframe 'logo_frame':
        logo_frame = ttk.Frame(self.control_frame)
        logo_frame.grid(row=0, column=0, padx=10, pady=3)
        label_logo = tk.Label(logo_frame, text='\n' + PYLCG_LOGO, font=PYLCG_LOGO_FONT, fg='gray')
        label_logo.grid(sticky='sew')
        label_logo = tk.Label(logo_frame, text=PYLCG_SUB_LOGO, font=PYLCG_SUB_LOGO_FONT, fg='black')
        label_logo.grid(sticky='sew')

        # Subframe 'control_subframe1':
        control_subframe1 = ttk.Frame(self.control_frame, padding=5)
        control_subframe1.grid(row=1, column=0, sticky=tk.N)
        control_subframe1.grid_columnconfigure(0, weight=1)
        control_subframe1.grid_columnconfigure(1, weight=1)

        # ----- Star labelframe:
        star_labelframe = tk.LabelFrame(control_subframe1, text=' Star ', padx=10, pady=6)
        star_labelframe.grid(pady=15, sticky='ew')
        self.button_stars_from_upload = ttk.Button(star_labelframe, text='From upload file...',
                                                   command=self._add_upload_star_ids)
        self.button_stars_from_upload.grid(row=0, column=0, columnspan=2, sticky='e')
        self.star_entered = tk.StringVar()
        self.star_entered.set('')
        # self.this_star.trace("w", lambda name, index, mode: print(self.star_entered.get()))
        self.star_entry = ttk.Entry(star_labelframe, textvariable=self.star_entered)
        self.star_entry.grid(row=1, columnspan=2, sticky='ew')
        self.button_plot_this_star = ttk.Button(star_labelframe, text='Plot this star',
                                                command=lambda: self._entered_star(self.star_entered.get()))
        self.button_plot_this_star.grid(row=2, column=0, columnspan=2, sticky='ew')
        self.star_entry.bind('<Return>', lambda d: self.button_plot_this_star.invoke())
        self.prev_star = tk.StringVar()  # reserve name for label, later.
        self.button_prev = ttk.Button(star_labelframe, text='Prev', command=self._prev_star)
        self.button_prev.grid(row=3, column=0, sticky='e')
        self.next_star = tk.StringVar()  # reserve name for label, later.
        self.button_next = ttk.Button(star_labelframe, text='Next', command=self._next_star)
        self.button_next.grid(row=3, column=1, sticky='w')
        self.button_prev.config(state='disabled')  # For now
        self.button_next.config(state='disabled')  # For now

        # ----- Time span labelframe:
        timespan_labelframe = tk.LabelFrame(control_subframe1, text=' Time span (any 2)', padx=10, pady=8)
        timespan_labelframe.grid(pady=15, sticky='ew')
        timespan_labelframe.grid_columnconfigure(1, weight=1)
        self.days_to_plot = tk.StringVar()
        self.timestart = tk.StringVar()
        self.timeend = tk.StringVar()
        self.days_valid = False
        self.timestart_valid = False
        self.timeend_valid = False
        self.days_flag_label = tk.Label(timespan_labelframe, text=' ', font=VALIDITY_MARK_FONT)
        self.timestart_flag_label = tk.Label(timespan_labelframe, text=' ', font=VALIDITY_MARK_FONT)
        self.timeend_flag_label = tk.Label(timespan_labelframe, text=' ', font=VALIDITY_MARK_FONT)
        self.label_background_color = self.timeend_flag_label['bg']  # save this for later use.
        self.days_to_plot.trace('w', lambda name, index, mode: self._set_time_flags(to_gray=True))
        self.timestart.trace('w', lambda name, index, mode: self._set_time_flags(to_gray=True))
        self.timeend.trace('w', lambda name, index, mode: self._set_time_flags(to_gray=True))
        self.days_to_plot.set(self.preferences.get('Data preferences', 'Days'))
        self.timestart.set('')
        self.timeend.set('{:20.6f}'.format(jd_now()).strip())
        self.days_entry = ttk.Entry(timespan_labelframe, width=6, justify=tk.RIGHT,
                                    textvariable=self.days_to_plot)
        self.timestart_entry = ttk.Entry(timespan_labelframe, width=12, justify=tk.RIGHT,
                                         textvariable=self.timestart)
        self.timeend_entry = ttk.Entry(timespan_labelframe, width=12, justify=tk.RIGHT,
                                       textvariable=self.timeend)
        self.days_entry.bind('<Return>', lambda d: self.button_plot_this_star.invoke())
        self.days_entry.grid(row=0, column=1, sticky='e')
        days_label = tk.Label(timespan_labelframe, text=' days')
        days_label.grid(row=0, column=2)
        self.days_flag_label.grid(row=0, column=3)
        timestart_label = tk.Label(timespan_labelframe, text='Start: ')
        timestart_label.grid(row=1, column=0)
        self.timestart_entry.grid(row=1, column=1, columnspan=2, sticky='ew')
        self.timestart_flag_label.grid(row=1, column=3)
        timeend_label = tk.Label(timespan_labelframe, text='End: ')
        timeend_label.grid(row=2, column=0)
        self.timeend_entry.grid(row=2, column=1, columnspan=2, sticky='ew')
        self.timeend_flag_label.grid(row=2, column=3)
        self._set_time_flags(to_gray=True)  # ensure flags are set before leaving setup.
        use_now_button = ttk.Button(timespan_labelframe, text='End = now', command=self._use_now)
        use_now_button.grid(row=3, column=1, columnspan=2, sticky='ew')

        # ----- Bands labelframe:
        self.bands_labelframe = tk.LabelFrame(control_subframe1, text=' Bands ', padx=15, pady=10)
        self.bands_labelframe.grid(pady=10, sticky='ew')
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
                                                  command=self._update_bands_to_plot_then_plot)
        self.band_b_checkbutton = ttk.Checkbutton(self.bands_labelframe, text='B',
                                                  variable=self.band_flags['B'],
                                                  command=self._update_bands_to_plot_then_plot)
        self.band_v_checkbutton = ttk.Checkbutton(self.bands_labelframe, text='V',
                                                  variable=self.band_flags['V'],
                                                  command=self._update_bands_to_plot_then_plot)
        self.band_r_checkbutton = ttk.Checkbutton(self.bands_labelframe, text='R',
                                                  variable=self.band_flags['R'],
                                                  command=self._update_bands_to_plot_then_plot)
        self.band_i_checkbutton = ttk.Checkbutton(self.bands_labelframe, text='I',
                                                  variable=self.band_flags['I'],
                                                  command=self._update_bands_to_plot_then_plot)
        self.band_vis_checkbutton = ttk.Checkbutton(self.bands_labelframe, text='Vis.',
                                                    variable=self.band_flags['Vis.'],
                                                    command=self._update_bands_to_plot_then_plot)
        self.band_tg_checkbutton = ttk.Checkbutton(self.bands_labelframe, text='TG',
                                                   variable=self.band_flags['TG'],
                                                   command=self._update_bands_to_plot_then_plot)
        self.band_others_checkbutton = ttk.Checkbutton(self.bands_labelframe, text='others',
                                                       variable=self.band_flags['others'],
                                                       command=self._update_bands_to_plot_then_plot)
        self.band_all_checkbutton = ttk.Checkbutton(self.bands_labelframe, text='ALL',
                                                    variable=self.band_flags['ALL'],
                                                    command=self._update_bands_to_plot_then_plot)
        self.band_u_checkbutton.grid(row=0, column=0, sticky='w')
        self.band_b_checkbutton.grid(row=1, column=0, sticky='w')
        self.band_v_checkbutton.grid(row=2, column=0, sticky='w')
        self.band_r_checkbutton.grid(row=3, column=0, sticky='w')
        self.band_i_checkbutton.grid(row=4, column=0, sticky='w')
        self.band_vis_checkbutton.grid(row=0, column=1, sticky='w')
        self.band_tg_checkbutton.grid(row=1, column=1, sticky='w')
        self.band_others_checkbutton.grid(row=2, column=1, sticky='w')
        self.band_all_checkbutton.grid(row=4, column=1, sticky='w')

        # ----- Checkbutton frame:
        checkbutton_frame = tk.Frame(control_subframe1)
        checkbutton_frame.grid(sticky='ew')
        self.grid_flag = tk.BooleanVar()
        self.errorbar_flag = tk.BooleanVar()
        self.plotjd_flag = tk.BooleanVar()
        self.lessthan_flag = tk.BooleanVar()
        self.grid_flag.set(True)
        self.errorbar_flag.set(True)
        self.plotjd_flag.set(True)
        self.lessthan_flag.set(False)
        self.grid_flag.trace("w", lambda name, index,
                                         mode: self._entered_star(self.target_list.current()))
        self.errorbar_flag.trace("w", lambda name, index,
                                             mode: self._entered_star(self.target_list.current()))
        self.plotjd_flag.trace("w", lambda name, index,
                                             mode: self._entered_star(self.target_list.current()))
        self.lessthan_flag.trace("w", lambda name, index,
                                             mode: self._entered_star(self.target_list.current()))
        grid_checkbutton = ttk.Checkbutton(checkbutton_frame, text='grid    ', variable=self.grid_flag)
        errorbars_checkbutton = ttk.Checkbutton(checkbutton_frame, text='error bars    ',
                                                variable=self.errorbar_flag)
        plotjd_checkbutton = ttk.Checkbutton(checkbutton_frame, text='plot in JD',
                                             variable=self.plotjd_flag)
        lessthan_checkbutton = ttk.Checkbutton(checkbutton_frame, text='less-thans',
                                               variable=self.lessthan_flag)

        grid_checkbutton.grid(row=0, column=0, sticky='w')
        plotjd_checkbutton.grid(row=0, column=1, sticky='w')
        errorbars_checkbutton.grid(row=1, column=0, sticky='w')
        lessthan_checkbutton.grid(row=1, column=1, sticky='w')

        self.mdf_obs_data = MiniDataFrame()  # declare here, as will be depended upon later.

        # ----- Button frame:
        button_frame = tk.Frame(control_subframe1, pady=12)
        button_frame.grid(sticky='ew')
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_preferences = ttk.Button(button_frame, text='Preferences...',
                                        command=self._preferences_window)
        button_listobservers = ttk.Button(button_frame, text='List Observers',
                                          command=self._listobservers_window)
        button_vsx = ttk.Button(button_frame, text='VSX',
                                command=lambda: web.webbrowse_vsx(self.star_entered.get()))
        button_webobs = ttk.Button(button_frame, text='Observations',
                                   command=lambda: web.webbrowse_webobs(self.star_entered.get()))
        button_clearcache = ttk.Button(button_frame, text='Clear cache',
                                       command=web.get_vsx_obs.cache_clear)
        button_preferences.grid(row=0, column=0, sticky='ew')
        button_listobservers.grid(row=1, column=0, sticky='ew')
        button_vsx.grid(row=0, column=1, sticky='ew')
        button_webobs.grid(row=1, column=1, sticky='ew')
        button_clearcache.grid(row=2, column=1, sticky='ew')
        button_preferences.state(['disabled'])
        button_listobservers.state(['disabled'])
        button_vsx.state(['!disabled'])  # enabled
        button_webobs.state(['!disabled'])  # enabled
        button_clearcache.state(['!disabled'])  # enabled

        # Subframe quit_frame:
        quit_frame = tk.Frame(self.control_frame, height=60)
        quit_frame.grid_columnconfigure(0, weight=1)
        quit_frame.grid(row=2, column=0, padx=8, pady=10, sticky='ew')
        self.quit_button = ttk.Button(quit_frame, text='QUIT pylcg', width=16, cursor='pirate',
                                      command=self._quit_window)
        self.quit_button.grid(row=0, column=0, sticky='ew')

    def _preferences_window(self):
        # 'transient' window style (not modal).
        # Lay out window elements:
        preferences_window = tk.Toplevel(self)
        tk.Label(preferences_window, text='pylcg Preferences').grid(sticky='new')
        preferences_window.transient(self)
        frame1 = ttk.Frame(preferences_window)
        frame1.grid(sticky='ew')
        show_errorbars = ttk.Checkbutton(frame1, text='show errorbars')
        show_errorbars.grid(row=0, column=0)
        show_grid = ttk.Checkbutton(frame1, text='show grid')
        show_grid.grid(row=1, column=0)

    def _about_window(self):
        # TODO: later, probably refactor this "About" window into a separate class.
        about_window = tk.Toplevel(self)
        about_window.transient(self)  # stays on top of main window.
        # about_window.overrideredirect(1)  # plain window.
        about_frame = ttk.Frame(about_window)  # entire window
        about_frame.grid(row=0, column=0, padx=20, pady=10)
        about_frame.columnconfigure(0, minsize=240)
        label_logo = tk.Label(about_frame, text='\n' + PYLCG_LOGO, font=PYLCG_LOGO_FONT, fg='gray')
        label_logo.grid(sticky='ew')
        label_version = tk.Label(about_frame, text=PYLCG_VERSION + ',  ' + PYLCG_VERSION_DATE)
        label_version.grid(sticky='ew')
        label_code = tk.Label(about_frame, text='\nSource code & README at:', justify=tk.LEFT)
        label_code.grid(sticky='w')
        label_repo = tk.Label(about_frame, text=web.PYLCG_REPO_URL, justify=tk.RIGHT,
                              font=PYLCG_REPO_FONT, cursor='hand2')
        label_repo.grid(sticky='e')
        label_py_version = tk.Label(about_frame, text='running py ' +
                                                      sys.version.split('|')[0].split()[0].strip(),
                                    font=ABOUT_AUTHOR_FONT, justify=tk.CENTER)
        label_py_version.grid(sticky='ew')
        # next line: odd syntax, but one must account for .bind()'s including event as a parameter:
        label_repo.bind('<Button-1>', lambda event: web.webbrowse_repo())
        quit_frame = tk.Frame(about_frame, height=60)
        quit_frame.grid_columnconfigure(0, weight=1)
        quit_frame.grid(padx=8, pady=32, sticky='ew')
        quit_button = ttk.Button(quit_frame, text='Close', width=16, cursor='star',
                                 command=about_window.destroy)  # (not .quit(), which would exit pylcg)
        quit_button.grid(sticky='ew')
        label_author = tk.Label(about_frame, text=ABOUT_AUTHOR, font=ABOUT_AUTHOR_FONT, justify=tk.CENTER)
        label_author.grid(sticky='ew')

    def _listobservers_window(self):
        """  Postponed until later version, if there is demand for it."""
        pass

    def _quit_window(self):
        """  Popup window to ensure user really wants to quit. Stops entire program if user confirms.
        :return [None]
        """
        # self.quit_button.config(state='disabled')
        if tkm.askokcancel('Quit?', 'You really want to quit pylcg?'):
            self.preferences.write_current_config_to_ini_file()
            self.quit()     # stop mainloop
            self.destroy()  # prevent Fatal Python Error: PyEval_RestoreThread: NULL tstate

    def _add_upload_star_ids(self):
        # tk.Tk.withdraw()
        self.update()
        # TODO: Add initialdir= option when it's added to preferences.
        fullpath = filedialog.askopenfilename(filetypes=(("Text File", "*.txt"), ("All Files", "*.*")),
                                              title="Choose an upload file.")
        self.update()
        new_star_ids = get_star_ids_from_upload_file(fullpath)
        if len(new_star_ids) >= 1:
            self.target_list.add(new_star_ids)
            # TODO: Add popup of # star ids added.
            self.star_entered.set(self.target_list.current())
            self.button_prev.config(state=(tk.NORMAL if self.target_list.prev_exists() else tk.DISABLED))
            self.button_next.config(state=(tk.NORMAL if self.target_list.next_exists() else tk.DISABLED))
            if self.target_list.current() is not None:
                self._plot_star(self.target_list.current(), True)
        else:
            # TODO: Add popup 'No stars found in file [fullpath].'
            iii = 3

    def _entered_star(self, star_id):
        if self.target_list.current() is None:
            if star_id is not None:
                self.target_list.add(star_id)
        else:
            if self.target_list.current().lower().strip() != star_id.lower().strip():
                self.target_list.add(star_id)
        self.button_prev.config(state=(tk.NORMAL if self.target_list.prev_exists() else tk.DISABLED))
        self.button_next.config(state=(tk.NORMAL if self.target_list.next_exists() else tk.DISABLED))
        if self.target_list.current() is not None:
            self._plot_star(star_id, True)

    def _prev_star(self):
        if self.target_list.prev_exists():
            star_id = self.target_list.go_prev()
            self.star_entered.set(star_id)
            self._plot_star(star_id)
        self.button_prev.config(state=(tk.NORMAL if self.target_list.prev_exists() else tk.DISABLED))
        self.button_next.config(state=(tk.NORMAL if self.target_list.next_exists() else tk.DISABLED))

    def _next_star(self):
        if self.target_list.next_exists():
            star_id = self.target_list.go_next()
            self.star_entered.set(star_id)
            self._plot_star(star_id)
        self.button_prev.config(state=(tk.NORMAL if self.target_list.prev_exists() else tk.DISABLED))
        self.button_next.config(state=(tk.NORMAL if self.target_list.next_exists() else tk.DISABLED))

    def _use_now(self):
        """  Set GUI's End JD entry box to current JD. """
        self.timeend.set('{:20.6f}'.format(jd_now()).strip())

    def _update_bands_to_plot_then_plot(self):
        """  Provides a single function call to GUI components as they require. """
        self._update_bands_to_plot()
        if self.target_list.current() is not None:
            if self.target_list.current().strip() != '':
                self._plot_star(self.target_list.current())  # update plot, but data already downloaded.

    def _update_bands_to_plot(self):
        """  Memorizes band checkbutton seetings before use in plotting.
             Typically called whenever user changes a band checkbutton.
             :return [None]
        """
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

    def _get_plot_start_end(self):
        try:
            num_days = float(self.days_to_plot.get())
        except ValueError:
            num_days = None
        jd_start = jd_from_any_date_string(self.timestart.get())
        jd_end = jd_from_any_date_string(self.timeend.get())

        if self.timestart_valid and self.timeend_valid:
            # Use jd_start and jd_end, ignore num_days:
            self.timestart_flag_label.config(fg='green', bg='#afa')
            self.timeend_flag_label.config(fg='green', bg='#afa')
            self.days_flag_label.config(fg='gray', bg=self.label_background_color)
            return jd_start, jd_end
        if self.timestart_valid and self.days_valid:
            # Use jd_start and num_days:
            self.timestart_flag_label.config(fg='green', bg='#afa')
            self.timeend_flag_label.config(fg='gray', bg=self.label_background_color)
            self.days_flag_label.config(fg='green', bg='#afa')
            return jd_start, jd_start + num_days
        if self.timeend_valid and self.days_valid:
            # Use jd_end and num_days:
            self.timestart_flag_label.config(fg='gray', bg=self.label_background_color)
            self.timeend_flag_label.config(fg='green', bg='#afa')
            self.days_flag_label.config(fg='green', bg='#afa')
            return jd_end - num_days, jd_end
        # If here, not enough good entries to define time span.
        self.timestart_flag_label.config(fg='red', bg='#faa')
        self.timeend_flag_label.config(fg='red', bg='#faa')
        self.days_flag_label.config(fg='red', bg='#faa')
        return None, None

    def _set_time_flags(self, to_gray=True):
        """  Set the check-mark, wrong-mark, or blank flags just to the right of the Time Span items.
        :param to_gray: True if flag marks to be written in gray (not yet used in a plot) [boolean].
        :return: [no return]
        """
        num_days_entry = self.days_to_plot.get()
        if num_days_entry.strip() == '':
            self.days_valid = None
        else:
            try:
                num_days = float(num_days_entry)
            except ValueError:
                num_days = None
            if num_days is None:
                self.days_valid = False
            else:
                self.days_valid = (num_days > 0)  # valid iff positive number.
        self.days_flag_label['text'] = VALIDITY_TO_MARK[self.days_valid]

        timestart_entry = self.timestart.get()
        if timestart_entry.strip() == '':
            self.timestart_valid = None
        else:
            jd_start = jd_from_any_date_string(timestart_entry)
            if jd_start is None:
                self.timestart_valid = False
            else:
                self.timestart_valid = (MIN_JD_ALLOWABLE <= jd_start <= MAX_JD_ALLOWABLE)
        self.timestart_flag_label['text'] = VALIDITY_TO_MARK[self.timestart_valid]

        timeend_entry = self.timeend.get()
        if timeend_entry.strip() == '':
            self.timeend_valid = None
        else:
            jd_end = jd_from_any_date_string(timeend_entry)
            if jd_end is None:
                self.timeend_valid = False
            else:
                # TODO: check > (jd_start if not None).
                self.timeend_valid = (MIN_JD_ALLOWABLE <= jd_end <= MAX_JD_ALLOWABLE)
        self.timeend_flag_label['text'] = VALIDITY_TO_MARK[self.timeend_valid]

        if to_gray is True:
            self.days_flag_label.config(fg='gray', bg=self.label_background_color)
            self.timestart_flag_label.config(fg='gray', bg=self.label_background_color)
            self.timeend_flag_label.config(fg='gray', bg=self.label_background_color)

    def _plot_star(self, star_id, must_get_obs_data=True):
        """  Assembles required data, and passes it to module plot.py, which does makes the plot.
        :param star_id: ID of star to plot, read from GUI entry box.
        :param must_get_obs_data: True iff new data needs to be downloaded from AAVSO.
        :return [None]
        """
        self._update_bands_to_plot()  # ensure sync with checkbuttons.
        self.preferences.set('Data preferences', 'bands', self.bands_to_plot)  # ensure bands are stored.
        if star_id.strip() == '':
            return
        jd_start, jd_end = self._get_plot_start_end()
        if (jd_start is None) or (jd_end is None):
            return
        if must_get_obs_data:
            self.mdf_obs_data = web.get_vsx_obs(star_id=star_id,
                                                jd_start=jd_start, jd_end=jd_end,
                                                num_days=jd_end - jd_start)
        # print(web.get_vsx_obs.cache_info())  # show cache hits, number of entries, etc
        plotter.redraw_plot(self.canvas, self.mdf_obs_data, star_id, bands_to_plot=self.bands_to_plot,
                            show_errorbars=self.errorbar_flag.get(), show_grid=self.grid_flag.get(),
                            show_lessthans=self.lessthan_flag.get(),
                            jd_start=jd_start, jd_end=jd_end, num_days=jd_end - jd_start)


# ***** Python file entry here. *****
# We must do without entry via functions, because tkinter just can't do that right.
# Thus, enter via this python file. We'll add arguments later, if necessary.
# Sigh.
# Well, at least this might later facilitate the making of executables for distribution.
if __name__ == "__main__":
    app = ApplicationPylcg()
    app.mainloop()

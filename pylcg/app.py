from collections import OrderedDict

import matplotlib
matplotlib.use('TkAgg')  # graphics backend
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import style
from matplotlib import pyplot as plt

import tkinter as tk
from tkinter import ttk

import pylcg.settings as settings
import pylcg.plot as plotter
import pylcg.web as web
from pylcg.util import jd_now

__author__ = "Eric Dose :: New Mexico Mira Project, Albuquerque"

PYLCG_LOGO = 'pylcg v0.1'
PYLCG_LOGO_FONT = ('consolas', 20)
PYLCG_SUB_LOGO = 'for local testing only'
PYLCG_SUB_LOGO_FONT = ('consolas', 9)


class ApplicationPylcg(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        # self.iconbitmap(self, default='app_icon.ico')  # must be an icon file
        tk.Tk.wm_title(self, 'pylcg  -- Light Curve Generator in python 3')
        self.resizable(True, True)

        # main_frame (fills entire application window):
        self.main_frame = tk.Frame(self)
        self.main_frame.grid()
        self.main_frame.pack(side="top", fill="both", expand=True)

        # Build menu bar:
        menubar = tk.Menu(self.main_frame)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label='Exit', command=quit)
        menubar.add_cascade(label='File', menu=file_menu)
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label='Reload User Settings', command=settings.UserSettings.reload_all)
        settings_menu.add_command(label='Set all Settings to Defaults',
                                  command=settings.UserSettings.set_all_to_defaults)
        menubar.add_cascade(label='Settings', menu=settings_menu)
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label='Browse pylcg repo', command=web.browse_repo)
        help_menu.add_command(label='About', command=self.about_popup)
        menubar.add_cascade(label='Help', menu=help_menu)
        tk.Tk.config(self, menu=menubar)

        # main_frame:
        self.main_frame.grid_rowconfigure(0, weight=1)     # display_frame expandable.
        self.main_frame.grid_columnconfigure(0, weight=1)  # "
        display_frame = tk.Frame(self.main_frame)
        self.control_frame = tk.Frame(self.main_frame, width=300)
        display_frame.grid(row=0, column=0, sticky='nsew')
        self.control_frame.grid(row=0, column=1, sticky='ns')

        # display_frame:
        display_frame.grid_rowconfigure(0, weight=1)     # plot_frame expandable.
        display_frame.grid_columnconfigure(0, weight=1)  # "
        plot_frame = tk.Frame(display_frame)
        toolbar_frame = tk.Frame(display_frame)
        plot_frame.grid(row=0, column=0, sticky='nsew')
        toolbar_frame.grid(row=1, column=0, padx=125, sticky='w')
        plot_frame.grid_rowconfigure(0, weight=1)
        plot_frame.grid_columnconfigure(0, weight=1)

        # Plot frame (matplotlib):
        fig = Figure(figsize=(10.24, 7.20), dpi=100)
        ax = fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(fig, plot_frame)
        self.canvas.show()

        # Toolbar:
        # note: NavigationToolbar2TkAgg must be isolated in its own frame.
        toolbar = NavigationToolbar2TkAgg(self.canvas, toolbar_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.update()

        # Control Frame:
        self.control_frame.grid_rowconfigure(1, weight=1)
        self.control_frame.grid_columnconfigure(0, weight=1)

        # Logo frame:
        logo_frame = ttk.Frame(self.control_frame)
        logo_frame.grid(row=0, column=0, padx=20, pady=15)
        label_logo = tk.Label(logo_frame, text='\n' + PYLCG_LOGO, font=PYLCG_LOGO_FONT, fg='gray')
        label_logo.grid(sticky='sew')
        label_logo = tk.Label(logo_frame, text=PYLCG_SUB_LOGO, font=PYLCG_SUB_LOGO_FONT, fg='black')
        label_logo.grid(sticky='sew')

        # Subframe 'control_subframe1':
        self.control_subframe1 = ttk.Frame(self.control_frame, padding=5)
        self.control_subframe1.grid(row=1, column=0, sticky=tk.N)
        self.control_subframe1.grid_columnconfigure(0, weight=1)
        self.control_subframe1.grid_columnconfigure(1, weight=1)

        # Star labelframe:
        star_labelframe = tk.LabelFrame(self.control_subframe1, text=' Star ', padx=10, pady=10)
        star_labelframe.grid(pady=15, sticky='ew')
        # self.this_star = tk.StringVar()
        # self.this_star.trace("w", lambda name, index, mode: print(self.this_star.get()))
        # self.this_star.set('xxxxx')
        self.star_entry = ttk.Entry(star_labelframe)
        self.star_entry.grid(row=0, columnspan=2, sticky='ew')
        self.button_prev = ttk.Button(star_labelframe, text='Prev', command=self._prev_star)
        self.button_prev.grid(row=1, column=0, sticky='e')
        self.button_next = ttk.Button(star_labelframe, text='Next', command=self._next_star)
        self.button_next.grid(row=1, column=1, sticky='w')

        # Time span labelframe:
        timespan_labelframe = tk.LabelFrame(self.control_subframe1, text=' Time span ', padx=10, pady=10)
        timespan_labelframe.grid(pady=15, sticky='ew')
        timespan_labelframe.grid_columnconfigure(1, weight=1)
        # self.days = tk.StringVar()
        self.days_entry = ttk.Entry(timespan_labelframe, width=8)
        self.days_entry.grid(row=0, column=0, columnspan=2, sticky='ew')
        days_label = tk.Label(timespan_labelframe, text=' days')
        days_label.grid(row=0, column=2)
        jdstart_label = ttk.Label(timespan_labelframe, text='JD Start: ')
        jdstart_label.grid(row=1, column=0)
        # self.jdstart = tk.StringVar()
        self.jdstart_entry = ttk.Entry(timespan_labelframe, width=12, justify=tk.RIGHT)
        self.jdstart_entry.grid(row=1, column=1, columnspan=2, sticky='ew')
        jdend_label = ttk.Label(timespan_labelframe, text='JD End: ')
        jdend_label.grid(row=2, column=0)
        # self.jdend = tk.StringVar()
        self.jdend_entry = ttk.Entry(timespan_labelframe, width=12, justify=tk.RIGHT)
        self.jdend_entry.grid(row=2, column=1, columnspan=2, sticky='ew')
        use_now_button = ttk.Button(timespan_labelframe, text='JD End = Now', command=self._use_now)
        use_now_button.grid(row=3, column=1, columnspan=2, sticky='ew')

        # Bands labelframe:
        self.bands_labelframe = tk.LabelFrame(self.control_subframe1, text=' Bands ', padx=15, pady=10)
        self.bands_labelframe.grid(pady=15, sticky='ew')
        self.bands_labelframe.grid_columnconfigure(0, weight=1)
        self.bands_labelframe.grid_columnconfigure(1, weight=1)

        self.bands_gui = OrderedDict()
        self.bands_gui['U'] = tk.BooleanVar()
        self.bands_gui['V'] = tk.BooleanVar()
        self.bands_gui['B'] = tk.BooleanVar()
        self.bands_gui['R'] = tk.BooleanVar()
        self.bands_gui['I'] = tk.BooleanVar()
        self.bands_gui['Vis'] = tk.BooleanVar()
        self.bands_gui['TG'] = tk.BooleanVar()
        self.bands_gui['others'] = tk.BooleanVar()
        self.bands_gui['ALL'] = tk.BooleanVar()

        # self.band_u.trace("w", lambda name, index, mode: print(self.bands_gui['U'].get()))
        # self.band_u.set(True) ; self.band_u.set(False) ; self.band_u.set(True)
        self.band_u_checkbutton = ttk.Checkbutton(self.bands_labelframe, text='U      ',
                                                  variable=self.bands_gui['U'],
                                                  command=self._update_active_bands)
        self.band_b_checkbutton = ttk.Checkbutton(self.bands_labelframe, text='B',
                                                  variable=self.bands_gui['B'],
                                                  command=self._update_active_bands)
        self.band_v_checkbutton = ttk.Checkbutton(self.bands_labelframe, text='V',
                                                  variable=self.bands_gui['V'],
                                                  command=self._update_active_bands)
        self.band_r_checkbutton = ttk.Checkbutton(self.bands_labelframe, text='R',
                                                  variable=self.bands_gui['R'],
                                                  command=self._update_active_bands)
        self.band_i_checkbutton = ttk.Checkbutton(self.bands_labelframe, text='I',
                                                  variable=self.bands_gui['I'],
                                                  command=self._update_active_bands)
        self.band_vis_checkbutton = ttk.Checkbutton(self.bands_labelframe, text='Vis',
                                                    variable=self.bands_gui['Vis'],
                                                    command=self._update_active_bands)
        self.band_tg_checkbutton = ttk.Checkbutton(self.bands_labelframe, text='TG',
                                                   variable=self.bands_gui['TG'],
                                                   command=self._update_active_bands)
        self.band_others_checkbutton = ttk.Checkbutton(self.bands_labelframe, text='others',
                                                       variable=self.bands_gui['others'],
                                                       command=self._update_active_bands)
        self.band_all_checkbutton = ttk.Checkbutton(self.bands_labelframe, text='ALL',
                                                    variable=self.bands_gui['ALL'],
                                                    command=self._update_active_bands)

        self.band_u_checkbutton.grid(row=0, column=0, sticky='w')
        self.band_b_checkbutton.grid(row=1, column=0, sticky='w')
        self.band_v_checkbutton.grid(row=2, column=0, sticky='w')
        self.band_r_checkbutton.grid(row=3, column=0, sticky='w')
        self.band_i_checkbutton.grid(row=4, column=0, sticky='w')
        self.band_vis_checkbutton.grid(row=0, column=1, sticky='w')
        self.band_tg_checkbutton.grid(row=1, column=1, sticky='w')
        self.band_others_checkbutton.grid(row=2, column=1, sticky='w')
        self.band_all_checkbutton.grid(row=4, column=1, sticky='w')

        button_moresettings = ttk.Button(self.control_subframe1, text='More settings...',
                                         command=self._moresettings)
        button_moresettings.grid(pady=5, sticky='ew')
        button_listobservers = ttk.Button(self.control_subframe1, text='List Observers',
                                          command=self._listobservers)
        button_listobservers.grid(pady=5, sticky='ew')

        # Quit frame:
        quit_frame = tk.Frame(self.control_frame, height=60)
        quit_frame.grid(row=2, column=0, pady=10)
        self.quit_button = ttk.Button(quit_frame, text='QUIT pylcg', width=16, cursor='pirate',
                                      command=self._quit_window)
        self.quit_button.grid(row=0, column=0)

        # TODO: here, populate all widgets with default values.

        # Start processing:

        # ---------- The following lines are temporary, to support local testing (will later be passed in):
        self.star_ids = ['UZ Cam', 'ST Tri']
        self.bands_to_draw = ['V', 'R', 'I', 'B']
        self.i_star = 0  # just to get us started.
        self.jd_end = None  # indicating now.
        self.num_days = 500  # to get us started.
        # ---------- End temporary lines.

        # Plot the first star (without waiting for button press):
        self._plot_star(self.star_ids[0], get_obs_data=True)
        if self.i_star >= len(self.star_ids) - 1:
            self.button_next.config(state='disabled')

    def _quit_window(self):
        print('Quit was pressed...stopping now.')
        self.quit_button.config(state='disabled')
        # plotter.message_popup("You're leaving me???")
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
        self.jdend_entry.delete(0, tk.END)
        self.jdend_entry.insert(0, '{:20.6f}'.format(jd_now()).strip())

    def _moresettings(self):
        pass
        # self.jdstart_entry.delete(0, tk.END)
        # self.jdstart_entry.insert(0, '_moresettings(): ' + str(self.band_u.get()))
        print('_moresettings(): ', str(self.bands_gui['U'].get()))

    def _listobservers(self):
        pass

    def _update_active_bands(self):
        pass
        # print('_update_active_bands(): ', ' '.join([str(v.get())[0] for v in self.bands_gui.values()]))

    def _plot_star(self, star_id, get_obs_data=True):
        if get_obs_data:
            self.df = web.get_vsx_obs(star_id)
        plotter.redraw_plot(self.canvas, self.df, star_id, self.bands_to_draw,
                            jd_start=None, jd_end=None, num_days=500)

    def about_popup(self):
        pass


# ***** Python file entry here. *****
# We must do without entry via functions, because tkinter just can't do that right.
# Thus, enter via this python file. We'll add arguments later, if necessary.
# Sigh.
# Well, at least this might later facilitate the making of executables for distribution.
if __name__ == "__main__":
    app = ApplicationPylcg()
    app.mainloop()

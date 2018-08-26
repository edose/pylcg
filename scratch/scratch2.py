import matplotlib
matplotlib.use('TKAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as pltlib
import tkinter
from tkinter import *
import numpy as np
import scipy as sc

__author__ = \
    'adapted from https://stackoverflow.com/questions/11270078/' \
    'how-do-i-refresh-a-matplotlib-plot-in-a-tkinter-window'


# Make object for application:
class App_Window(tkinter.Tk):
    def __init__(self,parent):
        tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        button = tkinter.Button(self,text="Open File", command=self.OnButtonClick).pack(side=tkinter.TOP)
        self.canvasFig = pltlib.figure(1)
        Fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
        FigSubPlot = Fig.add_subplot(111)
        x = []
        y = []
        self.line1, = FigSubPlot.plot(x, y, 'r-')
        self.canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(Fig, master=self)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        self.canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        self.resizable(True, True)
        self.update()
        self.OnButtonClick()  # to draw first plot without manually clicking button.

    def refreshFigure(self, x, y):
        self.line1.set_data(x, y)
        ax = self.canvas.figure.axes[0]
        ax.set_xlim(x.min(), x.max())
        ax.set_ylim(y.min(), y.max())
        self.canvas.draw()

    def OnButtonClick(self):
        # file is opened here and some data is taken
        # I've just set some arrays here so it will compile alone
        import random
        x = []
        y = []
        increment = random.random()
        for num in range(0, 1000):
            x.append(num * increment + 1)
        # just some random function is given here, the real data is a UV-Vis spectrum
        for num2 in range(0, 1000):
            y.append(random.random())
            # y.append(sc.math.sin(num2*.06)+sc.math.e**(num2*.001))
        X = np.array(x)
        Y = np.array(y)
        self.refreshFigure(X,Y)


if __name__ == "__main__":
    MainWindow = App_Window(None)
    MainWindow.mainloop()

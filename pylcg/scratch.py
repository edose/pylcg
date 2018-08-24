import matplotlib
matplotlib.use('TkAgg')  # graphics backend
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
from matplotlib import pyplot as plt

import tkinter as tk
from tkinter import ttk

import urllib
import json

import pandas as pd
import numpy as np

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)

style.use('ggplot')

f = Figure(figsize=(10, 6), dpi=100)
a = f.add_subplot(111)  # one chart only, Vasily


def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title('!')
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side='top', fill='x', pady=10)
    B1 = ttk.Button(popup, text='Okay', command=popup.destroy)
    B1.pack()
    popup.mainloop()


exchange = 'BTC-e'  # beginning value
DatCounter = 9000  # to force update
programName = 'btce'  # beginning value
resampleSize = '15Min'  # beginning value
DataPace = '1d'  # beginning value
candleWidth = 0.008  # beginning value
topIndicator = 'none'  # beginning value
bottomIndicator = 'none'  # beginning value
middleIndicator = 'none'  # beginning value
chartLoad = True
EMAs = []  # beginning value
SMAs = []  # beginning value


def tutorial():
    # def leavemini(what):
    #     what.destroy()
    def page2():
        tut.destroy()
        tut2 = tk.Tk()

        def page3():
            tut2.destroy()
            tut3 = tk.Tk()
            tut3.wm_title('Part 3')
            label = ttk.Label(tut3, text='Part 3', font=NORM_FONT)
            label.pack(side='top', fill='x', pady=10)
            B1 = ttk.Button(tut3, text='Done!', command=tut3.destroy)
            B1.pack()
            tut3.mainloop()

        tut2.wm_title('Part 2')
        label = ttk.Label(tut2, text='Part 2', font=NORM_FONT)
        label.pack(side='top', fill='x', pady=10)
        B1 = ttk.Button(tut2, text='Next!', command=page3)
        B1.pack(side='top', fill='x', pady=10)
        tut2.mainloop()

    tut = tk.Tk()
    tut.wm_title('Tutorial')
    label = ttk.Label(tut, text='What do you need help with?', font=NORM_FONT)
    label.pack(side='top', fill='x', pady=10)
    B1 = ttk.Button(tut, text='Overview of the application', command=page2)
    B1.pack()
    B2 = ttk.Button(tut, text='How do I trade with this client?',
                    command=lambda: popupmsg('Not yet completed.'))
    B2.pack()
    B3 = ttk.Button(tut, text='Indicator questions/Help', command=lambda: popupmsg('Not yet completed.'))
    B3.pack()
    tut.mainloop()


def loadChart(run):
    global chartLoad
    if run == 'start':
        chartLoad = True
    elif run == 'start':
        chartLoad = False


def addMiddleIndicator(what):
    global middleIndicator
    global DatCounter
    if DataPace == 'tick':
        popupmsg('Indicators in Tick Data not available.')
    if what != 'none':
        if middleIndicator == 'none':
            if what == 'sma':
                midIQ = tk.Tk()
                midIQ.wm_title('Periods?')
                label = ttk.Label(midIQ, text='Choose how many periods.')
                label.pack(side='top', fill='x', pady=10)
                e = ttk.Entry(midIQ)
                e.insert(0, 10)
                e.pack()
                e.focus_set()

                def callback():
                    global middleIndicator
                    global DatCounter
                    middleIndicator = []
                    periods = (e.get())
                    group = []
                    group.append('sma')
                    group.append(int(periods))
                    middleIndicator.append(group)
                    DatCounter = 9000
                    print('middle indicator set to:', middleIndicator)
                    midIQ.destroy()
                b = ttk.Button(midIQ, text='Submit', width=10, command=callback)
                b.pack()
                tk.mainloop()
            if what == 'ema':
                midIQ = tk.Tk()
                midIQ.wm_title('Periods?')
                label = ttk.Label(midIQ, text='Choose how many periods.')
                label.pack(side='top', fill='x', pady=10)
                e = ttk.Entry(midIQ)
                e.insert(0, 10)
                e.pack()
                e.focus_set()

                def callback():
                    global middleIndicator
                    global DatCounter
                    middleIndicator = []
                    periods = (e.get())
                    group = []
                    group.append('ema')
                    group.append(int(periods))
                    middleIndicator.append(group)
                    DatCounter = 9000
                    print('middle indicator set to:', middleIndicator)
                    midIQ.destroy()
                b = ttk.Button(midIQ, text='Submit', width=10, command=callback)
                b.pack()
                tk.mainloop()
        else:
            if what == 'sma':
                midIQ = tk.Tk()
                midIQ.wm_title('Periods?')
                label = ttk.Label(midIQ, text='Choose how many periods.')
                label.pack(side='top', fill='x', pady=10)
                e = ttk.Entry(midIQ)
                e.insert(0, 10)
                e.pack()
                e.focus_set()

                def callback():
                    global middleIndicator
                    global DatCounter
                    # middleIndicator = []
                    periods = (e.get())
                    group = []
                    group.append('sma')
                    group.append(int(periods))
                    middleIndicator.append(group)
                    DatCounter = 9000
                    print('middle indicator set to:', middleIndicator)
                    midIQ.destroy()
                b = ttk.Button(midIQ, text='Submit', width=10, command=callback)
                b.pack()
                tk.mainloop()
            if what == 'ema':
                midIQ = tk.Tk()
                midIQ.wm_title('Periods?')
                label = ttk.Label(midIQ, text='Choose how many periods.')
                label.pack(side='top', fill='x', pady=10)
                e = ttk.Entry(midIQ)
                e.insert(0, 10)
                e.pack()
                e.focus_set()

                def callback():
                    global middleIndicator
                    global DatCounter
                    # middleIndicator = []
                    periods = (e.get())
                    group = []
                    group.append('ema')
                    group.append(int(periods))
                    middleIndicator.append(group)
                    DatCounter = 9000
                    print('middle indicator set to:', middleIndicator)
                    midIQ.destroy()
                b = ttk.Button(midIQ, text='Submit', width=10, command=callback)
                b.pack()
                tk.mainloop()
    else:
        middleIndicator = 'none'


def addTopIndicator(what):
    global topIndicator
    global DatCounter
    if DataPace == 'tick':
        popupmsg('Indicators in Tick Data not available.')
    elif what == 'none':
        topIndicator = what
        DatCounter = 9000
    elif what == 'rsi':
        rsiQ = tk.Tk()
        rsiQ.wm_title('Periods?')
        label = ttk.Label(rsiQ, text="choose how many periods.")
        label.pack(side='top', fill='x', pady=10)
        e = ttk.Entry(rsiQ)
        e.insert(0, 14)
        e.pack()
        e.focus_set()

        def callback():
            global topIndicator
            global DatCounter
            periods = (e.get())
            group = []
            group.append('rsi')
            group.append(periods)
            topIndicator = group
            DatCounter = 9000  # force update
            print('Set top indicator to ', group)
            rsiQ.destroy()

        b = ttk.Button(rsiQ, text='Submit', width=10, command=callback)
        b.pack()
        tk.mainloop()
    elif what == 'macd':
        topIndicator = 'macd'
        DatCounter = 9000


def addBottomIndicator(what):
    global bottomIndicator
    global DatCounter
    if DataPace == 'tick':
        popupmsg('Indicators in Tick Data not available.')
    elif what == 'none':
        bottomIndicator = what
        DatCounter = 9000
    elif what == 'rsi':
        rsiQ = tk.Tk()
        rsiQ.wm_title('Periods?')
        label = ttk.Label(rsiQ, text="choose how many periods.")
        label.pack(side='top', fill='x', pady=10)
        e = ttk.Entry(rsiQ)
        e.insert(0, 14)
        e.pack()
        e.focus_set()

        def callback():
            global bottomIndicator
            global DatCounter
            periods = (e.get())
            group = []
            group.append('rsi')
            group.append(periods)
            bottomIndicator = group
            DatCounter = 9000  # force update
            print('Set bottom indicator to ', group)
            rsiQ.destroy()

        b = ttk.Button(rsiQ, text='Submit', width=10, command=callback)
        b.pack()
        tk.mainloop()
    elif what == 'macd':
        bottomIndicator = 'macd'
        DatCounter = 9000


def changeTimeFrame(tf):
    global DataPace
    global DatCounter
    if tf == '7d' and resampleSize == '1Min':
        popupmsg('Too much data chosen, choose a smaller time frame or OHLC Interval')
    else:
        DataPace = tf
        DatCounter = 9000


def changeSampleSize(size, width):
    global resampleSize
    global DatCounter
    global candleWidth
    if DataPace == '7d' and resampleSize == '1Min':
        popupmsg('Too much data chosen, choose a smaller time frame or OHLC Interval')
    elif DataPace == 'tick':
        popupmsg('You are currently viewing tick data, not OhLC.')
    else:
        resampleSize = size
        DatCounter = 9000
        candleWidth = width


def changeExchange(toWhat, pn):
    global exchange
    global DatCounter
    global programName
    exchange = toWhat
    programName = pn
    DatCounter = 9000  # in theory forces update


def animate(i):
    pullData = open('sampleData.txt', 'r').read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            xList.append(int(x))
            yList.append(int(y))
    a.clear()
    a.plot(xList, yList, 'g', label='buys')
    a.legend(bbox_to_anchor=(0, 1.02, 1, .102), loc=3, ncol=2, borderaxespad=0)

    title = 'Hey Hey this is the title'
    a.set_title(title)


class SeaofBTCapp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # tk.Tk.iconbitmap(self, default='clienticon.ico')  # must be an icon file
        tk.Tk.wm_title(self, 'This is the window title')

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Build menu bar:
        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='Save settings', command=lambda: popupmsg('Not supported just yet.'))
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=quit)
        menubar.add_cascade(label='File', menu=filemenu)
        exchangeChoice = tk.Menu(menubar, tearoff=1)
        exchangeChoice.add_command(label='BTC-e', command=lambda: changeExchange('BTC-e', 'btce'))
        exchangeChoice.add_command(label='Bitfinex', command=lambda: changeExchange('Bitfinex', 'bitfinex'))
        exchangeChoice.add_command(label='Bitstamp', command=lambda: changeExchange('Bitstamp', 'bitstamp'))
        exchangeChoice.add_command(label='Huobi', command=lambda: changeExchange('Huobi', 'huobi'))
        menubar.add_cascade(label='Exchange', menu=exchangeChoice)
        dataTF = tk.Menu(menubar, tearoff=1)
        dataTF.add_command(label='Tick', command=lambda: changeTimeFrame('tick'))
        dataTF.add_command(label='1 Day', command=lambda: changeTimeFrame('1d'))
        dataTF.add_command(label='3 Day', command=lambda: changeTimeFrame('3d'))
        dataTF.add_command(label='1 Week', command=lambda: changeTimeFrame('7d'))
        menubar.add_cascade(label='Data Time Frame', menu=dataTF)
        OHLCI = tk.Menu(menubar, tearoff=1)
        OHLCI.add_command(label='Tick', command=lambda: changeTimeFrame('tick'))
        OHLCI.add_command(label='1 Minute', command=lambda: changeSampleSize('1Min', 0.0005))
        OHLCI.add_command(label='5 Minute', command=lambda: changeSampleSize('5Min', 0.003))
        OHLCI.add_command(label='15 Minute', command=lambda: changeSampleSize('15Min', 0.008))
        OHLCI.add_command(label='30 Minute', command=lambda: changeSampleSize('30Min', 0.016))
        OHLCI.add_command(label='1 Hour', command=lambda: changeSampleSize('1H', 0.032))
        OHLCI.add_command(label='3 Hour', command=lambda: changeSampleSize('3H', 0.096))
        menubar.add_cascade(label='OHLC Interval', menu=OHLCI)
        topIndi = tk.Menu(menubar, tearoff=1)
        topIndi.add_command(label='None', command=lambda: addTopIndicator('none'))
        topIndi.add_command(label='RSI', command=lambda: addTopIndicator('rsi'))
        topIndi.add_command(label='MACD', command=lambda: addTopIndicator('macd'))
        menubar.add_cascade(label='Top Indicator', menu=topIndi)
        mainIndi = tk.Menu(menubar, tearoff=1)
        mainIndi.add_command(label='None', command=lambda: addMiddleIndicator('none'))
        mainIndi.add_command(label='SMA', command=lambda: addMiddleIndicator('sma'))
        mainIndi.add_command(label='EMA', command=lambda: addMiddleIndicator('ema'))
        menubar.add_cascade(label='Main/middle Indicator', menu=mainIndi)
        bottomIndi = tk.Menu(menubar, tearoff=1)
        bottomIndi.add_command(label='None', command=lambda: addBottomIndicator('none'))
        bottomIndi.add_command(label='RSI', command=lambda: addBottomIndicator('rsi'))
        bottomIndi.add_command(label='MACD', command=lambda: addBottomIndicator('macd'))
        menubar.add_cascade(label='Bottom Indicator', menu=bottomIndi)
        tradeButton = tk.Menu(menubar, tearoff=1)
        tradeButton.add_command(label='Manual Trading', command=lambda: popupmsg('Not live yet.'))
        tradeButton.add_command(label='Automated Trading', command=lambda: popupmsg('Not live yet.'))
        tradeButton.add_separator()
        tradeButton.add_command(label='Quick Buy', command=lambda: popupmsg('Not live yet.'))
        tradeButton.add_command(label='Quick Sell', command=lambda: popupmsg('Not live yet.'))
        tradeButton.add_separator()
        tradeButton.add_command(label='Set up Quick Buy/Sell', command=lambda: popupmsg('Not live yet.'))
        menubar.add_cascade(label='Trading', menu=tradeButton)
        startStop = tk.Menu(menubar, tearoff=1)
        startStop.add_command(label='Resume', command=lambda: loadChart('start'))
        startStop.add_command(label='Pause', command=lambda: loadChart('stop'))
        menubar.add_cascade(label='Resume/Pause client', menu=startStop)
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label='Tutorial', command=tutorial)
        menubar.add_cascade(label='Help', menu=helpmenu)

        tk.Tk.config(self, menu=menubar)

        # Build dict of frames:
        self.frames = {}
        for F in (StartPage, PageOne, BTCe_Page):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=("""ALPHA Bitcoin trading application.
        There is no warranty."""), font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text='Agree',
                             command=lambda: controller.show_frame(BTCe_Page))
        button1.pack()
        button2 = ttk.Button(self, text='Disagree', command=quit)
        button2.pack()


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button1 = ttk.Button(self, text='Back to Home',
                             command=lambda: controller.show_frame(StartPage))
        button1.pack()


class BTCe_Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button1 = ttk.Button(self, text='Back to Home',
                             command=lambda: controller.show_frame(StartPage))
        button1.pack()

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


app = SeaofBTCapp()
app.geometry('1280x720')
ani = animation.FuncAnimation(f, animate, interval=1000)  # msec
print('wtf')
app.mainloop()
print('wtf2')



def scratch():
    a.clear()  # where a is axis object, clears figure



# from tkinter import *
# from PIL import Image, ImageTk
#
# __author__ = "Eric Dose :: New Mexico Mira Project, Albuquerque"
#
#
# class Window(Frame):
#     def __init__(self, master=None):
#         Frame.__init__(self, master)
#         self.master = master
#         self.init_window()
#
#     def init_window(self):
#         self.master.title('GUI -- title')
#         self.pack(fill=BOTH, expand=1)
#         # quitButton = Button(self, text='Quit', command=self.client_exit)
#         # quitButton.place(x=0, y=0)  # upper left
#
#         menu = Menu(self.master)
#         self.master.config(menu=menu)
#
#         file = Menu(menu)
#         file.add_command(label='Save')
#         file.add_command(label='Exit', command=self.client_exit)
#         menu.add_cascade(label='File', menu=file)
#
#         edit = Menu(menu)
#         edit.add_command(label='Show Image', command=self.showImg)
#         edit.add_command(label='Show Text', command=self.showTxt)
#         menu.add_cascade(label='Edit', menu=edit)
#
#     def showImg(self):
#         load1 = Image.open('C:/Dev/app_entry_manual/data/pic.jpg')
#         render1 = ImageTk.PhotoImage(load1)
#         img = Label(self, image=render1)
#         img.image = render1
#         img.place(x=0, y=0)
#
#     def showTxt(self):
#         text = Label(self, text='Hey there')
#         text.pack()
#
#
#     def client_exit(self):
#         exit()
#
#
# root = Tk()
# root.geometry('400x300')
# app = Window(root)
# root.mainloop()


# def animate(i):
#     dataLink = 'https://btc-e.com/api/3/trades/btc_usd?limit=2000'  # um, BTC-e seized by Feds 2017.
#     data = urllib.request.urlopen(dataLink)
#     data = data.readall().decode("utf-8")
#     data = json.loads(data)
#     data = data["btc_usd"]
#     data = pd.DataFrame(data)
#
#     buys = data[(data['type'] == "bid")]
#     buys["datestamp"] = np.array(buys["timestamp"]).astype("datetime64[s]")
#     buyDates = (buys["datestamp"]).tolist()
#
#     sells = data[(data['type'] == "ask")]
#     sells["datestamp"] = np.array(sells["timestamp"]).astype("datetime64[s]")
#     sellDates = (sells["datestamp"]).tolist()
#
#     a.clear()
#
#     a.plot_date(buyDates, buys["price"])
#     a.plot_date(sellDates, sells["price"])

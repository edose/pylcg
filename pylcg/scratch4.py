__author__ = "Eric Dose :: New Mexico Mira Project, Albuquerque"

from collections import OrderedDict
from tkinter import *
root = Tk()
states = OrderedDict()


# ********** As OrderedDict:

def xx():
    print(' '.join([str(v.get()) for v in states.values()]))


for i in range(10):
    var = IntVar()
    chk = Checkbutton(root, text=str(i), variable=var, command=xx)
    chk.pack(side=LEFT)
    states[i] = var
root.mainloop()

# ********** As list:
#
# from tkinter import *
# root = Tk()
# states = []
#
#
# def xx():
#     print(' '.join([str(v.get()) for v in states]))
#
#
# for i in range(10):
#     var = IntVar()
#     chk = Checkbutton(root, text=str(i), variable=var, command=xx)
#     chk.pack(side=LEFT)
#     states.append(var)
# root.mainloop()

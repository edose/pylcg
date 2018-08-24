import tkinter as tk


class App(tk.Tk):
    def __init__(self, parent):
        tk.Tk.__init__(self, parent)

        self.band_u = tk.BooleanVar()
        self.band_u_checkbutton = tk.Checkbutton(self, text='U', variable=self.band_u)
        self.band_u_checkbutton.grid()

        self.button_read = tk.Button(self, text='Read U', command=self._read)
        self.button_read.grid()

    def _read(self):
        print('read(): ', str(self.band_u.get()))


def go():
    app = App(None)
    app.mainloop()


if __name__ == "__main__":
    go()



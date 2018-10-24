import tkinter as tk
import tkinter.font as tkfont
import tkinter.ttk as ttk

"""  table_window.py
     Produces a sortable, scrollable table in a standalone window. 
     Relies on tkinter (ttk) TreeView.
     This code adapted beyond any recognition by E. Dose, from code found Oct 23 2018 at:
        https://www.daniweb.com/programming/software-development/threads/350266/creating-table-in-python     
"""


class TableWindow:
    """  Make a sortable, scrollable table in a standalone window, using ttk.TreeView"""
    def __init__(self, parent, window_label, header_text, column_names, data_list,
                 horizontal_scrollbar=False):
        """  Constructor.
        :param parent: parent window from which this is called.
        :param window_label: text that goes in the window's top border [string].
        :param header_text:  text that goes in window, above table [string].
        :param column_names: names of columns, left to right [list of strings].
        :param data_list:  data to go in table, matching column name order [list of tuples].
        :param horizontal_scrollbar: True iff user wants a horizontal scrollbar[boolean].
        """
        self.tree = None
        self.this_frame = None
        self.parent = parent
        self.window_label = window_label
        self.header_text = header_text
        self.column_names = column_names
        self.data_list = data_list
        self.horizontal_scrollbar = horizontal_scrollbar
        self._layout_window()
        self._layout_table()
        self._layout_columns()
        self._populate_table()

    def _layout_window(self):
        # 'transient' window style (not modal).
        self.this_window = tk.Toplevel(self.parent)
        self.this_window.transient(self.parent)
        self.this_window.title(self.window_label)
        header_label = ttk.Label(self.this_window, justify="left", anchor="n", padding=(10, 2, 10, 6),
                                 text=self.header_text)
        header_label.pack(fill='x')
        self.this_frame = ttk.Frame(self.this_window)
        self.this_frame.pack(fill='both', expand=True)

    def _layout_table(self):
        # Create a treeview with vertical scrollbar & optionally horizontal scrollbar:
        self.tree = ttk.Treeview(self.this_frame, columns=self.column_names, show="headings", padding=20)
        vsb = ttk.Scrollbar(self.this_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.grid(column=1, row=0, sticky='ns', in_=self.this_frame)
        if self.horizontal_scrollbar:
            hsb = ttk.Scrollbar(self.this_frame, orient="horizontal", command=self.tree.xview)
            self.tree.configure(xscrollcommand=hsb.set)
            hsb.grid(column=0, row=1, sticky='ew', in_=self.this_frame)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=self.this_frame)
        self.this_frame.grid_columnconfigure(0, weight=1)
        self.this_frame.grid_rowconfigure(0, weight=1)

    def _layout_columns(self):
        """  Add columns to table, and initially adjust each column's width to its header string."""
        for col in self.column_names:
            self.tree.heading(col, text=col.title(), command=lambda c=col: self._sort_by_column(c, 0))
            self.tree.column(col, width=tkfont.Font().measure(col.title()))

    def _populate_table(self):
        """  Add rows (items) to table, and readjust column widths. """
        for item in self.data_list:
            self.tree.insert('', 'end', values=item)
            # adjust column's width if necessary to fit each value
            # TODO: move this loop outside of item loop (in order to loop on columns, not rows).
            for ix, val in enumerate(item):
                col_w = tkfont.Font().measure(val)
                if self.tree.column(self.column_names[ix], width=None) < col_w:
                    self.tree.column(self.column_names[ix], width=col_w)

    def _sort_by_column(self, col, descending):
        """Sort contents whenever user clicks on a column header."""
        # NB: data should be in sortable text format for this method as written.
        data = [(self.tree.set(child, col), child)
                for child in self.tree.get_children('')]  # get table data.
        # Sort the data in place
        data.sort(reverse=descending)
        for ix, item in enumerate(data):
            self.tree.move(item[1], '', ix)
        # switch the heading so it will sort in the opposite direction
        self.tree.heading(col, command=lambda col=col: self._sort_by_column(col, int(not descending)))


# Local data (for local testing only):
local_window_label = 'LIST OBSERVERS'
local_header_text = '\n'.join(['OBSERVERS of this target in plot time range',
                               '   (sort on a column by clicking its header)', ''])
local_column_names = ['car', 'repair']
local_data_list = [
    ('Hyundai', 'brakes'),
    ('Honda', 'light'),
    ('Lexus', 'battery'),
    ('Benz', 'wiper'),
    ('Ford', 'tire'),
    ('Chevy', 'air'),
    ('Chrysler', 'piston'),
    ('Toyota', 'brake pedal'),
    ('BMW', 'seat'),
    ('Subaru', 'eVERYTHING!')
]

# Python module entry here (for local testing only):
if __name__ == "__main__":
    import time
    root = tk.Tk()
    root.wm_title('root label')
    time.sleep(2)
    local_window_table = TableWindow(root,
                                     local_window_label, local_header_text,
                                     local_column_names, local_data_list)
    root.mainloop()

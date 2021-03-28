import tkinter as tk
from tkinter import ttk
from pygedcom.core import Parser


class App(tk.Tk):
    def __init__(self, gedcomfile):
        super().__init__()

        # Window settings
        self.geometry("1240x720")
        self.title('PyGEDCOM')

        # Layout
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=4)
        self.rowconfigure(0, weight=4)
        self.rowconfigure(1, weight=1)

        # Load data
        self.tree = Parser(gedcomfile).build_tree()

        # Create widgets
        self.__create_widgets()

    def __create_widgets(self):
        search_frame = SearchFrame(self)
        search_frame.grid(column=0, row=0, rowspan=2)
        main_frame = MainFrame(self)
        main_frame.grid(column=1, row=0)
        info_frame = InfoFrame(self)
        info_frame.grid(column=1, row=1)

class SearchFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Layout
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        # Create widgets
        self.sv = tk.StringVar()
        self.sv.trace('w', lambda name, index, mode, sv=self.sv: self.on_type_callback())
        self.__create_widgets()

    def __create_widgets(self):
        ttk.Label(self, text='Find person:').grid(column=0, row=0)
        keyword = ttk.Entry(self, width=30, textvariable=self.sv)
        keyword.focus()
        keyword.grid(column=1, row=0)

        columns = ('#1', '#2')
        search_list = ttk.Treeview(self, columns=columns, show='headings')
        search_list.heading('#1', text='Full name')
        search_list.heading('#2', text='Backend ID')
        search_list.grid(column=0, row=1, columnspan=2)

    def on_type_callback(self):
        results = self.nametowidget('.').tree.find(self.sv.get())
        print(results)

class InfoFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Create widgets
        self.__create_widgets()

    def __create_widgets(self):
        pass

class MainFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Create widgets
        self.__create_widgets()

    def __create_widgets(self):
        pass
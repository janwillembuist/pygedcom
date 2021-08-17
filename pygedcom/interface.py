# External imports
import random
import tkinter as tk
from tkinter import ttk, filedialog
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

# Internal imports
from pygedcom import treeplot as treeplt
from pygedcom.gedcomparser import Parser

class App(tk.Tk):
    FRAME_OPTIONS = {
        'borderwidth': 1,
        'padding': '0.15i'
    }
    ANCESTOR_PLOT_DEPTH = 3

    def __init__(self):
        super().__init__()

        # The family tree
        self.tree = None

        # Window settings
        self.geometry("1240x720")
        # self.resizable(width=False, height=False)
        self.title('PyGEDCOM')
        self.option_add('*tearOff', False)
        self.overrideredirect(True)
        # self.attributes('-topmost', 1)

        self.style = ttk.Style(self)
        self.tk.call('source', '../data/themes/forest-light.tcl')
        self.style.theme_use('forest-light')

        # Layout
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=5)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=80)
        self.rowconfigure(2, weight=30)


        # Add sidegrip
        self.sg = ttk.Sizegrip(self)
        self.sg.grid(row=2, column=2, sticky=tk.SE)

        # Create subframes
        self.menu_frame = MenuButtons(self, **self.FRAME_OPTIONS)
        self.menu_frame.grid(column=0, row=0, columnspan=2, sticky='nesw')
        self.search_frame = SearchFrame(self, **self.FRAME_OPTIONS)
        self.search_frame.grid(column=0, row=1, rowspan=2, sticky='nesw')
        self.main_frame = MainFrame(self, **self.FRAME_OPTIONS)
        self.main_frame.grid(column=1, row=1, sticky='nesw')
        self.info_frame = InfoFrame(self, **self.FRAME_OPTIONS)
        self.info_frame.grid(column=1, row=2, sticky='nesw')

    def selectdata(self):
        file = filedialog.askopenfilename()
        self.opendata(file=file)

    def opendata(self, file='../data/555SAMPLE.GED'):
        # Load data
        self.tree = Parser(file).build_tree()

        # Draw random individual
        self.draw_individual(random.choice(list(self.tree.individuals_lookup.keys())))
        self.reset_views()

    def draw_individual(self, selected):
        if selected == 'random':
            selected = random.choice(list(self.tree.individuals_lookup.keys()))
        self.tree.selected_individual = self.tree.individuals[self.tree.individuals_lookup[selected]]

        # Update info and main frame
        self.info_frame.update_callback()
        self.main_frame.update_callback()

    def reset_views(self):
        # Empty search box
        self.search_frame.sv.set('')


class MenuButtons(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Layout
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=10)
        self.rowconfigure(0, weight=1)

        # Move coordinates
        self.x = None
        self.y = None

        self.file = ttk.Button(self, text="Open..", command=self.selectdata)
        self.file.grid(column=0, row=0, sticky='w')
        self.defaultfile = ttk.Button(self, text="Open example", command=self.opendata)
        self.defaultfile.grid(column=1, row=0, sticky='w')
        self.close = ttk.Button(self, text="Close", command=self.quit, style='Accent.TButton')
        self.close.grid(column=2, row=0, sticky='e')

        self.bind("<ButtonPress-1>", self.start_move)
        #self.bind("<ButtonRelease-1>", self.stop_move)
        self.bind("<B1-Motion>", self.do_move)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self):
        self.x = None
        self.y = None

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.nametowidget('.').winfo_x() + deltax
        y = self.nametowidget('.').winfo_y() + deltay
        self.nametowidget('.').geometry(f"+{x}+{y}")

    def selectdata(self):
        file = filedialog.askopenfilename()
        self.opendata(file=file)

    def opendata(self, file='../data/555SAMPLE.GED'):
        # Load data
        self.nametowidget('.').tree = Parser(file).build_tree()

        # Draw random individual
        self.nametowidget('.').draw_individual('random')
        self.nametowidget('.').reset_views()

class SearchFrame(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Layout
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=5)
        self.rowconfigure(2, weight=1)

        # Latest search results
        self.search_results = []

        # Create widgets
        self.sv = tk.StringVar()
        self.sv.trace('w', lambda name, index, mode, sv=self.sv: self.on_type_callback())

        ttk.Label(self, text='Find person:').grid(column=0, row=0)
        keyword = ttk.Entry(self, textvariable=self.sv)
        keyword.focus()
        keyword.grid(column=1, row=0, sticky='we')

        columns = ('#1', '#2')
        self.treeview_widget = ttk.Treeview(self, columns=columns, show='headings', name='search_list')
        self.treeview_widget.heading('#1', text='Full name')
        self.treeview_widget.heading('#2', text='Birth date')
        self.treeview_widget.grid(column=0, row=1, columnspan=2, sticky='nsew')
        self.treeview_widget.bind('<Double-1>', self.select_callback)

        # Create scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.treeview_widget.yview)
        self.scrollbar.grid(column=2, row=1, sticky='ns')

        # Couple scrollbar
        self.treeview_widget.configure(yscrollcommand=self.scrollbar.set)

        self.select_button = ttk.Button(self, text='Select person', command=self.select_callback, style='Accent.TButton')
        self.select_button.grid(column=0, row=2, columnspan=2, sticky='we')

    def on_type_callback(self):
        if self.nametowidget('.').tree is None:
            # No tree is loaded in yet.
            return
        self.search_results = self.nametowidget('.').tree.find(self.sv.get())

        # Delete all items
        for child in self.treeview_widget.get_children():
            self.treeview_widget.delete(child)

        # Set new items
        for person in self.search_results:
            self.treeview_widget.insert('', 0, values=(person.fullname, person.birthdate))

    def select_callback(self, *args):
        selected = self.treeview_widget.focus()
        selected = self.treeview_widget.item(selected)['values'][0]

        # Save in main app
        self.nametowidget('.').draw_individual(selected)


class InfoFrame(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Layout
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=2)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Markup info
        self.fullname = tk.StringVar()
        self.fullname.set('None')
        self.sex = tk.StringVar()
        self.sex.set('None')
        self.birthdate = tk.StringVar()
        self.birthdate.set('None')
        self.deathdate = tk.StringVar()
        self.deathdate.set('None')

        # Create widgets
        ttk.Label(self, text='Full name:').grid(column=0, row=0, sticky='e')
        ttk.Label(self, text='Sex:').grid(column=0, row=1, sticky='e')
        ttk.Label(self, text='Date of birth:').grid(column=2, row=0, sticky='e')
        ttk.Label(self, text='Date of death:').grid(column=2, row=1, sticky='e')
        ttk.Label(self, textvariable=self.fullname).grid(column=1, row=0, sticky='we')
        ttk.Label(self, textvariable=self.sex).grid(column=1, row=1, sticky='we')
        ttk.Label(self, textvariable=self.birthdate).grid(column=3, row=0, sticky='we')
        ttk.Label(self, textvariable=self.deathdate).grid(column=3, row=1, sticky='we')

    def update_callback(self):
        individual = self.nametowidget('.').tree.selected_individual
        self.fullname.set(individual.fullname)
        self.sex.set(individual.sex)
        self.birthdate.set(individual.birthdate)
        self.deathdate.set(individual.deathdate)

class MainFrame(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Create widgets
        self.fig = plt.Figure()
        self.plotaxis = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        # self.toolbar = NavigationToolbar2Tk(self.canvas, self)  # Maybe ditch toolbar?
        self.canvas.get_tk_widget().pack(fill=tk.BOTH)

        # Preconfigure plot window
        self.plotaxis.axis('off')
        self.fig.canvas.mpl_connect('pick_event', self.onpick)

    def update_callback(self):
        tree = self.nametowidget('.').tree.find_ancestors(self.nametowidget('.').ANCESTOR_PLOT_DEPTH)
        treeplt.plot_tree(tree, self.plotaxis)
        self.canvas.draw()

    def onpick(self, event):
        text = event.artist
        person = text.get_text().replace('\n', ' ')
        self.nametowidget('.').draw_individual(person)

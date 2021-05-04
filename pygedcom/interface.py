import tkinter as tk
from tkinter import ttk
from pygedcom.core import Parser


class App(tk.Tk):
    FRAME_OPTIONS = {
        'borderwidth': 1,
        'relief': 'groove',
        'padding': '0.2i'
    }

    def __init__(self, gedcomfile):
        super().__init__()

        # Window settings
        self.geometry("1240x720")
        self.resizable(width=False, height=False)
        self.title('PyGEDCOM')

        # Layout
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=5)
        self.rowconfigure(0, weight=5)
        self.rowconfigure(1, weight=1)

        # Load data
        self.tree = Parser(gedcomfile).build_tree()

        # Placeholder for selected person
        self.selected_individual = None

        # Create subframes
        self.search_frame = SearchFrame(self, **self.FRAME_OPTIONS)
        self.search_frame.grid(column=0, row=0, rowspan=2, sticky='nesw')
        self.main_frame = MainFrame(self, **self.FRAME_OPTIONS)
        self.main_frame.grid(column=1, row=0, sticky='nesw')
        self.info_frame = InfoFrame(self, **self.FRAME_OPTIONS)
        self.info_frame.grid(column=1, row=1, sticky='nesw')

class SearchFrame(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Layout
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        #self.columnconfigure(2, weight=1)
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

        # Create scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.treeview_widget.yview)
        self.scrollbar.grid(column=2, row=1, sticky='ns')

        # Couple scrollbar
        self.treeview_widget.configure(yscrollcommand=self.scrollbar.set)

        self.select_button = ttk.Button(self, text='Select person', command=self.select_callback)
        self.select_button.grid(column=0, row=2, columnspan=2, sticky='we')

    def on_type_callback(self):
        self.search_results = self.nametowidget('.').tree.find(self.sv.get())

        # Delete all items
        for child in self.treeview_widget.get_children():
            self.treeview_widget.delete(child)

        # Set new items
        for person in self.search_results:
            self.treeview_widget.insert('', 0, values=(person.fullname, person.birthdate))

    def select_callback(self):
        selected = self.treeview_widget.focus()
        selected = self.treeview_widget.item(selected)['values'][0]

        # Find corresponding ID and save in main app
        self.nametowidget('.').selected_individual = self.nametowidget('.').tree.individuals_lookup[selected]

        # Update info and main frame
        self.nametowidget('.!infoframe').update_callback()


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
        individual = self.nametowidget('.').tree.individuals[self.nametowidget('.').selected_individual]
        self.fullname.set(individual.fullname)
        self.sex.set(individual.sex)
        self.birthdate.set(individual.birthdate)
        self.deathdate.set(individual.deathdate)

class MainFrame(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Create widgets

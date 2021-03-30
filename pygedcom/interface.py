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

        # Placeholder for selected person
        self.selected_individual = None

        # Create subframes
        self.search_frame = SearchFrame(self)
        self.search_frame.grid(column=0, row=0, rowspan=2)
        self.main_frame = MainFrame(self)
        self.main_frame.grid(column=1, row=0)
        self.info_frame = InfoFrame(self)
        self.info_frame.grid(column=1, row=1)

class SearchFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Layout
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        # Latest search results
        self.search_results = []

        # Create widgets
        self.sv = tk.StringVar()
        self.sv.trace('w', lambda name, index, mode, sv=self.sv: self.on_type_callback())

        ttk.Label(self, text='Find person:').grid(column=0, row=0)
        keyword = ttk.Entry(self, width=30, textvariable=self.sv)
        keyword.focus()
        keyword.grid(column=1, row=0)

        columns = ('#1', '#2')
        self.treeview_widget = ttk.Treeview(self, columns=columns, show='headings', name='search_list')
        self.treeview_widget.heading('#1', text='Full name')
        self.treeview_widget.heading('#2', text='Backend ID')
        self.treeview_widget.grid(column=0, row=1, columnspan=2)

        self.select_button = ttk.Button(self, text='Select person', command=self.select_callback)
        self.select_button.grid(column=0, row=2)

    def on_type_callback(self):
        self.search_results = self.nametowidget('.').tree.find(self.sv.get())

        # Delete all items
        for child in self.treeview_widget.get_children():
            self.treeview_widget.delete(child)

        # Set new items
        for res in self.search_results:
            self.treeview_widget.insert('', 0, values=(res, 'backend ID'))

    def select_callback(self):
        selected = self.treeview_widget.focus()
        selected = self.treeview_widget.item(selected)['values'][0]

        # Find corresponding ID and save in main app
        person_id = self.nametowidget('.').tree.individuals_lookup[selected]
        self.nametowidget('.').selected_individual = person_id

        # Update info and main frame
        self.nametowidget('.!infoframe').update_callback(person_id)


class InfoFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Markup info
        self.infostring = tk.StringVar()
        self.infostring.set('None')

        # Create widgets
        self.label = ttk.Label(self, textvariable=self.infostring)
        self.label.pack()

    def update_callback(self, person_id):
        individual = self.nametowidget('.').tree.individuals[person_id]
        self.infostring.set(individual)

class MainFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Create widgets
        self.__create_widgets()

    def __create_widgets(self):
        pass
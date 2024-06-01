#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.widgets.editabletreeview import EditableTreeview


class UnlockPDFAppUI:
    def __init__(self, master=None):
        # build ui
        toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)
        toplevel1.configure(height=200, width=200)
        self.frame_main = ttk.Frame(toplevel1, name="frame_main")
        self.frame_main.configure(height=200, padding=5, width=200)

        self.editabletreeview1 = EditableTreeview(self.frame_main)
        self.editabletreeview1.configure(selectmode="extended")
        editabletreeview1_cols = ['one', 'two', 'three', 'four']
        editabletreeview1_dcols = ['one', 'two', 'three', 'four']
        self.editabletreeview1.configure(
            columns=editabletreeview1_cols,
            displaycolumns=editabletreeview1_dcols)
        self.editabletreeview1.column(
            "one",
            anchor="w",
            stretch=True,
            width=200,
            minwidth=20)
        self.editabletreeview1.column(
            "two",
            anchor="w",
            stretch=True,
            width=200,
            minwidth=20)
        self.editabletreeview1.column(
            "three",
            anchor="w",
            stretch=True,
            width=200,
            minwidth=20)
        self.editabletreeview1.column(
            "four",
            anchor="w",
            stretch=True,
            width=200,
            minwidth=20)
        self.editabletreeview1.heading("one", anchor="w", text='File Name')
        self.editabletreeview1.heading("two", anchor="w", text='Size')
        self.editabletreeview1.heading("three", anchor="w", text='Pages')
        self.editabletreeview1.heading("four", anchor="w", text='Password')
        self.editabletreeview1.grid(column=1, row=2, sticky="nsew")

        self.frame_buttons = ttk.Frame(self.frame_main, name="frame_buttons")
        self.frame_buttons.configure(
            height=50, padding=20, relief="raised", width=200)
        self.btn_add_files = ttk.Button(
            self.frame_buttons, name="btn_add_files")
        self.btn_add_files.configure(
            compound="top",
            state="normal",
            text='Add Files...')
        self.btn_add_files.grid(column=1, row=1)
        self.btn_add_files.configure(command=self.on_add_files_button_clicked)
        self.btn_clear_table = ttk.Button(
            self.frame_buttons, name="btn_clear_table")
        self.btn_clear_table.configure(
            compound="top",
            cursor="arrow",
            default="active",
            state="normal",
            text='Clear Table')
        self.btn_clear_table.grid(column=2, padx="0 10", row=1)
        self.btn_clear_table.configure(
            command=self.on_clear_table_button_clicked)
        self.frame_buttons.grid(column=1, row=1, sticky="nsew")
        self.frame_buttons.grid_propagate(0)
        self.frame_buttons.grid_anchor("w")
        self.frame_main.grid(column=1, row=2, sticky="nsew")

        # Main widget
        self.mainwindow = toplevel1

    def run(self):
        self.mainwindow.mainloop()

    def on_add_files_button_clicked(self):
        pass

    def on_clear_table_button_clicked(self):
        pass


if __name__ == "__main__":
    app = UnlockPDFAppUI()
    app.editabletreeview1.column('#0', width=50)
    app.editabletreeview1.heading("#0", text="Item")
    app.editabletreeview1.insert('', 'end', values=('file1', '100', '10', 'password'))
    app.run()

#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
import pdf_unlockui as baseui


class unlock(baseui.unlockUI):
    def __init__(self, master=None):
        super().__init__(master)


if __name__ == "__main__":
    app = unlock()
    app.run()

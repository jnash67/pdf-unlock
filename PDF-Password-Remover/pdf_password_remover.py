import tkinter as tk
import tkinter.ttk as ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk
# from tooltip import create_tooltip # Moved to app_ui
# from tooltip_if_locked import create_tooltip_if_locked # Moved to app_ui
# import fitz  # PyMuPDF # Moved to relevant modules
from tkinter import messagebox
import sys
import os
# from pathlib import Path # Moved to app_file_operations
from brute_force_dialog import BruteForceDialog
import app_ui
import app_file_operations
import app_pdf_processing



class PDFPasswordRemoverApp(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        # images
        self.unlock_all_image = None
        self.unlock_selected_image = None
        self.pdf_image = None
        self.lock_image = None
        self.clear_image = None
        self.remove_image = None
        self.brute_force_image = None # For a potential icon

        # frames
        self.radio_button_frame = None
        self.bottom_buttons_frame = None
        self.top_buttons_frame = None
        self.file_list_treeview = None

        # buttons, labels, and entries
        self.unlock_all_button = None
        self.unlock_selected_button = None
        self.remove_all_button = None
        self.remove_selected_button = None
        self.add_pdf_button = None
        self.brute_force_button = None
        self.select_dir_button = None
        self.new_file_ending_label = None
        self.new_file_ending_entry = None
        self.output_dir_entry = None
        self.custom_folder_radiobutton = None
        self.same_folder_radiobutton = None

        # self.master = master # master is already handled by super().__init__
        # self.pack() # It's better to pack the instance in __main__.py

        # Initialize Tkinter variables first
        self.output_folder = tk.StringVar(value="same")

        # Then other instance variables
        self.locked_status = {}  # Add a dictionary to store the locked status of each item
        self.passwords = {}  # Add a dictionary to store the actual passwords
        self.added_files = set()  # Add a set to store the paths of added files

        self.create_widgets()  # Create widgets that might use these variables

    def create_widgets(self):
        app_ui.create_images(self)
        app_ui.create_top_buttons(self)
        app_ui.create_bottom_right_buttons(self)
        app_ui.create_bottom_left_ui(self)
        app_ui.create_treeview(self)

    def drop(self, event):
        app_file_operations.drop(self, event)

    def get_pdf_files(self):
        app_file_operations.get_pdf_files(self)

    def is_pdf(self, file_path): # Keep as app method if preferred, or call static from module
        return app_file_operations.is_pdf(self, file_path)

    def add_file_to_list(self, file_path):
        app_file_operations.add_file_to_list(self, file_path)

    def remove_selected(self):
        app_file_operations.remove_selected(self)

    def update_selected_buttons_state(self, event):
        app_file_operations.update_selected_buttons_state(self, event)

    def remove_all(self):
        app_file_operations.remove_all(self)

    def unlock_selected_pdf(self):
        app_pdf_processing.unlock_selected_pdf(self)

    def unlock_all_pdf(self):
        app_pdf_processing.unlock_all_pdf(self)

    def unlock_pdf(self, items):
        app_pdf_processing.unlock_pdf(self, items)

    def on_file_list_click(self, event):
        app_file_operations.on_file_list_click(self, event)

    def select_directory(self):
        app_file_operations.select_directory(self)

    def show_brute_force_dialog_for_selected(self):
        app_pdf_processing.show_brute_force_dialog_for_selected(self)

    def handle_brute_force_success(self, item_id, password):
        app_pdf_processing.handle_brute_force_success(self, item_id, password)

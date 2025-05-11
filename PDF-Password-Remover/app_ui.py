import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from tkinterdnd2 import DND_FILES
from tooltip import create_tooltip
from tooltip_if_locked import create_tooltip_if_locked
from utils import resource_path, get_default_downloads_path
from pathlib import Path # For resolving Downloads/Home paths
import os


def create_images(app):
    image_size = 40, 40

    app.lock_image = Image.open(resource_path("icons/icons8-lock-48.png"))
    app.lock_image = app.lock_image.resize((15, 15))  # Resize the image
    app.lock_image = ImageTk.PhotoImage(app.lock_image)

    app.pdf_image = Image.open(resource_path("icons/icons8-pdf-64.png"))
    app.pdf_image = app.pdf_image.resize(image_size)  # Resize the image
    app.pdf_image = ImageTk.PhotoImage(app.pdf_image)

    app.clear_image = Image.open(
        resource_path("icons/icons8-remove-blue-circle-48.png"))
    app.clear_image = app.clear_image.resize(image_size)  # Resize the image
    app.clear_image = ImageTk.PhotoImage(app.clear_image)

    app.remove_image = Image.open(
        resource_path("icons/icons8-remove-blue-trashcan-48.png"))
    app.remove_image = app.remove_image.resize(image_size)  # Resize the image
    app.remove_image = ImageTk.PhotoImage(app.remove_image)

    app.unlock_selected_image = Image.open(resource_path("icons/icons8-unlock-64.png"))
    app.unlock_selected_image = app.unlock_selected_image.resize(image_size)  # Resize the image
    app.unlock_selected_image = ImageTk.PhotoImage(app.unlock_selected_image)

    app.unlock_all_image = Image.open(resource_path("icons/icons8-grand-master-key-48.png"))
    app.unlock_all_image = app.unlock_all_image.resize(image_size)  # Resize the image
    app.unlock_all_image = ImageTk.PhotoImage(app.unlock_all_image)
    
    try:
        app.brute_force_image = ImageTk.PhotoImage(Image.open(resource_path("icons/icons8-hacking-48.png")).resize(image_size))
    except FileNotFoundError:
        app.brute_force_image = None

def create_top_buttons(app):
    app.top_buttons_frame = tk.Frame(app)
    app.top_buttons_frame.grid(row=0, column=0, sticky='ew')

    app.add_pdf_button = tk.Button(app.top_buttons_frame, text="Add PDFs...", image=app.pdf_image,
                                    compound=tk.LEFT, command=app.get_pdf_files)
    app.add_pdf_button.pack(side="left", padx=5, pady=5)

    app.remove_selected_button = tk.Button(app.top_buttons_frame, text="Remove \nSelected ",
                                            image=app.clear_image,
                                            compound=tk.LEFT,
                                            command=app.remove_selected)
    app.remove_selected_button["state"] = "disabled"
    app.remove_selected_button.pack(side="left", padx=5, pady=5)

    app.remove_all_button = tk.Button(app.top_buttons_frame, text="Remove \nAll ", image=app.remove_image,
                                       compound=tk.LEFT, command=app.remove_all)
    app.remove_all_button.pack(side="left", padx=5, pady=5)

    app.brute_force_button = tk.Button(app.top_buttons_frame, text="Brute-force \nSelected",
                                        image=app.brute_force_image if app.brute_force_image else None,
                                        compound=tk.LEFT,
                                        command=app.show_brute_force_dialog_for_selected)
    app.brute_force_button["state"] = "disabled"
    app.brute_force_button.pack(side="left", padx=5, pady=5)
    create_tooltip(app.brute_force_button, "Attempt to find password for the selected locked PDF using brute-force.")

def create_bottom_right_buttons(app):
    app.bottom_buttons_frame = tk.Frame(app)
    app.bottom_buttons_frame.grid(row=2, column=0, sticky='e')

    app.unlock_selected_button = ttk.Button(app.bottom_buttons_frame, text="Unlock \nSelected ",
                                             image=app.unlock_selected_image,
                                             compound=tk.LEFT,
                                             command=app.unlock_selected_pdf)
    app.unlock_selected_button["state"] = "disabled"
    app.unlock_selected_button.pack(side="left", padx=5, pady=5)

    app.unlock_all_button = ttk.Button(app.bottom_buttons_frame, text="Unlock \nAll ",
                                        image=app.unlock_all_image,
                                        compound=tk.LEFT,
                                        command=app.unlock_all_pdf)
    app.unlock_all_button.pack(side="left", padx=5, pady=5)

def create_bottom_left_ui(app):
    app.radio_button_frame = tk.Frame(app)
    app.radio_button_frame.grid(row=2, column=0, sticky='w')

    app.same_folder_radiobutton = tk.Radiobutton(app.radio_button_frame, text="Same folder",
                                                  variable=app.output_folder, value="same", padx=5)
    app.same_folder_radiobutton.grid(row=0, column=0, sticky='w')

    app.custom_folder_radiobutton = tk.Radiobutton(app.radio_button_frame, text="Custom folder",
                                                    variable=app.output_folder, value="custom", padx=5)
    app.custom_folder_radiobutton.grid(row=1, column=0, sticky='w')

    app.output_dir_entry = tk.Entry(app.radio_button_frame, width=30)
    app.output_dir_entry.grid(row=1, column=1, sticky='w')
    app.output_dir_entry.insert(0, get_default_downloads_path())

    app.select_dir_button = ttk.Button(app.radio_button_frame, text="Select directory",
                                        command=app.select_directory)
    app.select_dir_button.grid(row=1, column=2, sticky='w', padx=(7, 0))

    app.new_file_ending_label = tk.Label(app.radio_button_frame, text="New Filename Ending:")
    app.new_file_ending_label.grid(row=2, column=0, sticky='w', padx=(5, 5), pady=(0, 5))
    create_tooltip(app.new_file_ending_label, "If blank then old file will be overwritten")

    app.new_file_ending_entry = tk.Entry(app.radio_button_frame)
    app.new_file_ending_entry.grid(row=2, column=1, sticky='w', pady=(0, 5))
    app.new_file_ending_entry.insert(0, "_NoPW")
    create_tooltip(app.new_file_ending_entry, "If blank then old file will be overwritten")

    app.radio_button_frame.grid_columnconfigure(1, weight=1)

def create_treeview(app):
    app.file_list_treeview = ttk.Treeview(app)
    app.file_list_treeview["columns"] = ("File Name", "Path", "Size", "Pages", "Password", "Status")
    app.file_list_treeview.column("#0", width=40, anchor="w")
    app.file_list_treeview.column("File Name", width=200, anchor="w")
    app.file_list_treeview.column("Path", width=200, anchor="w")
    app.file_list_treeview.column("Size", width=40, anchor="w")
    app.file_list_treeview.column("Pages", width=40, anchor="w")
    app.file_list_treeview.column("Password", width=60, anchor="w")
    app.file_list_treeview.column("Status", width=100, anchor="w")
    app.file_list_treeview.heading("#0", text=" Item", anchor="w")
    app.file_list_treeview.heading("File Name", text=" File name", anchor="w")
    app.file_list_treeview.heading("Path", text=" Path", anchor="w")
    app.file_list_treeview.heading("Size", text=" Size", anchor="w")
    app.file_list_treeview.heading("Pages", text=" Pages", anchor="w")
    app.file_list_treeview.heading("Password", text=" Password", anchor="w")
    app.file_list_treeview.heading("Status", text=" Status", anchor="w")
    app.file_list_treeview.grid(row=1, column=0, sticky='nsew')

    app.grid_rowconfigure(0, weight=0)
    app.grid_rowconfigure(1, weight=1)
    app.grid_columnconfigure(0, weight=1)

    app.file_list_treeview.bind("<1>", app.on_file_list_click)
    app.file_list_treeview.bind("<<TreeviewSelect>>", app.update_selected_buttons_state)
    create_tooltip_if_locked(app.file_list_treeview, "Click on lock to enter password", app.locked_status)

    app.file_list_treeview.drop_target_register(DND_FILES)
    app.file_list_treeview.dnd_bind('<<Drop>>', app.drop)
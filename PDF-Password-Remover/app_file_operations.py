import os
import tkinter as tk # For tk.splitlist in drop
from tkinter import filedialog, simpledialog
from pathlib import Path
import fitz  # PyMuPDF
from utils import get_default_downloads_path # Import the helper


def drop(app, event):
    files = app.master.tk.splitlist(event.data)
    for filename in files:
        filename = filename.strip('{}')
        if os.path.isfile(filename) and filename.endswith('.pdf'):
            app.add_file_to_list(filename)

def get_pdf_files(app):
    downloads_path = get_default_downloads_path()

    pdf_file_paths = filedialog.askopenfilenames(initialdir=downloads_path, filetypes=[("PDF files", "*.pdf")])
    for pdf_file_path in pdf_file_paths:
        if is_pdf(app, pdf_file_path): # Call as static or app method
            app.add_file_to_list(pdf_file_path)

def is_pdf(app, file_path): # app parameter kept for consistency, though not used
    _, ext = os.path.splitext(file_path)
    return ext.lower() == '.pdf'

def add_file_to_list(app, file_path):
    if file_path in app.added_files:
        return
    app.added_files.add(file_path)
    
    file_name = os.path.basename(file_path)
    file_size = f"{os.path.getsize(file_path) / 1024:.2f} KB"
    doc = None
    try:
        doc = fitz.open(file_path)
        is_encrypted = doc.is_encrypted
        pages_text = "##"
        status_text = "Locked"
        image_to_use = app.lock_image

        if not is_encrypted:
            pages_text = doc.page_count
            status_text = "Unlocked"
            image_to_use = "" 

        item_id = app.file_list_treeview.insert("", "end",
                                                 text=f"  {len(app.file_list_treeview.get_children()) + 1}",
                                                 image=image_to_use,
                                                 values=(file_name, file_path, file_size, pages_text, "", status_text))
        app.locked_status[item_id] = is_encrypted

    except Exception as e:
        print(f"Error opening/reading PDF {file_path} with PyMuPDF: {e}")
        item_id = app.file_list_treeview.insert("", "end", text=f"  {len(app.file_list_treeview.get_children()) + 1}",
                                                 values=(file_name, file_path, file_size, "ERR", "", "Error"))
        app.locked_status[item_id] = False
    finally:
        if doc:
            doc.close()

def remove_selected(app):
    selected_items = app.file_list_treeview.selection()
    for item in selected_items:
        file_path_in_tree = app.file_list_treeview.item(item)["values"][1]
        if file_path_in_tree in app.added_files:
            app.added_files.remove(file_path_in_tree)            
        app.file_list_treeview.delete(item)

def update_selected_buttons_state(app, event):
    if app.file_list_treeview.selection():
        selected_items = app.file_list_treeview.selection()
        app.remove_selected_button["state"] = "normal"
        app.unlock_selected_button["state"] = "normal"

        if len(selected_items) == 1 and app.locked_status.get(selected_items[0], False):
            app.brute_force_button["state"] = "normal"
        else:
            app.brute_force_button["state"] = "disabled"
    else:
        app.remove_selected_button["state"] = "disabled"
        app.unlock_selected_button["state"] = "disabled"
        app.brute_force_button["state"] = "disabled"

def remove_all(app):
    app.added_files.clear()
    for item in app.file_list_treeview.get_children():
        app.file_list_treeview.delete(item)

def select_directory(app):
    initial_dir = get_default_downloads_path()
    selected_directory = filedialog.askdirectory(initialdir=initial_dir)
    if selected_directory:
        selected_directory = os.path.normpath(selected_directory)
        app.output_dir_entry.delete(0, "end")
        app.output_dir_entry.insert(0, selected_directory)

def on_file_list_click(app, event):
    item_id = app.file_list_treeview.identify_row(event.y)
    column = app.file_list_treeview.identify_column(event.x)

    if column == "#0" and app.locked_status.get(item_id, False):
        password = app.passwords.get(item_id, "")
        new_password = simpledialog.askstring("Password", "Enter the password:", initialvalue=password, show="*")
        if new_password is not None and new_password != "":
            app.passwords[item_id] = new_password
            app.file_list_treeview.set(item_id, "Password", "****")
        elif new_password == "": # Explicitly cleared
            app.file_list_treeview.set(item_id, "Password", "")
            if item_id in app.passwords:
                del app.passwords[item_id]
    # Standard selection behavior is handled by Treeview itself if not a special click
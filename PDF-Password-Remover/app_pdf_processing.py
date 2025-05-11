import os
import fitz  # PyMuPDF
from tkinter import messagebox
from brute_force_dialog import BruteForceDialog


def unlock_selected_pdf(app):
    items = app.file_list_treeview.selection()
    unlock_pdf(app, items)

def unlock_all_pdf(app):
    items = app.file_list_treeview.get_children()
    unlock_pdf(app, items)

def unlock_pdf(app, items):
    for item in items:
        pdf_file_path = app.file_list_treeview.item(item)["values"][1]
        password = app.passwords.get(item, "")
        is_locked_in_tree = app.locked_status.get(item, False)

        if is_locked_in_tree and not password:
            print(f"Password required for {os.path.basename(pdf_file_path)} but not provided. Skipping.")
            app.file_list_treeview.set(item, "Status", "Password Missing")
            continue

        doc = None
        try:
            doc = fitz.open(pdf_file_path)
            if doc.is_encrypted:
                if not is_locked_in_tree:
                    print(f"Warning: File {os.path.basename(pdf_file_path)} is encrypted but not marked as locked in UI. Skipping.")
                    app.file_list_treeview.set(item, "Status", "Encrypted (UI Mismatch)")
                    if doc: doc.close()
                    continue
                if not doc.authenticate(password):
                    print(f"Incorrect password for {os.path.basename(pdf_file_path)} or decryption failed.")
                    app.file_list_treeview.set(item, "Status", "Decryption Failed")
                    if doc: doc.close()
                    continue
            
            original_dir = os.path.dirname(pdf_file_path)
            original_filename = os.path.basename(pdf_file_path)
            name_part, ext_part = os.path.splitext(original_filename)
            
            ending = app.new_file_ending_entry.get()
            new_filename_part = f"{name_part}{ending}" if ending else name_part
            new_filename = f"{new_filename_part}{ext_part}"

            if app.output_folder.get() == "same":
                output_dir = original_dir
            else:
                output_dir = app.output_dir_entry.get()
                if not os.path.isdir(output_dir):
                    print(f"Custom output directory '{output_dir}' does not exist. Skipping {os.path.basename(pdf_file_path)}.")
                    app.file_list_treeview.set(item, "Status", "Output Dir Invalid")
                    if doc: doc.close()
                    continue
            
            new_file_path = os.path.join(output_dir, new_filename)

            doc.save(new_file_path, garbage=4, deflate=True)
            actual_pages = doc.page_count

            print(f"Successfully processed and saved: {new_file_path}")
            app.file_list_treeview.set(item, "File Name", new_filename)
            app.file_list_treeview.set(item, "Path", new_file_path)
            app.file_list_treeview.set(item, "Password", "")
            app.file_list_treeview.set(item, "Status", "Unlocked")
            app.file_list_treeview.item(item, image="")
            if item in app.passwords: del app.passwords[item]
            app.locked_status[item] = False
            app.file_list_treeview.set(item, "Pages", actual_pages)

        except Exception as e:
            print(f"An error occurred while processing {os.path.basename(pdf_file_path)} with PyMuPDF: {e}")
            app.file_list_treeview.set(item, "Status", f"Error: {str(e)[:30]}")
        finally:
            if doc:
                doc.close()

def show_brute_force_dialog_for_selected(app):
    selected_items = app.file_list_treeview.selection()
    if len(selected_items) == 1:
        item_id = selected_items[0]
        if app.locked_status.get(item_id, False):
            pdf_file_path = app.file_list_treeview.item(item_id)["values"][1]
            BruteForceDialog(app.master, app, item_id, pdf_file_path)
        else:
            messagebox.showinfo("Info", "Selected PDF is not locked.", parent=app)
    else:
        messagebox.showinfo("Info", "Please select exactly one locked PDF to brute-force.", parent=app)

def handle_brute_force_success(app, item_id, password):
    app.passwords[item_id] = password
    app.file_list_treeview.set(item_id, "Password", "****")
    messagebox.showinfo("Success", f"Password found and set for: {os.path.basename(app.file_list_treeview.item(item_id)['values'][1])}", parent=app)
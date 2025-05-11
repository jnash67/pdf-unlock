import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import os
import threading
import itertools
import string
import fitz  # PyMuPDF
from tooltip import create_tooltip


def run_brute_force_pdf_attempt(pdf_path, char_options, min_length, max_length, dialog, cancel_event, item_id):
    """
    Attempts to find the password for a PDF file using brute-force.

    Args:
        pdf_path (str): The path to the PDF file.
        char_options (dict): A dictionary with boolean values for character sets to use.
        min_length (int): The minimum password length to try.
        max_length (int): The maximum password length to try.
        dialog (BruteForceDialog): The dialog instance to update with progress and results.
        cancel_event (threading.Event): An event to signal cancellation.
        item_id (str): The ID of the item in the main application's list.
    """
    charset = ""
    if char_options["uppercase"]: charset += string.ascii_uppercase
    if char_options["lowercase"]: charset += string.ascii_lowercase
    if char_options["digits"]:    charset += string.digits
    if char_options["special"]:   charset += string.punctuation
    if char_options["space"]:     charset += ' '

    if not charset:
        dialog.after(0, lambda: dialog.on_failure("No character types selected."))
        return

    total_attempts = 0
    for length in range(min_length, max_length + 1):
        total_attempts += len(charset) ** length
    
    tried_attempts = 0
    found = False

    for password_length in range(min_length, max_length + 1):
        if found or cancel_event.is_set(): break
        for guess_tuple in itertools.product(charset, repeat=password_length):
            if cancel_event.is_set():
                dialog.after(0, lambda: dialog.on_failure("Brute force cancelled."))
                return

            guess = ''.join(guess_tuple)
            tried_attempts += 1

            if tried_attempts % 200 == 0 or tried_attempts == total_attempts: # Update progress less frequently
                progress_val = tried_attempts / total_attempts if total_attempts > 0 else 0
                status_txt = f"Trying: {guess} ({tried_attempts}/{total_attempts})"
                # Use dialog.after for thread-safe UI updates
                dialog.after(0, lambda p=progress_val, s=status_txt: dialog.update_progress(p, s))

            doc = None
            try:
                doc = fitz.open(pdf_path)
                if doc.authenticate(guess): # Returns > 0 on success
                    dialog.after(0, lambda g=guess: dialog.on_success(g))
                    found = True
                    break
            except Exception:
                # For brute-force, we usually want to continue unless it's a critical file error.
                # fitz.authenticate handles incorrect passwords by returning 0.
                # If an exception occurs here, it might be a more severe issue.
                # For simplicity, we'll log it and let the dialog decide if it's fatal.
                pass # Continue trying
            finally:
                if doc:
                    doc.close()
        if found: break
    
    if not found and not cancel_event.is_set():
        dialog.after(0, lambda: dialog.on_failure("Password not found with given criteria."))


class BruteForceDialog(tk.Toplevel):
    def __init__(self, master, app_instance, item_id, pdf_path):
        super().__init__(master)
        self.app_instance = app_instance
        self.item_id = item_id
        self.pdf_path = pdf_path
        self.brute_force_thread = None
        self.cancel_event = threading.Event()

        self.title(f"Brute Force: {os.path.basename(pdf_path)}")
        self.geometry("500x380") # Adjusted for new layout
        self.transient(master)
        self.grab_set()

        self.char_options = {
            "uppercase": tk.BooleanVar(value=True), "lowercase": tk.BooleanVar(value=True),
            "digits": tk.BooleanVar(value=True), "special": tk.BooleanVar(value=False),
            "space": tk.BooleanVar(value=False),
            "all_chars": tk.BooleanVar(value=False) # New "All" option
        }
        self.individual_char_checkbox_widgets = {} # To store checkbox widgets for enable/disable

        bf_frame = ttk.LabelFrame(self, text="Brute Force Options")
        bf_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Configure grid columns for the main brute force options frame
        bf_frame.grid_columnconfigure(0, weight=1) # Character options take available space
        bf_frame.grid_columnconfigure(1, weight=0) # Length options fixed width

        # --- Character Options Frame (Left) ---
        char_options_frame = ttk.Frame(bf_frame)
        char_options_frame.grid(row=0, column=0, sticky="nsew", pady=(0,5))

        # "All Characters" option
        all_cb = tk.Checkbutton(char_options_frame, text="All Character Types", variable=self.char_options["all_chars"], command=self.toggle_all_chars_option)
        all_cb.pack(anchor="w", padx=5, pady=(2,5))

        # Character set options in a single column with descriptive labels
        self.individual_char_checkbox_widgets["uppercase"] = tk.Checkbutton(char_options_frame, text="Uppercase (A-Z)", variable=self.char_options["uppercase"])
        self.individual_char_checkbox_widgets["uppercase"].pack(anchor="w", padx=5, pady=2)
        self.individual_char_checkbox_widgets["lowercase"] = tk.Checkbutton(char_options_frame, text="Lowercase (a-z)", variable=self.char_options["lowercase"])
        self.individual_char_checkbox_widgets["lowercase"].pack(anchor="w", padx=5, pady=2)
        self.individual_char_checkbox_widgets["digits"] = tk.Checkbutton(char_options_frame, text="Digits (0-9)", variable=self.char_options["digits"])
        self.individual_char_checkbox_widgets["digits"].pack(anchor="w", padx=5, pady=2)
        
        special_chars_short_text = string.punctuation[:3] + "..." # e.g., "!@#..."
        special_cb = tk.Checkbutton(char_options_frame, text=f"Special ({special_chars_short_text})", variable=self.char_options["special"])
        special_cb.pack(anchor="w", padx=5, pady=2)
        create_tooltip(special_cb, string.punctuation) # Tooltip with full list
        self.individual_char_checkbox_widgets["special"] = special_cb
        
        self.individual_char_checkbox_widgets["space"] = tk.Checkbutton(char_options_frame, text="Space ( )", variable=self.char_options["space"])
        self.individual_char_checkbox_widgets["space"].pack(anchor="w", padx=5, pady=2)

        # --- Length Options Frame (Right) ---
        length_options_frame = ttk.Frame(bf_frame)
        length_options_frame.grid(row=0, column=1, sticky="nsew", padx=(10,0), pady=(0,5))

        # Min/Max length options
        tk.Label(length_options_frame, text="Min Length:").pack(anchor="w", padx=5, pady=(25,2)) # Added top padding
        self.min_length_entry = ttk.Spinbox(length_options_frame, from_=1, to=16, width=5)
        self.min_length_entry.pack(anchor="w", padx=5, pady=2)
        self.min_length_entry.set("1")

        tk.Label(length_options_frame, text="Max Length:").pack(anchor="w", padx=5, pady=(10,2))
        self.max_length_entry = ttk.Spinbox(length_options_frame, from_=1, to=16, width=5)
        self.max_length_entry.pack(anchor="w", padx=5, pady=2)
        self.max_length_entry.set("6")

        # --- Progress, Status, and Buttons (Below character and length frames) ---
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(bf_frame, variable=self.progress_var, maximum=1.0, length=300)
        self.progress_bar.grid(row=1, column=0, columnspan=2, pady=(10,5), sticky="ew")

        self.status_label = ttk.Label(bf_frame, text="Ready.")
        self.status_label.grid(row=2, column=0, columnspan=2, pady=5, sticky="ew")

        self.start_button = ttk.Button(bf_frame, text="Start Brute Force", command=self.start_brute_force)
        self.start_button.grid(row=3, column=0, pady=(10,5), sticky="ew")
        self.cancel_button = ttk.Button(bf_frame, text="Cancel", command=self.cancel_brute_force, state=tk.DISABLED)
        self.cancel_button.grid(row=3, column=1, pady=(10,5), sticky="ew")
        
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.toggle_all_chars_option() # Set initial state of individual checkboxes

    def toggle_all_chars_option(self):
        use_all = self.char_options["all_chars"].get()
        for key, checkbox_widget in self.individual_char_checkbox_widgets.items():
            if use_all:
                checkbox_widget.config(state=tk.DISABLED)
                # self.char_options[key].set(True) # Optionally set underlying vars
            else:
                checkbox_widget.config(state=tk.NORMAL)
                # Here, you might want to restore previous states or set defaults
                # For now, they just become enabled with their current BooleanVar state.

    def start_brute_force(self):
        try:
            min_len = int(self.min_length_entry.get())
            max_len = int(self.max_length_entry.get())
            if not (1 <= min_len <= max_len <= 16): # Max length 16 is a sensible limit
                raise ValueError("Invalid length (Min 1, Max <= 16, Min <= Max).")
            selected_char_options = {k: v.get() for k, v in self.char_options.items()}

            if self.char_options["all_chars"].get():
                # If "All" is selected, ensure all individual types are considered true for the attempt
                options_for_attempt = {
                    "uppercase": True, "lowercase": True, "digits": True,
                    "special": True, "space": True
                }
            else:
                # Use the state of the individual checkboxes
                options_for_attempt = {k: v_var.get() for k, v_var in self.char_options.items()
                                       if k in self.individual_char_checkbox_widgets}
            if not any(options_for_attempt.values()): # Check if any character type is selected
                raise ValueError("Select at least one character type (or 'All Character Types').")
        except ValueError as e:
            messagebox.showerror("Input Error", str(e), parent=self)
            return

        self.start_button.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.NORMAL)
        self.status_label.config(text="Starting...")
        self.progress_var.set(0)
        self.cancel_event.clear()

        self.brute_force_thread = threading.Thread(
            target=run_brute_force_pdf_attempt, # Call the standalone function
            args=(self.pdf_path, options_for_attempt, min_len, max_len, self, self.cancel_event, self.item_id),
            daemon=True
        )
        self.brute_force_thread.start()

    def cancel_brute_force(self):
        if self.brute_force_thread and self.brute_force_thread.is_alive():
            self.cancel_event.set()
            self.status_label.config(text="Cancelling...")
        self.start_button.config(state=tk.NORMAL)
        self.cancel_button.config(state=tk.DISABLED)

    def update_progress(self, value, status_text):
        self.progress_var.set(value)
        self.status_label.config(text=status_text)

    def on_success(self, password):
        self.status_label.config(text=f"Success! Password: {password}")
        self.progress_var.set(1.0)
        self.app_instance.handle_brute_force_success(self.item_id, password) # Call method on main app
        self.start_button.config(state=tk.NORMAL)
        self.cancel_button.config(state=tk.DISABLED)
        messagebox.showinfo("Success", f"Password found: {password}", parent=self)
        self.destroy()

    def on_failure(self, message):
        self.status_label.config(text=message)
        self.start_button.config(state=tk.NORMAL)
        self.cancel_button.config(state=tk.DISABLED)
        if "Password not found" in message: # Only show messagebox for actual failure, not cancellation
            messagebox.showinfo("Result", message, parent=self)

    def on_close(self):
        self.cancel_brute_force()
        self.destroy()
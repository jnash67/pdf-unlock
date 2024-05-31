import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, simpledialog
from tkinterdnd2 import DND_FILES, TkinterDnD
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image, ImageTk
import os
from tooltip import create_tooltip
from tooltip_if_locked import create_tooltip_if_locked
import traceback


class PDFPasswordRemoverApp(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pdf_image = None
        self.lock_image = None
        self.clear_image = None
        self.remove_image = None

        self.radio_button_frame = None
        self.bottom_buttons_frame = None
        self.top_buttons_frame = None
        self.file_list_treeview = None

        self.master = master
        self.pack()

        # Define the locked_status attribute here
        self.locked_status = {}

        self.create_widgets()
        self.passwords = {}  # Add a dictionary to store the actual passwords
        self.added_files = set()  # Add a set to store the paths of added files

    def create_images(self):
        image_size = 40, 40
        self.lock_image = Image.open("icons8-lock-48.png")  # Replace with the path to your image
        self.lock_image = self.lock_image.resize((15, 15))  # Resize the image
        self.lock_image = ImageTk.PhotoImage(self.lock_image)

        self.pdf_image = Image.open("icons8-pdf-64.png")  # Replace with the path to your image
        self.pdf_image = self.pdf_image.resize(image_size)  # Resize the image
        self.pdf_image = ImageTk.PhotoImage(self.pdf_image)

        self.clear_image = Image.open("icons8-remove-blue-circle-48.png")  # Replace with the path to your image
        self.clear_image = self.clear_image.resize(image_size)  # Resize the image
        self.clear_image = ImageTk.PhotoImage(self.clear_image)

        self.remove_image = Image.open("icons8-remove-blue-trashcan-48.png")  # Replace with the path to your image
        self.remove_image = self.remove_image.resize(image_size)  # Resize the image
        self.remove_image = ImageTk.PhotoImage(self.remove_image)

        self.unlock_selected_image = Image.open("icons8-unlock-64.png")
        self.unlock_selected_image = self.unlock_selected_image.resize(image_size)  # Resize the image
        self.unlock_selected_image = ImageTk.PhotoImage(self.unlock_selected_image)

        self.unlock_all_image = Image.open("icons8-grand-master-key-48.png")
        self.unlock_all_image = self.unlock_all_image.resize(image_size)  # Resize the image
        self.unlock_all_image = ImageTk.PhotoImage(self.unlock_all_image)

    def create_top_buttons(self):

        # Create a new frame for the buttons
        self.top_buttons_frame = tk.Frame(self)
        self.top_buttons_frame.grid(row=0, column=0, sticky='ew')  # Place the frame in row 0

        self.add_pdf_button = tk.Button(self.top_buttons_frame, text="Add PDFs...", image=self.pdf_image,
                                        compound=tk.LEFT, command=self.get_pdf_files)
        self.add_pdf_button.pack(side="left", padx=5, pady=5)  # Add 10 pixels of padding on each side

        self.remove_selected_button = tk.Button(self.top_buttons_frame, text="Remove \nSelected ",
                                                image=self.clear_image,
                                                compound=tk.LEFT,
                                                command=self.remove_selected)
        self.remove_selected_button["state"] = "disabled"  # Disable the button by default
        self.remove_selected_button.pack(side="left", padx=5, pady=5)

        self.remove_all_button = tk.Button(self.top_buttons_frame, text="Remove \nAll ", image=self.remove_image,
                                           compound=tk.LEFT, command=self.remove_all)
        self.remove_all_button.pack(side="left", padx=5, pady=5)

    def create_bottom_buttons(self):
        # Create a new frame for the unlock buttons
        self.bottom_buttons_frame = tk.Frame(self)
        self.bottom_buttons_frame.grid(row=2, column=0, sticky='e')  # Place the frame in row 2, aligned to the right

        # Replace tk.Button with ttk.Button for the unlock_selected_button
        self.unlock_selected_button = ttk.Button(self.bottom_buttons_frame, text="Unlock \nSelected ",
                                                 image=self.unlock_selected_image,
                                                 compound=tk.LEFT,
                                                 command=self.unlock_selected_pdf)
        self.unlock_selected_button["state"] = "disabled"  # Disable the button by default
        self.unlock_selected_button.pack(side="left", padx=5, pady=5)

        # Replace tk.Button with ttk.Button for the unlock_all_button
        self.unlock_all_button = ttk.Button(self.bottom_buttons_frame, text="Unlock \nAll ",
                                            image=self.unlock_all_image,
                                            compound=tk.LEFT,
                                            command=self.unlock_all_pdf,
                                            )
        self.unlock_all_button.pack(side="left", padx=5, pady=5)


    def create_radio_buttons(self):
        # Create a new frame for the radio buttons
        self.radio_button_frame = tk.Frame(self)
        self.radio_button_frame.grid(row=2, column=0, sticky='w')  # Place the frame in row 2, aligned to the left

        self.output_var = tk.StringVar(value="same")

        # Move the radio buttons to the radio_button_frame and place them on top of each other
        self.same_folder_radiobutton = tk.Radiobutton(self.radio_button_frame, text="Same folder",
                                                      variable=self.output_var, value="same", padx=5)
        self.same_folder_radiobutton.grid(row=0, column=0, sticky='w')  # Place the button in row 0

        self.custom_folder_radiobutton = tk.Radiobutton(self.radio_button_frame, text="Custom folder",
                                                        variable=self.output_var, value="custom", padx=5)
        self.custom_folder_radiobutton.grid(row=1, column=0, sticky='w')  # Place the button in row 1

        # Create an Entry to display the selected directory and place it to the right of the custom_folder_radiobutton
        self.output_dir_entry = tk.Entry(self.radio_button_frame, width=30)
        self.output_dir_entry.grid(row=1, column=1,
                                   sticky='w')  # Place the Entry in row 1, to the right of the custom_folder_radiobutton
        self.output_dir_entry.insert(0, os.getcwd())  # Set the initial value to the current directory

        # Create a Button that opens a directory selection dialog and place it to the right of the output_dir_entry
        self.select_dir_button = tk.Button(self.radio_button_frame, text="Select directory",
                                           command=self.select_directory)
        self.select_dir_button.grid(row=1, column=2,
                                    sticky='w',
                                    padx=(7, 0))  # Place the button in row 1, to the right of the output_dir_entry
        self.new_file_ending_label = tk.Label(self.radio_button_frame, text="New Filename Ending:")
        self.new_file_ending_label.grid(row=2, column=0, sticky='w', padx=(5, 5), pady=(0, 5))
        create_tooltip(self.new_file_ending_label, "If blank then old file will be overwritten")

        self.new_file_ending_entry = tk.Entry(self.radio_button_frame)
        self.new_file_ending_entry.grid(row=2, column=1, sticky='w', pady=(0, 5))  # Place the Entry in row 2, to the right of the custom_folder_radiobutton
        self.new_file_ending_entry.insert(0, "_NoPW")  # Set the initial value to "_NoPW"
        create_tooltip(self.new_file_ending_entry, "If blank then old file will be overwritten")

    def create_treeview(self):
        # Create a new Treeview for the file list
        self.file_list_treeview = ttk.Treeview(self)
        self.file_list_treeview["columns"] = ("File Name", "Size", "Pages", "Password", "Status")
        self.file_list_treeview.column("#0", width=60, anchor="w")
        self.file_list_treeview.column("File Name", width=200, anchor="w")
        self.file_list_treeview.column("Size", width=100, anchor="w")
        self.file_list_treeview.column("Pages", width=100, anchor="w")
        self.file_list_treeview.column("Password", width=100, anchor="w")
        self.file_list_treeview.column("Status", width=100, anchor="w")
        self.file_list_treeview.heading("#0", text=" Item", anchor="w")
        self.file_list_treeview.heading("File Name", text=" File name", anchor="w")
        self.file_list_treeview.heading("Size", text=" Size", anchor="w")
        self.file_list_treeview.heading("Pages", text=" Pages", anchor="w")
        self.file_list_treeview.heading("Password", text=" Password", anchor="w")
        self.file_list_treeview.heading("Status", text=" Status", anchor="w")
        self.file_list_treeview.grid(row=1, column=0, sticky='nsew')  # Use grid instead of pack

        self.grid_rowconfigure(0, weight=0)  # Make the top frame non-expandable
        self.grid_rowconfigure(1, weight=1)  # Make the row with the table expandable
        self.grid_columnconfigure(0, weight=1)  # Make the column expandable

        # Bind the click event to the on_click function
        # self.file_list.bind("<ButtonRelease-1>", self.show_password_entry)
        # self.file_list.bind("<1>", self.show_password_entry)
        self.file_list_treeview.bind("<1>", self.on_file_list_click)
        self.file_list_treeview.bind("<<TreeviewSelect>>", self.update_selected_buttons_state)
        create_tooltip_if_locked(self.file_list_treeview, "Click on lock to enter password", self.locked_status)
        # Bind the <<Drop>> event to the Treeview widget
        self.file_list_treeview.drop_target_register(DND_FILES)
        self.file_list_treeview.dnd_bind('<<Drop>>', self.drop)


    def create_widgets(self):
        self.create_images()
        self.create_top_buttons()
        self.create_bottom_buttons()
        self.create_radio_buttons()
        self.create_treeview()

    def drop(self, event):
        print("Drop event triggered")
        print("Dropped file path:", event.data)
        # Get the path of the dropped file
        dropped_file_path = event.data.strip('{}')  # Strip curly braces if present
        if os.path.isfile(dropped_file_path) and dropped_file_path.endswith('.pdf'):
            self.add_file_to_list(dropped_file_path)

    def get_pdf_files(self):
        pdf_file_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        for pdf_file_path in pdf_file_paths:
            if self.is_pdf(pdf_file_path):
                self.add_file_to_list(pdf_file_path)

    @staticmethod
    def is_pdf(file_path):
        _, ext = os.path.splitext(file_path)
        return ext.lower() == '.pdf'

    def add_file_to_list(self, file_path):
        # Check if the file has already been added
        if file_path in self.added_files:
            return
        # Add the file path to the set of added files
        self.added_files.add(file_path)
        # Get the item number
        item_number = len(self.file_list_treeview.get_children()) + 1
        # Get the file size in KB
        file_size = os.path.getsize(file_path) / 1024
        # Get the file name
        file_name = os.path.basename(file_path)
        # Get the number of pages in the PDF
        pdf_reader = PdfReader(file_path)
        if pdf_reader.is_encrypted:
            # Add file to the list
            item_id = self.file_list_treeview.insert("", "end", text=str(item_number),
                                                     image=self.lock_image,
                                                     values=(
                                                         file_name, f"{file_size:.0f} KB", "##", "", "Locked"))
            # Add the item ID to the locked_status dictionary with the value True
            self.locked_status[item_id] = True
        else:
            num_pages = len(pdf_reader.pages)
            # Add file to the list
            item_id = self.file_list_treeview.insert("", "end", text="  " + str(item_number),
                                                     values=(
                                                         file_name, f"{file_size:.0f} KB", num_pages, "",
                                                         "Unlocked"))
            # Add the item ID to the locked_status dictionary with the value False
            self.locked_status[item_id] = False

    def remove_selected(self):
        # Get the selected items
        selected_items = self.file_list_treeview.selection()
        # Remove the selected items
        for item in selected_items:
            file_path = self.file_list_treeview.item(item)["values"][0]
            self.added_files.discard(file_path)  # Remove the file path from the set
            self.file_list_treeview.delete(item)

    def update_selected_buttons_state(self, event):
        # If any items are selected, enable the buttons; otherwise, disable them
        if self.file_list_treeview.selection():
            self.remove_selected_button["state"] = "normal"
            self.unlock_selected_button["state"] = "normal"
        else:
            self.remove_selected_button["state"] = "disabled"
            self.unlock_selected_button["state"] = "disabled"

    def remove_all(self):
        # Clear the set of added files
        self.added_files.clear()
        # Remove all items from the file_list_treeview
        for item in self.file_list_treeview.get_children():
            self.file_list_treeview.delete(item)

    def unlock_selected_pdf(self):
        # Get the selected item from the Treeview
        items = self.file_list_treeview.selection()
        self.unlock_pdf(items)

    def unlock_all_pdf(self):
        # Get all items from the Treeview
        items = self.file_list_treeview.get_children()
        self.unlock_pdf(items)

    def unlock_pdf(self, items):
        for item in items:
            if self.locked_status.get(item, False):
                pdf_file_path = self.file_list_treeview.item(item)["values"][0]
                password = self.passwords.get(item, "")
                pdf_reader = PdfReader(pdf_file_path)
                try:
                    if password == "":
                        print(f"Please specify a password first for file: {pdf_file_path}")
                        continue
                    pdf_reader.decrypt(password)
                    pdf_writer = PdfWriter()
                    for page_num in range(len(pdf_reader.pages)):
                        pdf_writer.add_page(pdf_reader.pages[page_num])

                    dir_name = os.path.dirname(pdf_file_path)
                    base_name = os.path.basename(pdf_file_path)
                    file_name, file_extension = os.path.splitext(base_name)
                    new_file_ending = self.new_file_ending_entry.get()
                    new_file_name = file_name + new_file_ending + file_extension if new_file_ending else file_name + file_extension

                    if self.output_var.get() == "same":
                        new_file_path = os.path.join(dir_name, new_file_name)
                    else:
                        new_file_path = os.path.join(self.output_dir_entry.get(), new_file_name)

                    with open(new_file_path, "wb") as output_pdf:
                        pdf_writer.write(output_pdf)

                    self.file_list_treeview.set(item, "Password", "")
                    self.file_list_treeview.set(item, "Status", "Unlocked")
                    self.file_list_treeview.item(item, image="")
                    del self.passwords[item]
                    self.locked_status[item] = False
                except Exception as e:
                    print(f"Incorrect password for file: {pdf_file_path}")

    def on_file_list_click(self, event):
        # Get the item ID of the item clicked and the column clicked
        item_id = self.file_list_treeview.identify_row(event.y)
        column = self.file_list_treeview.identify_column(event.x)

        # Only open the password entry dialog if the clicked cell is in the "#0" column and the item is locked
        if column == "#0" and self.locked_status.get(item_id, False):
            # Get the password from the passwords dictionary
            password = self.passwords.get(item_id, "")

            # Open a password entry dialog with the password as the initial value
            new_password = simpledialog.askstring("Password", "Enter the password:", initialvalue=password, show="*")

            # If the user entered a password, save it in the passwords dictionary
            if new_password is not None and new_password != "":
                self.passwords[item_id] = new_password
                self.file_list_treeview.set(item_id, "Password", "****")
            else:
                if new_password == "":
                    self.file_list_treeview.set(item_id, "Password", "")
                    if item_id in self.passwords:
                        del self.passwords[item_id]
        else:
            # Check if the item is already selected
            if item_id in self.file_list_treeview.selection():
                # If it is, unselect it
                self.file_list_treeview.selection_remove(item_id)
                # Remove the 'selected' tag
                self.file_list_treeview.item(item_id, tags=())
            else:
                # If it's not, select it
                self.file_list_treeview.selection_add(item_id)
                # Add the 'selected' tag
                self.file_list_treeview.item(item_id, tags=('selected',))

    def select_directory(self):
        # Open a directory selection dialog and set the selected directory in the Entry
        selected_directory = filedialog.askdirectory()
        self.output_dir_entry.delete(0, "end")  # Delete the current value
        self.output_dir_entry.insert(0, selected_directory)  # Insert the selected directory


# Bind the click event to the on_click function
root = TkinterDnD.Tk()
root.title("PDF Password Remover")
root.geometry("750x450")
root.minsize(700, 200)  # Set the minimum window size to 500x300
app = PDFPasswordRemoverApp(master=root)
app.pack(fill='both', expand=True)  # Make the app expandable
app.mainloop()

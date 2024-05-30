import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from pygubu.widgets.editabletreeview import EditableTreeview
from tkinterdnd2 import DND_FILES, TkinterDnD
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image, ImageTk
import os
from tooltip import create_tooltip
import traceback


class PDFPasswordRemoverApp(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.radio_button_frame = None
        self.bottom_buttons_frame = None
        self.top_buttons_frame = None
        self.file_list_editabletreeview = None
        self.lock_image = None
        self.master = master
        self.pack()
        self.create_widgets()
        self.passwords = {}  # Add a dictionary to store the actual passwords

    def create_images(self):
        self.lock_image = Image.open("icons8-lock-48.png")  # Replace with the path to your image
        self.lock_image = self.lock_image.resize((20, 20))  # Resize the image
        self.lock_image = ImageTk.PhotoImage(self.lock_image)

    def create_widgets(self):
        self.create_images()

        # Create a custom style
        style = ttk.Style()
        style.configure("RoundedButton.TButton",
                        borderwidth=1,
                        relief="solid",
                        foreground="red",  # Set the text color here
                        background="white",
                        font=("Helvetica", 12),
                        padding=10)

        # Create a new frame for the buttons
        self.top_buttons_frame = tk.Frame(self)
        self.top_buttons_frame.grid(row=0, column=0, sticky='ew')  # Place the frame in row 0

        # Create a new frame for the unlock buttons
        self.bottom_buttons_frame = tk.Frame(self)
        self.bottom_buttons_frame.grid(row=2, column=0, sticky='e')  # Place the frame in row 2, aligned to the right

        # Create a new frame for the radio buttons
        self.radio_button_frame = tk.Frame(self)
        self.radio_button_frame.grid(row=2, column=0, sticky='w')  # Place the frame in row 2, aligned to the left

        self.file_list_editabletreeview = EditableTreeview(self)
        self.file_list_editabletreeview["columns"] = ("File Name", "Size", "Pages", "Password", "Status")
        self.file_list_editabletreeview.column("#0", width=60, anchor="w")
        self.file_list_editabletreeview.column("File Name", width=200, anchor="w")
        self.file_list_editabletreeview.column("Size", width=100, anchor="w")
        self.file_list_editabletreeview.column("Pages", width=100, anchor="w")
        self.file_list_editabletreeview.column("Password", width=100, anchor="w")
        self.file_list_editabletreeview.column("Status", width=100, anchor="w")
        self.file_list_editabletreeview.heading("#0", text=" Item", anchor="w")
        self.file_list_editabletreeview.heading("File Name", text=" File name", anchor="w")
        self.file_list_editabletreeview.heading("Size", text=" Size", anchor="w")
        self.file_list_editabletreeview.heading("Pages", text=" Pages", anchor="w")
        self.file_list_editabletreeview.heading("Password", text=" Password", anchor="w")
        self.file_list_editabletreeview.heading("Status", text=" Status", anchor="w")
        self.file_list_editabletreeview.grid(row=1, column=0, sticky='nsew')  # Use grid instead of pack

        self.grid_rowconfigure(0, weight=0)  # Make the top frame non-expandable
        self.grid_rowconfigure(1, weight=1)  # Make the row with the table expandable
        self.grid_columnconfigure(0, weight=1)  # Make the column expandable

        # Bind the click event to the on_click function
        # self.file_list.bind("<ButtonRelease-1>", self.show_password_entry)
        #self.file_list.bind("<1>", self.show_password_entry)
        #self.file_list.bind("<1>", self.on_click)
        # Bind the double-click event to the on_double_click function
        self.file_list_editabletreeview.bind("<Double-1>", self.on_double_click)
        # Bind the <<TreeviewSelect>> event to the update_remove_selected_button_state function
        self.file_list_editabletreeview.bind("<<TreeviewSelect>>", self.update_selected_buttons_state)
        create_tooltip(self.file_list_editabletreeview, "This is a tooltip")

        # Move the select_button to the button_frame
        self.add_pdf_button = tk.Button(self.top_buttons_frame)
        self.add_pdf_button["text"] = "Add PDFs..."
        self.add_pdf_button["command"] = self.get_pdf_files
        self.add_pdf_button.pack(side="left", padx=5)  # Add 10 pixels of padding on each side

        self.output_var = tk.StringVar(value="same")

        # Move the radio buttons to the radio_button_frame and place them on top of each other
        self.same_folder_radiobutton = tk.Radiobutton(self.radio_button_frame, text="Same folder",
                                                      variable=self.output_var, value="same")
        self.same_folder_radiobutton.grid(row=0, column=0, sticky='w')  # Place the button in row 0

        self.custom_folder_radiobutton = tk.Radiobutton(self.radio_button_frame, text="Custom folder",
                                                        variable=self.output_var, value="custom")
        self.custom_folder_radiobutton.grid(row=1, column=0, sticky='w')  # Place the button in row 1

        # Create an Entry to display the selected directory and place it to the right of the custom_folder_radiobutton
        self.output_dir_entry = tk.Entry(self.radio_button_frame)
        self.output_dir_entry.grid(row=1, column=1,
                                   sticky='w')  # Place the Entry in row 1, to the right of the custom_folder_radiobutton
        self.output_dir_entry.insert(0, os.getcwd())  # Set the initial value to the current directory

        # Create a Button that opens a directory selection dialog and place it to the right of the output_dir_entry
        self.select_dir_button = tk.Button(self.radio_button_frame, text="Select directory",
                                           command=self.select_directory)
        self.select_dir_button.grid(row=1, column=2,
                                    sticky='w')  # Place the button in row 1, to the right of the output_dir_entry

        # Move the execute_button to the button_frame
        # Replace tk.Button with ttk.Button for the unlock_selected_button
        self.unlock_selected_button = ttk.Button(self.bottom_buttons_frame, text="Unlock Selected",
                                                 command=self.unlock_pdf, style="RoundedButton.TButton")
        self.unlock_selected_button["state"] = "disabled"  # Disable the button by default
        self.unlock_selected_button.pack(side="left", padx=5)

        # Replace tk.Button with ttk.Button for the unlock_all_button
        self.unlock_all_button = ttk.Button(self.bottom_buttons_frame, text="Unlock All", command=self.unlock_pdf,
                                            style="RoundedButton.TButton")
        self.unlock_all_button.pack(side="left", padx=5)

        self.remove_selected_button = tk.Button(self.top_buttons_frame, text="Remove Selected",
                                                command=self.remove_selected)
        self.remove_selected_button["state"] = "disabled"  # Disable the button by default
        self.remove_selected_button.pack(side="left", padx=5)

        self.remove_all_button = tk.Button(self.top_buttons_frame, text="Remove All", command=self.remove_all)
        self.remove_all_button.pack(side="left", padx=5)

        # Bind the <<Drop>> event to the Treeview widget
        self.file_list_editabletreeview.dnd_bind('<<Drop>>', self.drop)

    def show_tooltip(self, event):
        # Get the column of the cell under the mouse cursor
        column = self.file_list_editabletreeview.identify_column(event.x)
        # Get the row of the cell under the mouse cursor
        row = self.file_list_editabletreeview.identify_row(event.y)
        # If the row is not empty (i.e., the mouse is over an item)
        if row:
            # Get the status of the PDF
            status = self.file_list_editabletreeview.set(row, "Status")
            # If the column is the first one and the status is "Locked", show the tooltip
            if column == "#0" and status == "Locked":
                self.tooltip.show_tip("This is a tooltip")
            else:
                self.tooltip.hide_tip()

    def hide_tooltip(self, event):
        # Unbind the tooltip from the Treeview widget
        self.tooltip.unbind_widget(self.file_list_editabletreeview)

    def drop(self, event):
        # Get the path of the dropped file
        dropped_file_path = event.data
        if os.path.isfile(dropped_file_path) and dropped_file_path.endswith('.pdf'):
            self.add_file_to_list(dropped_file_path)

    def get_pdf_files(self):
        pdf_file_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        for pdf_file_path in pdf_file_paths:
            # Get the item number
            item_number = len(self.file_list_editabletreeview.get_children()) + 1
            # Get the file size in KB
            file_size = os.path.getsize(pdf_file_path) / 1024
            # Get the file name
            file_name = os.path.basename(pdf_file_path)
            # Get the number of pages in the PDF
            pdf_reader = PdfReader(pdf_file_path)
            if pdf_reader.is_encrypted:
                # Add file to the list
                self.file_list_editabletreeview.insert("", "end", text=str(item_number), image=self.lock_image,
                                                       values=(file_name, f"{file_size:.0f} KB", "##", "", "Locked"))
            else:
                num_pages = len(pdf_reader.pages)
                # Add file to the list
                self.file_list_editabletreeview.insert("", "end", text="  " + str(item_number),
                                                       values=(
                                                       file_name, f"{file_size:.0f} KB", num_pages, "", "Unlocked"))

    def remove_selected(self):
        # Get the selected items
        selected_items = self.file_list_editabletreeview.selection()
        # Remove the selected items
        for item in selected_items:
            self.file_list_editabletreeview.delete(item)

    def update_selected_buttons_state(self, event):
        # If any items are selected, enable the buttons; otherwise, disable them
        if self.file_list_editabletreeview.selection():
            self.remove_selected_button["state"] = "normal"
            self.unlock_selected_button["state"] = "normal"
        else:
            self.remove_selected_button["state"] = "disabled"
            self.unlock_selected_button["state"] = "disabled"

    def remove_all(self):
        # Remove all items from the file_list_editabletreeview
        for item in self.file_list_editabletreeview.get_children():
            self.file_list_editabletreeview.delete(item)

    def unlock_pdf(self):
        for item in self.file_list_editabletreeview.get_children():
            pdf_file_path = self.file_list_editabletreeview.item(item)["values"][0]
            # Get the password from the passwords dictionary
            password = self.passwords.get(item, "")
            pdf_reader = PdfReader(pdf_file_path)
            if pdf_reader.is_encrypted:
                try:
                    pdf_reader.decrypt(password)
                    pdf_writer = PdfWriter()
                    for page_num in range(len(pdf_reader.pages)):
                        pdf_writer.add_page(pdf_reader.pages[page_num])

                    # Get the directory of the original file
                    dir_name = os.path.dirname(pdf_file_path)
                    # Get the original file name
                    base_name = os.path.basename(pdf_file_path)
                    # Split the original file name into the name and the extension
                    file_name, file_extension = os.path.splitext(base_name)
                    # Append "NoPW" to the end of the file name, and then add the extension back
                    new_file_name = file_name + "_NoPW" + file_extension
                    # Join the directory and the new file name together to get the new file path
                    new_file_path = os.path.join(dir_name, new_file_name)

                    with open(new_file_path, "wb") as output_pdf:
                        pdf_writer.write(output_pdf)
                    print(f"PDF unlocked and saved as '{new_file_name}'")
                except Exception as e:  # Catch the exception
                    # print("An error occurred:")
                    # traceback.print_exc()  # Print the details of the exception
                    print("Incorrect password")

    # def on_click(self, event):
    #     # Get the item ID of the item clicked and the column clicked
    #     item_id = self.file_list.identify_row(event.y)
    #     column = self.file_list.identify_column(event.x)
    #
    #     # Only make the cell editable if it's in the "Password" column and the PDF is locked
    #     if column == "#4" and self.file_list.set(item_id, "Status") == "Locked":
    #         # Start editing the cell
    #         self.file_list.edit_cell(item_id, column)

    def on_double_click(self, event):
        # Get the item ID of the item clicked and the column clicked
        item_id = self.file_list_editabletreeview.identify_row(event.y)
        column = self.file_list_editabletreeview.identify_column(event.x)

        # Only make the cell editable if it's in the "Password" column and the PDF is locked
        if column == "#4" and self.file_list_editabletreeview.set(item_id, "Status") == "Locked":
            # Get the current value of the cell from the passwords dictionary
            current_value = self.passwords.get(item_id, "")
            # Create an Entry widget with the current value as the initial value and the show option set to "*"
            self.password_entry = tk.Entry(self, show="*")
            self.password_entry.insert(0, current_value)  # Set the initial value
            # Position the Entry over the cell
            self.password_entry.place(x=event.x, y=event.y, width=100)  # Set a fixed width

            # Create a Checkbutton that toggles the show option of the Entry
            self.show_password_var = tk.BooleanVar()
            self.show_password_checkbutton = tk.Checkbutton(self, text="Show password", variable=self.show_password_var,
                                                            command=self.toggle_show_password)
            self.show_password_checkbutton.place(x=event.x,
                                                 y=event.y + self.password_entry.winfo_reqheight())  # Position the Checkbutton below the Entry

            # When the Entry loses focus or the user hits Enter, save the data and destroy the Entry and the Checkbutton
            self.password_entry.bind("<FocusOut>", lambda e: self.save_data(item_id, column))
            self.password_entry.bind("<Return>", lambda e: self.save_data(item_id, column))

    def toggle_show_password(self):
        # If the Checkbutton is checked, show the password; otherwise, mask it
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    def save_data(self, item_id, column):
        # Get the data from the Entry
        data = self.password_entry.get()
        # Save the actual password in the passwords dictionary
        self.passwords[item_id] = data
        # Set the masked password in the Treeview
        self.file_list_editabletreeview.set(item_id, column, "*" * len(data))
        # Destroy the Entry and the Checkbutton
        self.password_entry.destroy()
        self.show_password_checkbutton.destroy()

    def select_directory(self):
        # Open a directory selection dialog and set the selected directory in the Entry
        selected_directory = filedialog.askdirectory()
        self.output_dir_entry.delete(0, "end")  # Delete the current value
        self.output_dir_entry.insert(0, selected_directory)  # Insert the selected directory

    def print_window_size(self, event):
        # Get the current width and height of the window
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        print(f"Window size: {width}x{height}")


# Bind the click event to the on_click function
root = TkinterDnD.Tk()
root.title("PDF Password Remover")
root.geometry("750x450")
root.minsize(700, 200)  # Set the minimum window size to 500x300
app = PDFPasswordRemoverApp(master=root)
app.pack(fill='both', expand=True)  # Make the app expandable
# Bind the <Configure> event to the print_window_size function
#root.bind("<Configure>", app.print_window_size)
app.mainloop()

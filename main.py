import tkinter as tk
from tkinter import filedialog, ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
from PyPDF2 import PdfReader, PdfWriter
import os
import traceback

class Application(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.file_list = ttk.Treeview(self)
        self.file_list["columns"]=("one","two","three","four")
        self.file_list.column("#0", width=50)
        self.file_list.column("one", width=100)
        self.file_list.column("two", width=100)
        self.file_list.column("three", width=100)
        self.file_list.column("four", width=100)
        self.file_list.heading("#0",text="Item")
        self.file_list.heading("one", text="File name")
        self.file_list.heading("two", text="Size")
        self.file_list.heading("three", text="Pages")
        self.file_list.heading("four", text="Password")
        self.file_list.pack(side="top")

        self.select_button = tk.Button(self)
        self.select_button["text"] = "Select PDF"
        self.select_button["command"] = self.get_pdf_file
        self.select_button.pack(side="top")

        self.output_var = tk.StringVar(value="same")
        self.same_folder_button = tk.Radiobutton(self, text="Same folder", variable=self.output_var, value="same")
        self.same_folder_button.pack(side="top")

        self.custom_folder_button = tk.Radiobutton(self, text="Custom folder", variable=self.output_var, value="custom")
        self.custom_folder_button.pack(side="top")

        self.execute_button = tk.Button(self, text="EXECUTE", fg="red", command=self.unlock_pdf)
        self.execute_button.pack(side="bottom")

        # Bind the function to the Treeview widget
        self.file_list.bind("<ButtonRelease-1>", self.show_password_entry)
        # Bind the <<Drop>> event to the Treeview widget
        self.file_list.dnd_bind('<<Drop>>', self.drop)

    def drop(self, event):
        # Get the path of the dropped file
        dropped_file_path = event.data
        if os.path.isfile(dropped_file_path) and dropped_file_path.endswith('.pdf'):
            self.add_file_to_list(dropped_file_path)
    def get_pdf_file(self):
        pdf_file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if pdf_file_path:
            # Get the item number
            item_number = len(self.file_list.get_children()) + 1
            # Get the file size in KB
            file_size = os.path.getsize(pdf_file_path) / 1024
            # Get the file name
            file_name = os.path.basename(pdf_file_path)
            # Get the number of pages in the PDF
            pdf_reader = PdfReader(pdf_file_path)
            if pdf_reader.is_encrypted:
                num_pages = "Unknown"
            else:
                num_pages = len(pdf_reader.pages)
            # Add file to the list
            self.file_list.insert("", "end", text=item_number,
                                  values=(file_name, f"{file_size:.2f} KB", num_pages, ""))

    def show_password_entry(self, event):
        # Create an Entry widget for password input
        self.password_entry = tk.Entry(self)
        self.password_entry.pack()

    def unlock_pdf(self):
        for item in self.file_list.get_children():
            pdf_file_path = self.file_list.item(item)["values"][0]
            password = self.file_list.item(item)["values"][3]
            # Get password and decrypt the file
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
                    print("An error occurred:")
                    traceback.print_exc()  # Print the details of the exception
                    print("Incorrect password")

root = TkinterDnD.Tk()
app = Application(master=root)
app.mainloop()
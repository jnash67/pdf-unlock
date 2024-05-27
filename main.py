import tkinter as tk
from tkinter import filedialog
from PyPDF2 import PdfReader, PdfWriter
import traceback
import os

def get_pdf_file():
    global pdf_file_path
    print("get pdf file")
    pdf_file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    print(pdf_file_path)

def unlock_pdf():
    password = password_entry.get()
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

root = tk.Tk()
pdf_file_path = ""

select_button = tk.Button(root, text="Select PDF", command=get_pdf_file)
select_button.pack()

password_entry = tk.Entry(root)
password_entry.pack()

unlock_button = tk.Button(root, text="Unlock PDF", command=unlock_pdf)
unlock_button.pack()

root.mainloop()# This is a sample Python script.

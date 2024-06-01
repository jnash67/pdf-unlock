import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfFileWriter, PdfFileReader

class PDFPasswordRemoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Password Remover")

        # Frame for file list
        self.frame = tk.Frame(root)
        self.frame.pack(padx=10, pady=10)

        # Add Files button
        self.add_files_button = tk.Button(self.frame, text="Add Files...", command=self.add_files)
        self.add_files_button.grid(row=0, column=0, padx=5, pady=5)

        # File list
        self.file_listbox = tk.Listbox(self.frame, selectmode=tk.MULTIPLE, width=60)
        self.file_listbox.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

        # Scrollbar for the file list
        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical")
        self.scrollbar.config(command=self.file_listbox.yview)
        self.scrollbar.grid(row=1, column=3, sticky='ns')
        self.file_listbox.config(yscrollcommand=self.scrollbar.set)

        # Remove Files button
        self.remove_files_button = tk.Button(self.frame, text="Remove", command=self.remove_files)
        self.remove_files_button.grid(row=2, column=0, padx=5, pady=5)

        # Clear Files button
        self.clear_files_button = tk.Button(self.frame, text="Clear", command=self.clear_files)
        self.clear_files_button.grid(row=2, column=1, padx=5, pady=5)

        # Output folder selection
        self.output_folder_var = tk.StringVar(value="")
        self.save_in_source_folder = tk.Radiobutton(root, text="Save target file(s) in source folder", variable=self.output_folder_var, value="")
        self.save_in_source_folder.pack(anchor='w')
        self.custom_folder = tk.Radiobutton(root, text="Customize", variable=self.output_folder_var, value="custom")
        self.custom_folder.pack(anchor='w')
        self.custom_folder_path_entry = tk.Entry(root, width=50)
        self.custom_folder_path_entry.pack(padx=5, pady=5, anchor='w')
        self.custom_folder_path_entry.config(state='disabled')
        self.output_folder_var.trace("w", self.toggle_custom_folder)

        # Start button
        self.start_button = tk.Button(root, text="Start", command=self.remove_passwords)
        self.start_button.pack(padx=5, pady=10)

    def add_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        for path in file_paths:
            self.file_listbox.insert(tk.END, path)

    def remove_files(self):
        selected_files = self.file_listbox.curselection()
        for i in reversed(selected_files):
            self.file_listbox.delete(i)

    def clear_files(self):
        self.file_listbox.delete(0, tk.END)

    def toggle_custom_folder(self, *args):
        if self.output_folder_var.get() == "custom":
            self.custom_folder_path_entry.config(state='normal')
        else:
            self.custom_folder_path_entry.config(state='disabled')

    def remove_passwords(self):
        files = self.file_listbox.get(0, tk.END)
        if not files:
            messagebox.showerror("Error", "No files selected")
            return

        output_folder = self.custom_folder_path_entry.get() if self.output_folder_var.get() == "custom" else None

        for file in files:
            try:
                with open(file, "rb") as infile:
                    reader = PdfFileReader(infile)
                    if reader.isEncrypted:
                        reader.decrypt("")  # Assuming the password is an empty string for this example
                        writer = PdfFileWriter()
                        for i in range(reader.getNumPages()):
                            writer.addPage(reader.getPage(i))
                        output_file = f"{output_folder}/{file.split('/')[-1]}" if output_folder else file
                        with open(output_file, "wb") as outfile:
                            writer.write(outfile)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to process {file}\n{e}")

        messagebox.showinfo("Success", "Passwords removed successfully")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFPasswordRemoverApp(root)
    root.mainloop()

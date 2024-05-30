import tkinter as tk
from tkinter import filedialog, ttk

class PDFPasswordRemover(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PDF Password Remover")
        self.geometry("600x400")

        # Create a frame to hold the treeview and scrollbars
        tree_frame = tk.Frame(self)
        tree_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Create a treeview to display the PDF files
        self.tree = ttk.Treeview(tree_frame, columns=("File Name", "Size", "Pages", "Status"))
        self.tree.heading("#0", text="Item")
        self.tree.heading("File Name", text="File Name")
        self.tree.heading("Size", text="Size")
        self.tree.heading("Pages", text="Total Pages")
        self.tree.heading("Status", text="Status")
        self.tree.column("#0", width=50)
        self.tree.column("File Name", width=200)
        self.tree.column("Size", width=100)
        self.tree.column("Pages", width=100)
        self.tree.column("Status", width=100)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create scrollbars for the treeview
        tree_scrollbar_y = tk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        tree_scrollbar_x = tk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=tree_scrollbar_y.set, xscrollcommand=tree_scrollbar_x.set)
        tree_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        tree_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        # Create buttons
        button_frame = tk.Frame(self)
        add_button = tk.Button(button_frame, text="Add Files", command=self.add_files)
        clear_button = tk.Button(button_frame, text="Clear", command=self.clear_files)
        add_button.pack(side=tk.LEFT, padx=5)
        clear_button.pack(side=tk.LEFT, padx=5)
        button_frame.pack(pady=5)

        # Create output folder option
        output_folder_frame = tk.Frame(self)
        self.output_folder_var = tk.StringVar()
        self.output_folder_var.set("Customize output folder")
        output_folder_option1 = tk.Radiobutton(output_folder_frame, text="Save target file(s) in source folder", variable=self.output_folder_var, value="Source Folder")
        output_folder_option2 = tk.Radiobutton(output_folder_frame, text="Customize output folder", variable=self.output_folder_var, value="Customize output folder")
        output_folder_option1.pack(side=tk.LEFT)
        output_folder_option2.pack(side=tk.LEFT)
        output_folder_frame.pack(pady=5)

        # Create start button
        start_button = tk.Button(self, text="Start", state=tk.DISABLED)
        start_button.pack(pady=10)

    def add_files(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        for file in files:
            # Add code to get file information and insert into the treeview
            pass

    def clear_files(self):
        self.tree.delete(*self.tree.get_children())

if __name__ == "__main__":
    app = PDFPasswordRemover()
    app.mainloop()
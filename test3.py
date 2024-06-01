import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class MyApp:
    def __init__(self, root):
        self.root = root
        self.tree = ttk.Treeview(root)
        self.tree["columns"]=("one","two")

        # Configure the columns
        self.tree.column("#0", width=100, minwidth=50, stretch=tk.NO)
        self.tree.heading("#0",text="First Column",anchor=tk.W)

        self.tree.column("one", width=100, minwidth=50, stretch=tk.NO)
        self.tree.heading("one", text="Column One", anchor=tk.W)

        self.tree.column("two", width=100, minwidth=50, stretch=tk.NO)
        self.tree.heading("two", text="Column Two", anchor=tk.W)

        # Load and resize the image
        image = Image.open("icons8-lock-48.png")  # Replace with the path to your image
        image = image.resize((20, 20))  # Resize the image
        self.image = ImageTk.PhotoImage(image)

        # Insert a new item with the image in the 'one' column
        self.tree.insert('', 'end', text="Item 1", image=self.image, values=("Value 1", "Value 2"))

        self.tree.pack(side="top", fill="both", expand=True)

root = tk.Tk()
app = MyApp(root)
root.mainloop()
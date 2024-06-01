import os


def print_window_size(self, event):
    # Get the current width and height of the window
    width = self.master.winfo_width()
    height = self.master.winfo_height()
    print(f"Window size: {width}x{height}")


def load_pdfs_from_default_dir(self):
    default_dir = os.getcwd()  # Replace with the path to your default directory if it's not the current directory
    for file_name in os.listdir(default_dir):
        if file_name.endswith('.pdf'):
            file_path = os.path.join(default_dir, file_name)
            self.add_file_to_list(file_path)

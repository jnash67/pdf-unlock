import os
import sys
from pathlib import Path


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


def print_column_widths(self):
    for col in self.file_list_treeview["columns"]:
        width = self.file_list_treeview.column(col)["width"]
        print(f"Column '{col}' width: {width}")


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:  # _MEIPASS not found, so not running under PyInstaller
        # Use the directory of the current script (utils.py) as the base path
        base_path = os.path.dirname(os.path.abspath(__file__))

    joined_path = os.path.join(base_path, relative_path)
    return joined_path


def get_default_downloads_path():
    """Determines a sensible default path, preferring Downloads, then Home, then CWD."""
    paths_to_try = []
    try:
        paths_to_try.append(Path.home() / "Downloads")
        paths_to_try.append(Path.home())
    except RuntimeError as e:
        print(f"INFO: Could not determine home directory: {e}. Defaulting path to CWD.")
        return os.getcwd() # Early exit if home is not found

    for path_obj in paths_to_try:
        try:
            if path_obj.exists() and path_obj.is_dir():
                return str(path_obj)
        except OSError as e: # Catch potential permission errors etc. during exists/is_dir
            print(f"INFO: Error accessing {path_obj}: {e}. Trying next default path.")
            continue
    print("INFO: Downloads and Home directories not found or accessible. Defaulting to CWD.")
    return os.getcwd()

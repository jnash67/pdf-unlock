import os
import time
import datetime
from cx_Freeze import setup, Executable

# Set a minimum timestamp for all files (January 1, 1980)
min_date = datetime.datetime(1980, 1, 1)
min_timestamp = time.mktime(min_date.timetuple())

# Try to find tkinterdnd2 directory
import site
import glob
site_packages = site.getsitepackages()[0]
tkdnd_path = None
for path in glob.glob(os.path.join(site_packages, "tkinterdnd2/tkdnd")):
    if os.path.exists(path):
        tkdnd_path = path
        break

if not tkdnd_path:
    print("Warning: tkinterdnd2/tkdnd directory not found!")
    # Try to find it manually
    possible_paths = [
        "/home/backup_user/VoidProjects/pdf-unlock/PDF-Password-Remover/env/lib/python3.12/site-packages/tkinterdnd2/tkdnd",
        "/usr/lib/python3/dist-packages/tkinterdnd2/tkdnd"
    ]
    for path in possible_paths:
        if os.path.exists(path):
            tkdnd_path = path
            print(f"Found tkdnd at: {tkdnd_path}")
            break

include_files = []
if tkdnd_path:
    include_files.append((tkdnd_path, "tkinterdnd2/tkdnd"))

# Your existing setup code
setup(
    name="PDF-Password-Remover",
    version="1.0",
    description="Remove passwords from PDF files",
    options={"build_exe": {
        "packages": ["tkinter", "PIL", "fitz", "tkinterdnd2"],
        "include_files": include_files
    }},
    executables=[Executable("pdf_password_remover.py")]  # Replace with your actual main script
)
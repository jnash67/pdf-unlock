"""PyInstaller hook file for tkinterdnd2.

You need to use this hook-file if you are packaging a project using tkinterdnd2.
This hook file is located in pyinstaller-hooks/linux/ directory.
To use it with PyInstaller, run:

    pyinstaller myproject/myproject.py --additional-hooks-dir=pyinstaller-hooks/linux
    
or if you are in a different directory:

    pyinstaller myproject/myproject.py --additional-hooks-dir=/path/to/pyinstaller-hooks/linux
"""
from PyInstaller.utils.hooks import collect_data_files, collect_submodules
import os
import sys
import platform

# First, make sure we can import tkinterdnd2
try:
    import tkinterdnd2
except ImportError:
    print("WARNING: tkinterdnd2 module not found")
    datas = []
    hiddenimports = []
else:
    # Get the tkinterdnd2 installation directory
    tkdnd_path = os.path.dirname(tkinterdnd2.__file__)
    print(f"tkinterdnd2 path: {tkdnd_path}")

    # Determine the correct library path based on architecture
    machine = platform.machine().lower()
    
    # Check if we're on Linux
    if platform.system() == 'Linux':
        if machine in ('x86_64', 'amd64'):
            lib_dir = os.path.join(tkdnd_path, 'tkdnd', 'linux64')  # Changed from linux-x64 to match your error message
            print(f"Using x64 library dir: {lib_dir}")
        else:
            lib_dir = os.path.join(tkdnd_path, 'tkdnd', 'linux-arm64')
            print(f"Using ARM64 library dir: {lib_dir}")
    else:
        # On Windows or Mac, adjust paths accordingly
        if platform.system() == 'Windows':
            lib_dir = os.path.join(tkdnd_path, 'tkdnd', 'win64' if machine in ('x86_64', 'amd64') else 'win32')
        else:  # macOS
            lib_dir = os.path.join(tkdnd_path, 'tkdnd', 'osx64')
        print(f"Using library dir: {lib_dir}")

    # Collect all data files
    datas = []

    # Explicitly add the tkdnd library directory and all its contents
    if os.path.exists(lib_dir):
        # Print the files that exist in the directory
        print(f"Files in {lib_dir}:")
        for file in os.listdir(lib_dir):
            print(f"  - {file}")
            
        # Add the entire directory
        # The target path is calculated relative to the tkinterdnd2 package
        target_path = os.path.join('tkinterdnd2', 'tkdnd', os.path.basename(lib_dir))
        datas.append((lib_dir, target_path))
        print(f"Adding library directory: {lib_dir} -> {target_path}")
        
        # Also add the parent directory for good measure
        tkdnd_dir = os.path.join(tkdnd_path, 'tkdnd')
        if os.path.exists(tkdnd_dir):
            datas.append((tkdnd_dir, 'tkinterdnd2/tkdnd'))
            print(f"Adding tkdnd directory: {tkdnd_dir} -> tkinterdnd2/tkdnd")
    else:
        print(f"WARNING: tkdnd library directory not found: {lib_dir}")

    # Add other tkinterdnd2 data files
    tkdnd_data = collect_data_files('tkinterdnd2')
    datas += tkdnd_data
    print(f"Collected {len(tkdnd_data)} additional data files from tkinterdnd2")

    # Hidden imports
    hiddenimports = collect_submodules('tkinterdnd2')

# Add PIL data files and imports
try:
    from PIL import Image
    datas += collect_data_files('PIL')
    hiddenimports += collect_submodules('PIL')
    hiddenimports += ['PIL._tkinter_finder']
except ImportError:
    print("WARNING: PIL module not found")
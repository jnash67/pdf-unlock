"""PyInstaller hook file for tkinterdnd2.

You need to use this hook-file if you are packaging a project using tkinterdnd2.
This hook file is located in pyinstaller-hooks/linux/ directory.
To use it with PyInstaller, run:

    pyinstaller myproject/myproject.py --additional-hooks-dir=pyinstaller-hooks/windows
    
or if you are in a different directory:

    pyinstaller myproject/myproject.py --additional-hooks-dir=/path/to/pyinstaller-hooks/windows
"""

from PyInstaller.utils.hooks import collect_data_files, eval_statement


datas = collect_data_files('tkinterdnd2')
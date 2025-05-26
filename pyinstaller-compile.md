# Compile to executable with pyinstaller

## Overview

Specifying the right flags for pyinstaller can be very tricky. These resources were useful:
https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
https://www.youtube.com/watch?v=p3tSLatmGvU&t=135s
https://github.com/pmgagne/tkinterdnd2/blob/master/hook-tkinterdnd2.py

## .gitignore
For a git project you want to add the following to the .gitignore file if you're using pyinstaller

```gitignore
# PyInstaller
*.spec
dist/
build/
```

## Windows compilation

* Note: The below has not been tested in Windows since some changes were made that could impact this.
* In a terminal, be sure you're in the PDF-Password-Remover project directory.
* Then run:

```
pyinstaller --noconfirm --onefile \
     --windowed --noconsole \
     --icon "favicon.ico" \
     --name "PDF-Password-Remover" \
     --clean \
     --add-data ".;." \
     --additional-hooks-dir "./pyinstaller-hooks/windows" \
     ./__main__.py
```

## Linux environment setup

```bash
sudo apt install python3-venv
git clone https://github.com/jnash67/pdf-unlock.git
python3 -m venv pdf_unlock_env
# Activate the virtual environment
source pdf_unlock_env/bin/activate
cd ~/pdf-unlock
pip install -r requirements.txt
pip install pyinstaller
cd PDF-Password-Remover
python __main__.py
```

## Linux compilation

Make sure you're in the PDF-Password-Remover project directory where you were left in the setup section above.
Note set "--debug all" if you want debug output when running pyinstaller.

```bash
rm -rf build dist
rm -f PDF-Password-Remover.spec

pyinstaller --noconfirm --onefile \
    --name "PDF-Password-Remover" \
    --clean \
    --add-data "icons:icons" \
    --additional-hooks-dir ./pyinstaller-hooks/linux \
    --hidden-import PIL._tkinter_finder \
    --hidden-import PIL \
    --collect-submodules PIL \
    --debug none \
    ./__main__.py
```

After successful compilation:

```bash
cd dist
./PDF-Password-Remover
```

## Linux install

To install in the system (change user 'backup_user' to whatever the user actually is):

cat > ~/.local/share/applications/PDF-Password-Remover.desktop << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=PDF Password Remover
Comment=Remove passwords from PDF files
Exec=bash -c "cd /home/backup_user/pdf-unlock/PDF-Password-Remover/dist && ./PDF-Password-Remover"
Icon=/home/backup_user/pdf-unlock/PDF-Password-Remover/favicon.ico
Terminal=false
Categories=Utility;
EOF

chmod +x /home/backup_user/pdf-unlock/PDF-Password-Remover/dist/PDF-Password-Remover
chmod +x ~/.local/share/applications/PDF-Password-Remover.desktop
update-desktop-database ~/.local/share/applications
cd /home/backup_user/pdf-unlock/PDF-Password-Remover
cp icons8* favicon.ico dist/
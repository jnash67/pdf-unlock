# PDF Password Remover Application

## Overview
This program lets you select PDF files and, if they are locked, enables you create an unlocked version.
By default, the program adds a "_NoPW" extension to the file name of the unlocked file.
You can specify your own default extension in the "New Filename Ending:" text box at bottom left.
If there is no text in that text box (i.e. you've removed all the text) then it will overwrite the existing PDF file.

When you add a locked PDF, there will be a little lock icon in the Item column (the leftmost column in the table).
If you click on the lock icon, you will be asked to enter the password of file.  If you try to unlock a PDF file and no password has been entered then nothing will happen.

By default, the program will save the unlocked file in the same directory as the original PDF.
There is an option for you to specify a custom output folder.

## Usage
To run this project simply clone the repository, run `pip install -r requirements.txt` and then
run `python PDF-Password-Remover`.

To create the executable with pyinstaller, be sure you're in the PDF-Password-Remover project directory
(i.e. from the main project directory `cd PDF-Password-Remover`).
Then run:
`pyinstaller --noconfirm --onefile --windowed --noconsole --icon "favicon.ico" 
--name "PDF-Password-Remover" --clean --additional-hooks-dir "." --add-data ".;."  ./__main__.py`

Figuring out the right flags in the right format for pyinstaller was crazy difficult. These resources were useful:
https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
https://www.youtube.com/watch?v=p3tSLatmGvU&t=135s
https://github.com/pmgagne/tkinterdnd2/blob/master/hook-tkinterdnd2.py

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
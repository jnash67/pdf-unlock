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

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
from tkinterdnd2 import TkinterDnD
from pdf_password_remover import PDFPasswordRemoverApp

root = TkinterDnD.Tk()
root.title("PDF Password Remover")
root.geometry("750x450")
root.minsize(680, 250)  # Set the minimum window size to 500x300
app = PDFPasswordRemoverApp(master=root)
app.pack(fill='both', expand=True)  # Make the app expandable
app.mainloop()

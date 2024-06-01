from pdf_password_remover_app import PDFPasswordRemoverApp
from tkinterdnd2 import TkinterDnD

root = TkinterDnD.Tk()
root.title("PDF Password Remover")
root.geometry("750x450")
root.minsize(700, 200)  # Set the minimum window size to 500x300
app = PDFPasswordRemoverApp(master=root)
app.pack(fill='both', expand=True)  # Make the app expandable
app.mainloop()

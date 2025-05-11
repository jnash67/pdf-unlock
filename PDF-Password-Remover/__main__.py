from tkinterdnd2 import TkinterDnD
from pdf_password_remover import PDFPasswordRemoverApp

if __name__ == "__main__":
    try:
        root = TkinterDnD.Tk()
        root.title("PDF Password Remover")
        root.geometry("750x450")
        root.minsize(680, 250)
        app = PDFPasswordRemoverApp(master=root)
        app.pack(fill='both', expand=True)
        root.mainloop()
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

import tkinter as tk


class PasswordDialog(tk.Toplevel):
    def __init__(self, master, initial_password="", title="Password"):
        super().__init__(master)
        self.password_entry = None
        self.initial_password = initial_password
        self.result = None
        self.title(title)
        self.geometry(self.calculate_geometry())
        self.transient(master)  # Make the dialog a transient window to the main window
        self.create_widgets()
        self.grab_set()  # Ensure the dialog grabs focus

    def calculate_geometry(self):
        # Get the center position of the main application window
        master = self.master
        window_x = master.winfo_rootx()
        window_y = master.winfo_rooty()
        window_width = master.winfo_width()
        window_height = master.winfo_height()

        dialog_width = 300  # Estimated width of the dialog box
        dialog_height = 100  # Estimated height of the dialog box

        center_x = window_x + (window_width - dialog_width) // 2
        center_y = window_y + (window_height - dialog_height) // 2

        return f"{dialog_width}x{dialog_height}+{center_x}+{center_y}"

    def create_widgets(self):
        tk.Label(self, text="Enter the password:").pack(pady=10)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)
        self.password_entry.insert(0, self.initial_password)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="OK", command=self.on_ok).pack(side="left", padx=20)
        tk.Button(button_frame, text="Cancel", command=self.on_cancel).pack(side="right", padx=20)

    def on_ok(self):
        self.result = self.password_entry.get()
        self.destroy()

    def on_cancel(self):
        self.destroy()

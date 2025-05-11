import tkinter as tk


class ToolTip:
    def __init__(self, widget):
        self.widget = widget
        self.tip_window = None

    def show_tip(self, tip_text, event=None):
        "Display text in a tooltip window"
        if self.tip_window or not tip_text:
            return

        if event: # Position near mouse cursor
            x = event.x_root + 15 # offset from cursor
            y = event.y_root + 10 # offset from cursor
        else: # Fallback if no event (e.g. programmatic show)
            x = self.widget.winfo_rootx() + 20
            y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5

        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=tip_text, background="#ffffe0", relief=tk.SOLID, borderwidth=1)
        label.pack()

    def hide_tip(self):
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()


def create_tooltip(widget, text):
    tool_tip = ToolTip(widget)

    def enter(event):
        tool_tip.show_tip(text, event) # Pass the event

    def leave(event):
        tool_tip.hide_tip()

    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

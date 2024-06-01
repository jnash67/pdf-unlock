import tkinter as tk

class ToolTip:
    def __init__(self, widget):
        self.widget = widget
        self.tip_window = None

    def show_tip(self, tip_text, item_id):
        "Display text in a tooltip window"
        if self.tip_window or not tip_text:
            return
        bbox = self.widget.bbox(item_id)
        if bbox:
            x, y, _, _ = bbox
            x = x + self.widget.winfo_rootx() + 25
            y = y + self.widget.winfo_rooty() + 20
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

    def motion(event):
        column = widget.identify_column(event.x)
        row = widget.identify_row(event.y)
        if row:
            status = widget.set(row, "Status")
            # Check if the mouse cursor is over the column with the lock image
            if column == "#0" and status == "Locked":
                # Get the bounding box of the cell
                x, y, width, height = widget.bbox(row, column)
                # Check if the mouse cursor is within the bounding box of the cell
                if x < event.x < x + width and y < event.y < y + height:
                    tool_tip.show_tip(text, row)
                else:
                    tool_tip.hide_tip()
            else:
                tool_tip.hide_tip()

    widget.bind('<Motion>', motion)
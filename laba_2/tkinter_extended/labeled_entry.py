import tkinter as tk
from tkinter import ttk

from placeholdered_entry import PlaceholderEntry


class LabeledEntryField:
    def __init__(self, master, label_text, entry_width=20, placeholder=""):
        """Initialize the labeled entry field.

        Args:
        master (tk.Widget): Parent widget.
        label_text (str): Text for the label.
        entry_width (int): Width of the entry field.
        placeholder (str): placeholder
        """
        self.frame = tk.Frame(master)
        self.label = tk.Label(self.frame, text=label_text)
        if placeholder:
            self.entry = PlaceholderEntry(
                self.frame, width=entry_width, placeholder=placeholder
            )
        else:
            self.entry = tk.Entry(self.frame, width=entry_width)

        self.label.pack(side="left", padx=5, pady=5)
        self.entry.pack(side="left", padx=5, pady=5)

        self.frame.pack(pady=5, padx=5, fill="x")
        self.placeholder = placeholder

    def get(self):
        """Return the current contents of the entry field."""
        text = self.entry.get()
        if text == self.placeholder:
            return ""
        return text

    def set(self, text):
        """Set the contents of the entry field."""
        self.entry.delete(0, tk.END)
        self.entry.insert(0, text)

    def pack(self, **kwargs):
        """Pack the frame into the master widget."""
        self.frame.pack(**kwargs)

    def grid(self, **kwargs):
        """Grid the frame into the master widget."""
        self.frame.grid(**kwargs)

    def place(self, **kwargs):
        """Place the frame into the master widget."""
        self.frame.place(**kwargs)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Labeled Entry Field Example")

    frame = ttk.LabelFrame(root, text="menu")
    frame.pack()
    name_field = LabeledEntryField(
        frame, "Name:", entry_width=8, placeholder="bruh"
    )
    email_field = LabeledEntryField(
        frame, "Email:", entry_width=16, placeholder="name@example.com"
    )

    def submit():
        print(f"Name: {name_field.get()}")
        print(f"Email: {email_field.get()}")

    button = tk.Button(root, text="Submit", command=submit)
    button.pack(pady=10)

    root.mainloop()

from tkinter import Tk
from tkinter.constants import TOP
from tkinter.ttk import Frame

from tkinter_extended.focus_sensitive_elems import Button
from tkinter_extended.labeled_entry import LabeledEntryField


def start_exam(name: str): ...


def set_up_menu() -> Tk:
    root = Tk()
    root.title("Exam")

    frame_menu = Frame(root)
    frame_menu.pack(side=TOP)

    entry_name = LabeledEntryField(frame_menu, label_text="Name: ")

    frame_button = Frame(root)
    frame_button.pack()

    button_start_test = Button(
        frame_button,
        text="Start exam",
        command=lambda: start_exam(entry_name.get()),
    )
    button_start_test.pack()

    return root


if __name__ == "__main__":
    app = set_up_menu()
    app.mainloop()

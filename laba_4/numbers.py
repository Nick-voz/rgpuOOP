from tkinter import BOTTOM
from tkinter import LEFT
from tkinter import TOP
from tkinter import Tk
from tkinter.ttk import Frame
from tkinter.ttk import Label
from typing import Callable

from tkinter_extended.focus_sensitive_elems import Button
from tkinter_extended.labeled_entry import LabeledEntryField
from tkinter_extended.set_up_util import clear_frame


def set_up_menu(frame: Frame):
    frame_menu = Frame(frame)
    frame_menu.pack(side=LEFT)

    frame_info = Frame(frame)
    frame_info.pack(side=TOP)

    frame_entry_numebrs = Frame(frame_menu)
    frame_entry_numebrs.pack(side=TOP)

    frame_buttons = Frame(frame_menu)
    frame_buttons.pack(side=TOP)

    entry_first_number = LabeledEntryField(
        frame_entry_numebrs, label_text="Insert firsty number", entry_width=5
    )
    entry_first_number.pack(side=TOP)
    entry_secont_number = LabeledEntryField(
        frame_entry_numebrs, label_text="Insert second number", entry_width=5
    )
    entry_secont_number.pack(side=TOP)

    buttons = (
        ("Create objects", lambda: ...),
        ("Delete objects", lambda: ...),
        ("Calc GCD", lambda: ...),
        ("Calc LCM", lambda: ...),
        ("Calc prime numbers in range", lambda: ...),
    )

    for text, command in buttons:
        button = Button(frame_buttons, text=text, command=command, width=20)
        button.pack()

    text_gcd = "GCD: "
    text_lcm = "LCM: "
    text_prime_num = "Prime numbers: "

    label_gcd = Label(frame_info, text=text_gcd, width=15)
    label_gcd.pack(anchor="w")

    lable_lcm = Label(frame_info, text=text_lcm, width=15)
    lable_lcm.pack(anchor="w")

    lable_prime_numbers = Label(frame_info, text=text_prime_num, width=15)
    lable_prime_numbers.pack(anchor="w")


def set_up_numbers(root: Frame, callback: Callable):
    clear_frame(root)
    frame = Frame(root)
    frame.pack()
    set_up_menu(frame)
    Button(root, text="Back", command=callback).pack(side=BOTTOM)


def main():
    root = Tk()
    frame = Frame()
    frame.pack()
    set_up_menu(frame)
    root.mainloop()


if __name__ == "__main__":
    main()

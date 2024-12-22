from tkinter import BOTTOM
from tkinter import Tk
from tkinter.ttk import Frame
from typing import Callable

from tkinter_extended.focus_sensitive_elems import Button
from tkinter_extended.set_up_util import clear_frame


def set_up_menu(frame: Frame):
    pass


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

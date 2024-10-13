from tkinter.ttk import Frame
from typing import Callable

from laba_2.num_translater_interface import set_up_num_translater
from laba_2.word_translater_interface import set_up_word_translater
from tkinter_extended.set_up_util import set_up


def set_up_laba_2(frame: Frame, callback: Callable):
    buttons = (
        ("Num translater", set_up_num_translater),
        ("Word translater", set_up_word_translater),
    )
    set_up(frame, buttons, callback)


""" def set_up_laba_2(frame: Frame, callback: Callable):

    for widget in frame.winfo_children():
        widget.pack_forget()

    frame.pack()
    buttons = (
        (
            "Num translater",
            lambda: set_up_num_translater(
                frame, lambda: set_up_laba_2(frame, callback)
            ),
        ),
        (
            "Word translater",
            lambda: set_up_word_translater(
                frame, lambda: set_up_laba_2(frame, callback)
            ),
        ),
        ("Back", callback),
    )
    for text, command in buttons:
        button = Button(frame, text=text, command=command)
        button.pack() """

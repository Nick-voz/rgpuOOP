from tkinter.ttk import Frame
from typing import Callable

from tkinter_extended.set_up_util import set_up

from laba_4.exam import set_up_exam


def set_up_laba_4(frame: Frame, callback: Callable):
    frame.winfo_toplevel().title("Laba 4")
    buttons = [
        ("exam", set_up_exam),
    ]
    set_up(frame, buttons, callback)

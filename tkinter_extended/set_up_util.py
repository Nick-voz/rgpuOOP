from tkinter import BOTTOM
from tkinter.ttk import Frame
from typing import Callable

from tkinter_extended.focus_sensitive_elems import Button


def set_up(frame: Frame, buttons, callback: Callable = None):
    for widget in frame.winfo_children():
        widget.destroy()
    frame.pack()

    def _callback():
        set_up(frame, buttons, callback)

    for text, command in buttons:
        Button(
            frame,
            text=text,
            command=lambda cmd=command, frm=frame: cmd(frm, _callback),
        ).pack()

    if callback is not None:
        Button(frame, text="Back", command=callback).pack(side=BOTTOM)

from tkinter.ttk import Frame
from typing import Callable

from laba_3.ball import set_up_ball
from laba_3.bank import set_up_bank
from laba_3.bus import set_up_bus
from laba_3.live_button import set_up_live_button
from laba_3.power_of import set_up_power_of
from tkinter_extended.focus_sensitive_elems import Button
from tkinter_extended.set_up_util import set_up


def set_up_laba_3(frame: Frame, callback: Callable):
    buttons = (
        ("Ball", set_up_ball),
        ("Bank", set_up_bank),
        ("Live Button", set_up_live_button),
        ("Bus", set_up_bus),
        ("Power of", set_up_power_of),
    )
    set_up(frame, buttons, callback)

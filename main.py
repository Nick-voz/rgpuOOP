from tkinter import Tk
from tkinter.ttk import Frame

from laba_2.laba_2_main import set_up_laba_2
from laba_3.laba_3_main import set_up_laba_3
from tkinter_extended.set_up_util import set_up


def set_up_main(frame: Frame):
    buttons = (("laba 2", set_up_laba_2), ("laba 3", set_up_laba_3))
    set_up(frame, buttons)


if __name__ == "__main__":
    root = Tk()
    set_up_main(Frame(root))
    root.mainloop()

from tkinter import BOTTOM
from tkinter import Tk
from tkinter.constants import LEFT
from tkinter.constants import TOP
from tkinter.ttk import Frame
from tkinter.ttk import Label
from typing import Callable
from typing import Optional
from typing import TypeVar

from tkinter_extended.focus_sensitive_elems import Button
from tkinter_extended.labeled_entry import LabeledEntryField

T = TypeVar("T")


class PowerChecer:
    def __init__(self):
        self._number: Optional[int] = None

    def set_number(self, number: int):
        if isinstance(number, int) is False:
            raise ValueError(f"axcept integer, got {number}")
        self._number = number

    def is_power_of(self, base: int) -> bool:
        self._number = self.__raise_if_number_is_none(self._number)

        if base == 0:
            raise ValueError("base must be not zero")

        current = base
        while current < self._number:
            current *= base

        return current == self._number

    def is_positiv_and_even(self) -> bool:
        self._number = self.__raise_if_number_is_none(self._number)

        if self._number <= 0:
            return False

        return self._number % 2 == 0

    @staticmethod
    def __raise_if_number_is_none(number: Optional[T]) -> T:
        if number is None:
            raise ValueError(
                "self._number is None, set_number should by calld before"
            )
        return number


class App:
    def __init__(self, frame: Frame):
        self.root = frame
        self.root.winfo_toplevel().title("Is power of")
        self.power_checker: Optional["PowerChecer"] = None
        self.run()

    def run(self):
        self.__set_up_mnnu()
        self.__set_up_info()

    def mainloop(self):
        self.root.mainloop()

    def __set_up_mnnu(self):
        self.frame_menu = Frame(self.root)
        self.frame_menu.pack(side=LEFT)

        buttons = (
            ("Create", lambda: self.__set_power_shecker()),
            ("Input", lambda: self.__set_number_to_power_checker()),
            ("Check pow", lambda: self.__check_power_of_2()),
            ("check even", lambda: self.__check_is_positive_and_even()),
            ("Delete", lambda: self._delete()),
        )

        for text, command in buttons:
            button = Button(
                self.frame_menu, text=text, command=command, width=10
            )
            button.pack(side=TOP, padx=5)

    def __set_up_info(self):
        self.frame_info = Frame(self.root)
        self.frame_info.pack(side=LEFT)
        self.entry = LabeledEntryField(
            self.frame_info, label_text="Insert number"
        )
        self.entry.pack(side=TOP)

    def __set_power_shecker(self):
        self.power_checker = PowerChecer()

    def __set_number_to_power_checker(self):
        if self.power_checker is None:
            raise RuntimeError

        str_num = self.entry.get()
        try:
            number = int(str_num)
        except ValueError:
            self.entry.set("Number must be integer")
            return

        self.power_checker.set_number(number)

    def __check_power_of_2(self):
        if self.power_checker is None or self.power_checker._number is None:
            return
        if self.power_checker.is_power_of(2):
            text = f"{self.power_checker._number} is a power of 2"
        else:
            text = f"{self.power_checker._number} is not power of 2"
        self.anwer_is_power = Label(self.frame_info, text=text)
        self.anwer_is_power.pack(side=TOP)

    def _delete(self):
        self.anwer_is_power.pack_forget()
        self.anwer_is_positive_and_even.pack_forget()
        self.power_checker = None
        self.entry.set("")

    def __check_is_positive_and_even(self):

        if self.power_checker is None or self.power_checker._number is None:
            return
        if self.power_checker.is_positiv_and_even():
            text = f"{self.power_checker._number} is positive and even"
        else:
            text = f"{self.power_checker._number} is not positive and even"
        self.anwer_is_positive_and_even = Label(self.frame_info, text=text)
        self.anwer_is_positive_and_even.pack(side=TOP)


def set_up_power_of(root: Frame, callback: Callable):
    for widget in root.winfo_children():
        widget.pack_forget()
    App(root)
    Button(root, text="Back", command=callback).pack(side=BOTTOM)


if __name__ == "__main__":
    root = Tk()
    frame = Frame(root)
    frame.pack()
    app = App(frame)
    app.mainloop()

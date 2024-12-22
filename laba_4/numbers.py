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


class NaturalNumber(object):  # pylint: disable=useless-object-inheritance
    def __init__(self, number: int) -> None:
        if number < 0:
            raise ValueError("NaturalNumber must be greate or equal zero")
        self.number: int = number

    def calc_gcd(self, other: "NaturalNumber") -> int:
        a = self.number
        b = other.number
        while a and b:
            if a > b:
                a = a % b
            else:
                b = b % a
        return max(a, b)

    def calc_lcm(self, other: "NaturalNumber") -> int:
        gcd_value = self.calc_gcd(other)
        if gcd_value == 0:
            return 0
        return (self.number * other.number) // gcd_value

    def calc_prime_numbers(self, limit: "NaturalNumber") -> list[int]:
        _limit = max(limit.number, self.number)
        if _limit < 2:
            return []

        is_prime = [True] * (_limit + 1)
        is_prime[0], is_prime[1] = (False, False)

        for number in range(2, int(_limit**0.5) + 1):
            if is_prime[number]:
                for multiple in range(number * number, _limit + 1, number):
                    is_prime[multiple] = False

        prime_numbers = [num for num, prime in enumerate(is_prime) if prime]
        return prime_numbers


def set_up_menu(frame: Frame):  # pylint: disable=[too-many-locals, R0915]
    first_num: NaturalNumber | None = None
    second_num: NaturalNumber | None = None

    def creade_objects():
        nonlocal first_num, second_num
        a = int(entry_first_number.get())
        b = int(entry_secont_number.get())
        first_num = NaturalNumber(a)
        second_num = NaturalNumber(b)

    def delete_objects():
        nonlocal first_num, second_num
        entry_first_number.set("")
        entry_secont_number.set("")
        first_num = None
        second_num = None
        lable_gcd.configure(text=text_gcd)
        lable_lcm.configure(text=text_lcm)
        lable_prime_numbers.configure(text=text_prime_nums)

    def calc_gcd():
        nonlocal first_num, second_num
        if first_num is None or second_num is None:
            return
        gcd = first_num.calc_gcd(second_num)
        lable_gcd.configure(text=f"{text_gcd}{gcd}")

    def calc_lcm():
        nonlocal first_num, second_num
        if first_num is None or second_num is None:
            return
        lcm = first_num.calc_lcm(second_num)
        lable_lcm.configure(text=f"{text_lcm}{lcm}")

    def calc_prime_numbers():
        nonlocal first_num, second_num
        if first_num is None or second_num is None:
            return
        primes = first_num.calc_prime_numbers(second_num)
        primes = str(primes)[1:-1]
        lable_prime_numbers.configure(text=f"{text_prime_nums}{primes}")

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
        ("Create objects", creade_objects),
        ("Delete objects", delete_objects),
        ("Calc GCD", calc_gcd),
        ("Calc LCM", calc_lcm),
        ("Calc prime numbers in range", calc_prime_numbers),
    )

    for text, command in buttons:
        button = Button(frame_buttons, text=text, command=command, width=20)
        button.pack()

    text_gcd = "GCD: "
    text_lcm = "LCM: "
    text_prime_nums = "Prime numbers: "

    lable_gcd = Label(frame_info, text=text_gcd, width=20)
    lable_gcd.pack(anchor="w")

    lable_lcm = Label(frame_info, text=text_lcm, width=20)
    lable_lcm.pack(anchor="w")

    lable_prime_numbers = Label(frame_info, text=text_prime_nums)
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

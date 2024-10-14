from tkinter import BOTTOM
from tkinter import LEFT
from tkinter import RIGHT
from tkinter import TOP
from tkinter import StringVar
from tkinter import Tk
from tkinter.ttk import Frame
from tkinter.ttk import LabelFrame
from typing import Callable

from sqlalchemy import Select
from sqlalchemy.orm import Session

from laba_3.models import BankAccount
from laba_3.models import engine
from tkinter_extended.focus_sensitive_elems import Button
from tkinter_extended.focus_sensitive_elems import Radiobutton
from tkinter_extended.labeled_entry import LabeledEntryField


class BankInterface:
    def __init__(self, frame: Frame) -> None:
        self.wndow = frame

        self.wndow.winfo_toplevel().title("Bank")
        self.show_greeting()

    def mainloop(self):
        self.wndow.mainloop()

    def show_greeting(self):
        self.greeting_frame = LabelFrame(
            self.wndow, text="Welcome to the Bank"
        )

        self.sign_up_button = Button(
            self.greeting_frame, text="Sign Up", command=self.show_sign_up_menu
        )
        self.sign_up_button.pack(side=LEFT)

        self.log_in_button = Button(
            self.greeting_frame, text="Log In", command=self.show_log_in_menu
        )
        self.log_in_button.pack(side=LEFT)

        self.quit_button = Button(
            self.greeting_frame, text="Quit", command=self.greeting_frame.quit
        )
        self.quit_button.pack(side=RIGHT)

        self.greeting_frame.pack(padx=10, pady=10)

    def show_sign_up_menu(self):
        self.greeting_frame.forget()
        self.sign_up_frame = LabelFrame(self.wndow, text="Welcome, New User")

        self.card_number = LabeledEntryField(
            self.sign_up_frame,
            label_text="Card Number",
            entry_width=20,
            placeholder="xxxx-xxxx-xxxx-xxxx",
        )
        self.card_password = LabeledEntryField(
            self.sign_up_frame,
            label_text="Password",
            entry_width=20,
            placeholder="xxxx",
        )
        self.bank_name = LabeledEntryField(
            self.sign_up_frame, label_text="Bank Name", entry_width=20
        )
        self.full_name = LabeledEntryField(
            self.sign_up_frame, label_text="Full Name", entry_width=20
        )
        self.balance = LabeledEntryField(
            self.sign_up_frame,
            label_text="Balance",
            entry_width=20,
            placeholder="0",
        )

        submit_button = Button(
            self.sign_up_frame, text="Submit", command=self.sign_up
        )
        submit_button.pack(side=TOP)

        back_button = Button(
            self.sign_up_frame,
            text="Back",
            command=lambda: (
                self.sign_up_frame.pack_forget(),
                self.show_greeting(),
            ),
        )
        back_button.pack(side=BOTTOM)

        self.sign_up_frame.pack(padx=10, pady=10)

    def show_log_in_menu(self):
        self.log_in_frame = LabelFrame(self.wndow, text="Welcome, Old User")
        self.greeting_frame.forget()

        self.card_number = LabeledEntryField(
            self.log_in_frame,
            label_text="Card Number",
            entry_width=20,
            placeholder="xxxx-xxxx-xxxx-xxxx",
        )
        self.card_password = LabeledEntryField(
            self.log_in_frame,
            label_text="Password",
            entry_width=20,
            placeholder="xxxx",
        )

        submit_button = Button(
            self.log_in_frame, text="Submit", command=self.log_in
        )
        submit_button.pack(side=TOP)

        back_button = Button(
            self.log_in_frame,
            text="Back",
            command=lambda: (
                self.log_in_frame.pack_forget(),
                self.show_greeting(),
            ),
        )
        back_button.pack(side=BOTTOM)

        self.log_in_frame.pack(padx=10, pady=10)

    def log_in(self):
        password = int(self.card_password.get())
        card_number = self.card_number.get()
        if not BankAccount.is_exist(card_number, password):
            return
        self.user = BankAccount.get_if_exist(card_number, password)
        self.log_in_frame.forget()
        self.show_manage_menu()

    def sign_up(self):
        self.user = BankAccount()
        self.user.card_number = self.card_number.get()
        self.user.password = int(self.card_password.get())
        self.user.bank_name = self.bank_name.get()
        self.user.full_name = self.full_name.get()
        self.user.balance = int(self.balance.get().replace(" ", "") or 0)
        self.user.save()

        self.user = BankAccount.get_if_exist(
            self.card_number.get(), int(self.card_password.get())
        )
        self.sign_up_frame.forget()
        self.show_manage_menu()

    def show_manage_menu(self):
        self.manage_menu_frame = LabelFrame(self.wndow, text="Manage Account")
        self.details_frame = Frame(self.manage_menu_frame)

        self.card_number = LabeledEntryField(
            self.details_frame,
            label_text="Card Number",
            entry_width=20,
            placeholder=self.user.card_number,
        )
        self.bank_name = LabeledEntryField(
            self.details_frame,
            label_text="Bank Name",
            entry_width=20,
            placeholder=self.user.bank_name,
        )
        self.full_name = LabeledEntryField(
            self.details_frame,
            label_text="Full Name",
            entry_width=20,
            placeholder=self.user.full_name,
        )
        self.balance = LabeledEntryField(
            self.details_frame,
            label_text="Balance",
            entry_width=20,
            placeholder=str(self.user.balance),
        )

        self.details_frame.pack(side=TOP, padx=10)

        self.manage_menu_buttons_frame = Frame(self.manage_menu_frame)

        make_operation_button = Button(
            self.manage_menu_buttons_frame,
            text="Make Operation",
            command=self.make_operation,
        )
        make_operation_button.pack(side=LEFT, padx=5)

        log_out_button = Button(
            self.manage_menu_buttons_frame,
            text="Log Out",
            command=self.log_out,
        )
        log_out_button.pack(side=RIGHT, padx=5)

        self.manage_menu_buttons_frame.pack(side=BOTTOM, pady=10)

        self.operation_manage_frame = Frame(self.manage_menu_frame)
        self.operation_type = StringVar()
        self.operation_type.set("deposit")

        self.radio_buttons_frame = Frame(self.operation_manage_frame)
        radio_button_withdraw = Radiobutton(
            self.radio_buttons_frame,
            text="Withdraw",
            variable=self.operation_type,
            value="withdraw",
        )
        radio_button_withdraw.pack(padx=5, pady=5, side=LEFT)

        radio_button_deposit = Radiobutton(
            self.radio_buttons_frame,
            text="Deposit",
            variable=self.operation_type,
            value="deposit",
            state="",
        )
        radio_button_deposit.pack(padx=5, pady=5, side=RIGHT)
        self.operation_entry = LabeledEntryField(
            self.operation_manage_frame,
            label_text="Operation Amount",
            entry_width=17,
        )
        self.operation_entry.pack(padx=5, pady=5, side=TOP)

        self.radio_buttons_frame.pack(padx=5, pady=5, side=TOP)
        self.operation_manage_frame.pack(side=TOP)

        self.manage_menu_frame.pack(padx=10, pady=10)

    def log_out(self):
        self.manage_menu_frame.forget()
        self.show_greeting()

    def make_operation(self):
        selector = (
            Select(BankAccount)
            .where(BankAccount.card_number == self.user.card_number)
            .where(BankAccount.password == self.user.password)
        )

        amount = float(self.operation_entry.get().strip() or 0)
        if self.operation_type.get() == "withdraw":
            amount *= -1

        with Session(engine) as session:
            self.user = session.scalars(selector).one()
            self.user.balance += amount
            session.commit()
            self.user = session.scalars(selector).one()

        self.manage_menu_frame.pack_forget()
        self.show_manage_menu()


def set_up_bank(root: Frame, callback: Callable):
    for widget in root.winfo_children():
        widget.pack_forget()
    BankInterface(root)
    Button(root, text="Back", command=callback).pack(side=BOTTOM)


if __name__ == "__main__":
    root = Tk()
    frame = Frame(root)
    frame.pack()
    BankInterface(frame).mainloop()

import tkinter as tk
from typing import Optional

from translaters import NumTranslater

from tkinter_extended.basic_interface import BasicInterface
from tkinter_extended.placeholdered_entry import PlaceholderEntry


class NumTranslaterInterface(BasicInterface):
    translater: Optional[NumTranslater] = None

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("NumTranslaterInterface")

        self.entry: tk.Entry = PlaceholderEntry(
            self.root, placeholder="Insert decimal value"
        )
        self.entry.pack(padx=5, pady=5)

        self.info_frame = tk.Frame(self.root)
        self.button_frame = tk.Frame(self.root)
        self.info_frame.pack(padx=5, pady=5, side=tk.TOP, fill=tk.X)
        self.button_frame.pack(padx=5, pady=5, side=tk.BOTTOM, fill=tk.X)

        self.quit_button = tk.Button(
            self.button_frame, text="Close", command=self.root.quit
        )
        self.create_button = tk.Button(
            self.button_frame,
            text="Create Translater",
            command=self.add_translater,
        )
        self.delete_button = tk.Button(
            self.button_frame, text="Delete", command=self.del_translater
        )
        self.translate_button = tk.Button(
            self.button_frame, text="Translate", command=self.translate
        )

        self.show_elements((self.quit_button, self.create_button))

        self.translater: Optional[NumTranslater] = None

        self.root.mainloop()

    def add_translater(self) -> None:
        self.translater = NumTranslater()
        self.hide_elements(self.create_button)
        self.show_elements((self.delete_button, self.translate_button))

    def del_translater(self) -> None:
        self.entry.delete(0, tk.END)
        self.translater = None
        self.clear_frame(self.info_frame)
        self.hide_elements(
            (
                self.translate_button,
                self.delete_button,
                self.info_frame,
            )
        )
        self.show_elements(self.create_button)

    def is_valid(self) -> bool:
        value = self.entry.get()
        if value.isdigit():
            return True
        self.entry.delete(0, tk.END)
        self.entry.insert(0, "Invalid entry! Please enter a number.")
        return False

    def translate(self) -> None:
        if not self.is_valid() or self.translater is None:
            return
        self.show_elements(self.info_frame, side=tk.TOP)
        dec_val = self.entry.get()
        self.translater.set_num(dec_val)

        _hex = self.translater.hex()
        hex_label = tk.Label(self.info_frame, text=f"hex: {dec_val} -> {_hex}")
        _bin = self.translater.bin()
        bin_label = tk.Label(self.info_frame, text=f"bin: {dec_val} -> {_bin}")
        self.show_elements((bin_label, hex_label), side=tk.TOP)

        self.hide_elements(self.translate_button)


if __name__ == "__main__":
    NumTranslaterInterface()

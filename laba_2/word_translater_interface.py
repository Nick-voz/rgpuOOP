import tkinter as tk
from tkinter.ttk import Frame
from typing import Callable

from laba_2.translaters import WordTranslater
from tkinter_extended.basic_interface import BasicInterface
from tkinter_extended.focus_sensitive_elems import Button
from tkinter_extended.placeholdered_entry import PlaceholderEntry


class WordTranslaterInterface(BasicInterface):
    translater: WordTranslater | None = None

    def __init__(self, root: Frame):
        self.root = root
        self.root.winfo_toplevel().title("WordTranslaterInterface")

        self.entry = PlaceholderEntry(self.root, "insert word")
        self.entry.pack(padx=10, pady=10)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(padx=10, pady=10)

        self.quit_button = tk.Button(
            self.button_frame, text="Close", command=self.root.quit
        )
        self.quit_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.create_button = tk.Button(
            self.button_frame,
            text="create translatery",
            command=self.add_translater,
        )

        self.delete_button = tk.Button(
            self.button_frame, text="delet", command=self.del_translater
        )

        self.translate_button = tk.Button(
            self.button_frame, text="translate", command=self.translate
        )

        self.show_elements(self.create_button)

    def mainloop(self):
        self.root.mainloop()

    def add_translater(self) -> None:
        self.translater = WordTranslater()
        self.hide_elements(self.create_button)
        self.show_elements((self.translate_button, self.delete_button))

    def del_translater(self) -> None:
        self.entry.delete(0, tk.END)
        self.translater = None
        self.hide_elements((self.translate_button, self.delete_button))
        self.show_elements(self.create_button)

    def translate(self) -> None:
        if self.translater is None:
            return

        self.translater.set_word(self.entry.get())
        translation = self.translater.translate()
        self.entry.delete(0, tk.END)
        self.entry.insert(0, translation)


def set_up_word_translater(root: Frame, callback: Callable):
    for widget in root.winfo_children():
        widget.pack_forget()
    WordTranslaterInterface(root)
    Button(root, text="Back", command=callback).pack(side=tk.BOTTOM)


if __name__ == "__main__":
    root = tk.Tk()
    frame = Frame(root)
    frame.pack()
    WordTranslaterInterface(frame)
    root.mainloop()

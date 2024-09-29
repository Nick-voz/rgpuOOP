import tkinter as tk

from translaters import WordTranslater

from tkinter_extended.basic_interface import BasicInterface
from tkinter_extended.placeholdered_entry import PlaceholderEntry


class WordTranslaterInterface(BasicInterface):
    translater: WordTranslater | None = None

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("WordTranslaterInterface")

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


if __name__ == "__main__":
    WordTranslaterInterface()

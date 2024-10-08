import tkinter as tk
from typing import Optional


class PlaceholderEntry(tk.Entry):

    def __init__(
        self,
        master: Optional[tk.Widget] = None,
        placeholder: str = "PLACEHOLDER",
        color: str = "grey",
        *args,
        **kwargs,
    ):
        super().__init__(master, *args, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self["fg"]

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self) -> None:
        if not self.get():
            self.insert(0, self.placeholder)
            self["fg"] = self.placeholder_color

    def foc_in(self, *_: Optional[tk.Event]) -> None:
        if self["fg"] == self.placeholder_color:
            self.delete("0", "end")
            self["fg"] = self.default_fg_color

    def foc_out(self, *_: Optional[tk.Event]) -> None:
        if not self.get():
            self.put_placeholder()

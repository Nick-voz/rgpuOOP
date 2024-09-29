import tkinter as tk
from collections.abc import Iterable
from typing import Union


class BasicInterface:
    def hide_elements(
        self, widgets: Union[tk.Widget, Iterable[tk.Widget]]
    ) -> None:
        if isinstance(widgets, Iterable):
            for widget in widgets:
                widget.pack_forget()
        else:
            widgets.pack_forget()

    def show_elements(
        self,
        widgets: Union[tk.Widget, Iterable[tk.Widget]],
        side: str = tk.LEFT,
    ) -> None:
        if isinstance(widgets, Iterable):
            for widget in widgets:
                widget.pack(side=side, padx=5, pady=5)
        else:
            widgets.pack(side=side, padx=5, pady=5)

    def clear_frame(self, frame: tk.Frame) -> None:
        for widget in frame.winfo_children():
            widget.pack_forget()

from tkinter.ttk import Button as _Button
from tkinter.ttk import Radiobutton as _Radiobutton
from tkinter.ttk import Style


class Radiobutton(_Radiobutton):
    def __init__(self, master, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)

        self.bind("<FocusIn>", lambda _: self.on_focus())
        self.bind("<FocusOut>", lambda _: self.on_unfocus())

        self.style = Style()
        self.style.configure("Default.TRadiobutton")
        self.style.configure("Focused.TRadiobutton", foreground="green")

    def on_focus(self):
        self.configure(style="Focused.TRadiobutton")

    def on_unfocus(self):
        self.configure(style="Default.TRadiobutton")


class Button(_Button):
    def __init__(self, master, *args, **kwargs) -> None:
        # kwargs["width"] = kwargs.get("width", 8)
        super().__init__(master, *args, **kwargs)

        self.bind("<FocusIn>", lambda _: self.on_focus())
        self.bind("<FocusOut>", lambda _: self.on_unfocus())

        self.style = Style()
        self.style.configure("Default.TButton")
        self.style.configure("Focused.TButton", foreground="green")

    def on_focus(self):
        self.configure(style="Focused.TButton")

    def on_unfocus(self):
        self.configure(style="Default.TButton")

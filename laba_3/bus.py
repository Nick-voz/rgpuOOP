from tkinter import Canvas
from tkinter import Tk
from tkinter.constants import BOTTOM
from tkinter.constants import LEFT
from tkinter.constants import TOP
from tkinter.ttk import Frame
from tkinter.ttk import LabelFrame

from tkinter_extended.focus_sensitive_elems import Button
from tkinter_extended.labeled_entry import LabeledEntryField


class Bus:
    def __init__(self) -> None: ...

    def delete_bus(self): ...

    def create_bus(self): ...

    def to_start(self): ...

    def start_moving(self): ...

    def set_distance(self, distance: int): ...

    def set_speed(self, speed: int): ...


def set_up_menu():
    root = Tk()
    root.title("Bus")

    canvas = Canvas(root, width=600, height=100, bg="black")
    canvas.pack(side=BOTTOM)

    bus = Bus()

    frame_menu = Frame(root)
    frame_menu.pack(side=TOP)
    frame_menu_buttons = Frame(frame_menu)
    frame_menu_buttons.pack(side=TOP)

    buttons = (
        ("Create", lambda: bus.create_bus()),
        ("To start", lambda: bus.to_start()),
        ("Delete bus", lambda: bus.delete_bus()),
    )
    for text, command in buttons:
        b = Button(frame_menu_buttons, text=text, command=command)
        b.pack(side=LEFT, padx=5, pady=5)

    frame_moving = LabelFrame(frame_menu, text="Moving")
    frame_moving.pack(side=TOP, padx=10, pady=5)

    button_start_moving = Button(
        frame_moving, text="Start moving", command=lambda: bus.start_moving()
    )
    button_start_moving.pack(side=TOP)

    entry_distance = LabeledEntryField(
        frame_moving, label_text="Distance (0-500)", placeholder="500"
    )
    entry_distance.pack(side=TOP)

    entry_speed = LabeledEntryField(
        frame_moving, label_text="Speed (0-100)", placeholder="50"
    )
    entry_speed.pack(side=TOP)

    def set_bus_speed(bus: Bus):
        try:
            speed = int(entry_speed.get())
        except ValueError:
            return
        bus.set_speed(speed)

    def set_bus_distance(bus: Bus):
        try:
            distance = int(entry_speed.get())
        except ValueError:
            return
        bus.set_distance(distance)

    frame_moving.bind("<FocusOut>", lambda _: set_bus_speed(bus), add=True)
    frame_moving.bind("<FocusOut>", lambda _: set_bus_distance(bus), add=True)

    return root


if __name__ == "__main__":
    root = set_up_menu()
    root.mainloop()

import os
from tkinter import Canvas
from tkinter import Tk
from tkinter.constants import BOTTOM
from tkinter.constants import LEFT
from tkinter.constants import TOP
from tkinter.ttk import Frame
from tkinter.ttk import LabelFrame

import dotenv
from PIL import Image
from PIL import ImageTk

from tkinter_extended.focus_sensitive_elems import Button
from tkinter_extended.labeled_entry import LabeledEntryField
from tkinter_extended.utils import Point


class Bus:
    def __init__(self, canvas: Canvas, image_path: str) -> None:
        self._canvas = canvas
        self._distance = 500
        self._speed = 50
        self._image = self._load_image(image_path)

        self._draw_image(Point(50, 50))

    def delete_bus(self):
        pass

    def create_bus(self):
        pass

    def to_start(self):
        pass

    def start_moving(self):
        pass

    def set_distance(self, distance: int):
        try:
            self._distance = int(distance)
        except ValueError:
            pass

    def set_speed(self, speed: int):
        try:
            self._speed = int(speed)
        except ValueError:
            pass

    def _draw_image(self, root: Point):
        self._canvas.create_image(root.x, root.y, image=self._image)

    def _load_image(self, path: str) -> ImageTk.PhotoImage:
        image = Image.open(path)
        image = image.resize((75, 50))
        return ImageTk.PhotoImage(image)


def set_up_menu():
    root = Tk()
    root.title("Bus")

    canvas = Canvas(root, width=600, height=100, bg="black")
    canvas.pack(side=BOTTOM)

    dotenv.load_dotenv()
    if BUS_IMG_PATH := getenv("BUS_IMG_PATH"):
        bus = Bus(canvas, image_path=BUS_IMG_PATH)
    else:
        print("courd nod get access to bus image file")
        return

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

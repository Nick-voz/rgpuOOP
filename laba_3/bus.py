from enum import Enum
from enum import auto
from os import getenv
from tkinter import Canvas
from tkinter import Tk
from tkinter.constants import BOTTOM
from tkinter.constants import LEFT
from tkinter.constants import NW
from tkinter.constants import TOP
from tkinter.ttk import Frame
from tkinter.ttk import LabelFrame
from typing import Tuple

import dotenv
from PIL import Image
from PIL import ImageTk

from tkinter_extended.focus_sensitive_elems import Button
from tkinter_extended.labeled_entry import LabeledEntryField
from tkinter_extended.utils import Point


class ImageOnCanvas:
    def __init__(
        self,
        canvas: Canvas,
        image_path: str,
        root: Point,
        size: Tuple[int, int] = (70, 50),
    ):
        self._canvas = canvas
        self._size = size
        self._image = self.__load_image(image_path)
        self._root = root

    def draw(self):
        self._img_id = self._canvas.create_image(
            self._root.x, self._root.y, image=self._image, anchor=NW
        )

    def move_on(self, delta_x: int, delta_y: int):
        delta_x, delta_y = self.__validate_cords(delta_x, delta_y)
        self._root.x += delta_x
        self._root.y += delta_y

    def move_to(self, point: Point):
        self._root = point

    def clear(self):
        self._canvas.delete(self._img_id)

    @staticmethod
    def __validate_cords(x, y) -> Tuple[int, int]:
        try:
            _x = int(x)
            _y = int(y)
        except ValueError as e:
            raise e
        return (_x, _y)

    def __load_image(self, path: str) -> ImageTk.PhotoImage:
        image = Image.open(path)
        image = image.resize((self._size[0], self._size[1]))
        return ImageTk.PhotoImage(image)


class State(Enum):
    moving = auto()
    created = auto()
    stoped = auto()


class Bus:
    def __init__(self, canvas: Canvas, image_path: str) -> None:
        self._canvas = canvas
        self._distance = 500
        self._speed = 50
        self._image = ImageOnCanvas(canvas, image_path, Point(0, 0), (70, 50))
        self.state = State.created

    def tmp(self):
        if self.state == State.stoped:
            self.state = State.moving
            return

        self._image.clear()
        self._image.move_on(5, 0)
        self._image.draw()
        self._canvas.after(50, self.tmp)

    def delete_bus(self):
        self._image.clear()

    def create_bus(self):
        self._image.draw()

    def to_start(self):
        self.state = State.stoped
        self._image.clear()
        self._image.move_to(Point(0, 0))
        self._image.draw()

    def start_moving(self):
        self.tmp()

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
    if root:
        root.mainloop()

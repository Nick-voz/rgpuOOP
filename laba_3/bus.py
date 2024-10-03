from enum import Enum
from enum import auto
from os import getenv
from tkinter import Canvas
from tkinter import Tk
from tkinter.constants import BOTTOM
from tkinter.constants import LEFT
from tkinter.constants import TOP
from tkinter.ttk import Frame
from tkinter.ttk import LabelFrame
from typing import Tuple

import dotenv

from tkinter_extended.focus_sensitive_elems import Button
from tkinter_extended.ImageOnCanvas import ImageOnCanvas
from tkinter_extended.labeled_entry import LabeledEntryField
from tkinter_extended.utils import Point


class State(Enum):
    moving = auto()
    created = auto()
    stoped = auto()
    deleted = auto()


class Bus:
    def __init__(
        self,
        canvas: Canvas,
        image_path: str,
        root: Point,
        img_size: Tuple[int, int] = (70, 50),
    ) -> None:
        self._canvas = canvas
        self._distance = 500
        self._speed = 5
        self.__start_point = root
        self.__size = img_size
        self._image = ImageOnCanvas(
            canvas,
            image_path,
            Point(self.__start_point.x, self.__start_point.y),
            self.__size,
        )
        self.state = State.created

    def moving_loop(self):
        if self.state == State.stoped:
            self.state = State.moving
            return

        if self.state == State.created:
            self.state = State.moving

        if self.state == State.deleted:
            return

        if self.__is_out_of_distance():
            self.state = State.stoped
            return

        self._image.clear()
        self._image.move_on(self._speed, 0)
        self._image.draw()
        self._canvas.after(50, self.moving_loop)

    def delete_bus(self):
        self.state = State.deleted
        self._image.move_to(self.__start_point)
        self._image.clear()

    def create_bus(self):
        if self.state == State.deleted:
            self.state = State.created

        if self.state != State.created:
            return
        self.state = State.created

        try:
            self._image.clear()
        except Exception:
            pass

        self._image.draw()

    def to_start(self):
        # self.state = State.stoped
        self._image.clear()
        self._image.move_to(self.__start_point)
        self._image.draw()

    def set_distance(self, distance: int):
        try:
            distance = int(distance)
        except ValueError:
            pass
        self._distance = distance

    def set_speed(self, speed: int):
        try:
            speed = int(speed / 10)
        except ValueError:
            pass
        self._speed = speed

    def __is_out_of_distance(self) -> bool:
        return (
            self._image._root.x + self.__size[0] + self._speed
            >= self._distance + self.__start_point.x
        )


def draw_number_line(canvas: Canvas, width, height):
    canvas.create_line(0, height // 2, width, height // 2, fill="white")

    for i in range(0, width + 1):
        x = 10 + i * (width) / width
        if i % 50 == 0:
            canvas.create_line(
                x, height // 2 - 5, x, height // 2 + 5, fill="white"
            )
            canvas.create_text(x, height // 2 + 15, text=str(i), fill="white")
        elif i % 10 == 0:

            canvas.create_line(
                x, height // 2 - 3, x, height // 2 + 3, fill="white"
            )


def set_up_menu():
    root = Tk()
    root.title("Bus")

    width = 600
    height = 200
    canvas = Canvas(root, width=width, height=height, bg="black")
    canvas.pack(side=BOTTOM)

    draw_number_line(canvas, width, height)

    dotenv.load_dotenv()
    if BUS_IMG_PATH := getenv("BUS_IMG_PATH"):
        bus = Bus(canvas, image_path=BUS_IMG_PATH, root=Point(10, 50))
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
        frame_moving, text="Start moving", command=lambda: bus.moving_loop()
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
            distance = int(entry_distance.get())
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

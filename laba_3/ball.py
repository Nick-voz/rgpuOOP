import enum
from tkinter import LEFT
from tkinter import Tk
from tkinter.constants import TOP
from tkinter.ttk import Frame
from typing import Optional

from tkinter_extended.canvas import Canvas
from tkinter_extended.focus_sensitive_elems import Button
from tkinter_extended.labeled_entry import LabeledEntryField
from tkinter_extended.utils import Point


class Side(enum.Enum):
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    TOP = (0, -1)
    BOTTOM = (0, 1)


class BallOnString:
    CENTER_RADIUS = 10

    def __init__(
        self,
        canvas: Canvas,
        center: Point,
        radius: int = 50,
        step: int = 10,
        side: Side = Side.RIGHT,
        ball_radius: int = 10,
        speed: int = 10,
    ):
        self.canvas = canvas
        self.center = center
        self.radius = radius
        self.ball_radius = ball_radius
        self.step = step
        self.speed = speed
        self.side = side

        self.ball_center = Point(
            self.center.x,
            self.center.y,
        )

        self.border: Optional["Point"] = None

        self.__draw()
        self.times = 0
        self.__continue = True

    def set_times(self, times: int):
        self.times = times

    def move(self):
        """Initial the movement loop"""
        if self.__continue is False:
            self.__continue = True
            return

        self.__clear_moving_elements()
        self.__calculate_movement()
        self.__draw_ball()
        self.canvas.after(self.speed, self.move)

    def __draw(self):
        """draw the ball, the center and line"""
        self.__draw_center()
        self.__draw_ball()

    def __calculate_movement(self):
        """Update The ball position based on its distance from the center or border"""

        if (
            bool(self.times) is False
            and self.border is None
            and self.ball_center.dist(self.center) == 0
        ):
            self.__continue = False
            return

        if self.border is None and self.ball_center.dist(self.center) != 0:
            self.__move_to_point(self.center)
            return

        elif self.border is None:
            self.__calculate_border_point()
            self.times -= 1
            return

        self.__move_to_point(self.border)

    def __calculate_border_point(self):
        self.border = Point(
            self.center.x + self.radius * self.side.value[0],
            self.center.y + self.radius * self.side.value[1],
        )

    def __move_to_point(self, point: Point):
        dx, dy = self.ball_center.decriment_move(point)

        if abs(dx) <= self.step and abs(dy) <= self.step:
            self.ball_center = Point(point.x, point.y)
            self.border = None
            return

        dx = self.step if dx > 0 else -self.step if dx != 0 else 0
        dy = self.step if dy > 0 else -self.step if dy != 0 else 0

        self.ball_center.x += int(dx)
        self.ball_center.y += int(dy)

    def __clear_moving_elements(self):
        if self.__ball_id:
            self.canvas.delete(self.__ball_id)
        if self.__line_id:
            self.canvas.delete(self.__line_id)

    def __draw_ball(self):
        self.__ball_id = self.canvas.create_circle(
            self.ball_center,
            self.ball_radius,
            fill="red",
        )

        self.__line_id = self.canvas.create_line(
            self.center.x,
            self.center.y,
            self.ball_center.x,
            self.ball_center.y,
            fill="white",
        )

    def __draw_center(self):
        self.__center_id = self.canvas.create_circle(
            self.center,
            self.CENTER_RADIUS,
            fill="blue",
        )

    def clear(self):
        """clear all drawn elements from canvas."""
        self.canvas.delete(self.__center_id, self.__ball_id, self.__line_id)

    def set_side(self, side: Side):
        if not isinstance(side, Side):
            raise AttributeError("side mast be instanc of Side")
        self.side = side


def setup():
    root = Tk()
    root.title("Ball")

    frame_menu = Frame(root)
    frame_menu.pack(side=TOP)

    canvas = Canvas(root, height=400, bg="black")
    canvas.pack(fill="x")

    ball = BallOnString(
        canvas=canvas,
        center=Point(150, 150),
        radius=150,
        ball_radius=25,
        speed=1,
        step=1,
    )

    def set_times():
        ball.set_times(int(times_entry.get()))

    button_move = Button(
        frame_menu,
        text="start moving",
        command=lambda: (set_times(), ball.move()),
    )

    button_move.pack(side=TOP)

    times_entry = LabeledEntryField(
        frame_menu, label_text="Times", entry_width=5
    )
    times_entry.pack(side=TOP, fill="none")

    side_buttons = (
        ("Left", lambda: ball.set_side(Side.LEFT)),
        ("Top", lambda: ball.set_side(Side.TOP)),
        ("Bottom", lambda: ball.set_side(Side.BOTTOM)),
        ("Right", lambda: ball.set_side(Side.RIGHT)),
    )
    for text, command in side_buttons:
        button = Button(frame_menu, text=text, command=command)
        button.pack(side=LEFT)

    root.bind("<Up>", lambda _: ball.set_side(Side.TOP))
    root.bind("<Down>", lambda _: ball.set_side(Side.BOTTOM))
    root.bind("<Left>", lambda _: ball.set_side(Side.LEFT))
    root.bind("<Right>", lambda _: ball.set_side(Side.RIGHT))

    return root


if __name__ == "__main__":
    app = setup()
    app.mainloop()

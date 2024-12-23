from collections.abc import Callable
from random import randint
from tkinter import BOTTOM
from tkinter import LEFT
from tkinter import TOP
from tkinter import Tk
from tkinter.ttk import Button
from tkinter.ttk import Frame
from tkinter.ttk import Label

from tkinter_extended.canvas import Canvas
from tkinter_extended.canvas import Point
from tkinter_extended.labeled_entry import LabeledEntryField
from tkinter_extended.set_up_util import clear_frame

COLORS = [
    "red",
    "green",
    "blue",
    "yellow",
    "cyan",
    "magenta",
    "black",
    "white",
    "gray",
    "orange",
    "purple",
    "brown",
    "pink",
]


class Ball:
    def __init__(
        self,
        canvas: Canvas,
        right_bottom_border: Point,
        ball_center: Point = Point(150, 150),
        ball_radius: int = 25,
    ) -> None:
        self.canvas = canvas
        self.right_bottom_border = right_bottom_border
        self.ball_center = ball_center
        self.ball_radius = ball_radius
        self._ball_id: int | None = None
        self.color = "white"
        self._change_direction_timer = -1
        self.step = 10
        self.sleep_time = 50
        self.update_direction()
        self.draw()

    def draw(self) -> None:
        if self._ball_id is not None:
            return

        self._ball_id = self.canvas.create_circle(
            self.ball_center, self.ball_radius, fill=self.color
        )

    def delete(self) -> None:
        if self._ball_id is None:
            return
        self.canvas.delete(self._ball_id)
        self._ball_id = None

    def is_in_borders(self, point: Point) -> bool:
        in_ox = point.x >= 0 and point.x <= self.right_bottom_border.x
        in_oy = point.y >= 0 and point.y <= self.right_bottom_border.y
        return in_ox and in_oy

    def animate_move(self, dx: int, dy: int) -> None:
        new_cords = Point(self.ball_center.x + dx, self.ball_center.y + dy)
        if not self.is_in_borders(new_cords):
            self.update_direction()
            return

        self.delete()
        self.ball_center = new_cords
        self.draw()

    def update_direction(self):
        self.direction = randint(-100, 100) / 100, randint(-100, 100) / 100

    def contor_direction(self):
        if self._change_direction_timer <= 100:
            self._change_direction_timer += randint(0, 10)
            return

        self.update_direction()
        self._change_direction_timer = 0

    def random_move(self):
        self.contor_direction()
        dx = self.step * self.direction[0]
        dy = self.step * self.direction[1]
        self.animate_move(int(dx), int(dy))

    def moving_loop(self):
        self.random_move()
        self.canvas.after(self.sleep_time, self.moving_loop)

    def has_collision(self, other: "Ball") -> bool:
        dist = self.ball_center.dist(other.ball_center)
        radius_sum = self.ball_radius + other.ball_radius
        return dist <= radius_sum

    def random_color(self):
        self.color = COLORS[randint(0, len(COLORS) - 1)]


def set_up_menu(frame: Frame):
    menu_frame = Frame(frame)
    menu_frame.pack(side=TOP)
    collisions = 0

    def collision_control(balls: list["Ball"]):
        nonlocal collisions
        for i in range(len(balls)):
            for k in range(i, len(balls)):
                left_ball = balls[i]
                right_ball = balls[k]
                if left_ball is right_ball:
                    continue
                if left_ball.has_collision(right_ball):
                    right_ball.random_color()
                    collisions += 1
        update_colisions_label()
        canvas.after(400, lambda: collision_control(balls))

    def start():
        ball = Ball(canvas, Point(160, 200))
        ball_2 = Ball(canvas, Point(160, 200))
        ball.moving_loop()
        ball_2.moving_loop()
        collision_control([ball, ball_2])

    def update_colisions_label():
        hits_label.configure(text=f"Hits: {collisions}")

    start_buttn = Button(menu_frame, text="Start", command=start)
    start_buttn.pack(side=LEFT)

    interval_entry = LabeledEntryField(
        menu_frame, label_text="Timers's interval:", placeholder="10"
    )
    interval_entry.pack(side=LEFT)

    hits_label = Label(menu_frame, text="Hits: 0")
    hits_label.pack(side=LEFT)

    canvas = Canvas(frame, width=450, height=300, bg="black")
    canvas.pack(side=TOP)


def set_up_balls(root: Frame, callback: Callable):
    clear_frame(root)
    frame = Frame(root)
    frame.pack()
    set_up_menu(frame)
    Button(root, text="Back", command=callback).pack(side=BOTTOM)


if __name__ == "__main__":
    root = Tk()
    frame = Frame(root)
    frame.pack()
    set_up_menu(frame)
    root.mainloop()

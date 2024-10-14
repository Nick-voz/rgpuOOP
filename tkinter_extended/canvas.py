from tkinter import Canvas as _Canvas

from .utils import Point


class Canvas(_Canvas):
    def create_circle(self, root: Point, r: float, *args, **kwargs) -> int:
        delta = int(r / 2)
        return self.create_oval(
            root.x - delta,
            root.y - delta,
            root.x + delta,
            root.y + delta,
            *args,
            **kwargs
        )

from tkinter import Canvas
from tkinter.constants import NW
from typing import Tuple

from PIL import Image
from PIL import ImageTk

from .utils import Point


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
        self._root.x = point.x
        self._root.y = point.y

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

from math import dist

from typing_extensions import Tuple


class Point:
    def __init__(self, x: int, y: int):
        self.x = int(x)
        self.y = int(y)

    def cords(self) -> Tuple[int, int]:
        return (self.x, self.y)

    def dist(self, other: "Point") -> float:
        return dist(self.cords(), other.cords())

    def decriment_move(self, other: "Point") -> Tuple[float, float]:
        dif_x = self.x - other.x
        dif_y = self.y - other.y
        delta_x = -(abs(dif_x)) if self.x >= other.x else abs(dif_x)
        delta_y = -(abs(dif_y)) if self.y >= other.y else abs(dif_y)
        return delta_x, delta_y

    def __str__(self) -> str:
        return f"{self.x=} {self.y=}"


if __name__ == "__main__":
    points = [
        Point(0, 0),
        Point(0, 5),
        Point(5, 0),
        Point(-5, 0),
        Point(0, -5),
        Point(-5, -5),
    ]
    a = Point(0, 0)
    a.x = 10
    assert a.cords() == (10, 0)
    print(".cords() warcks successfully")
    b = [dist(Point(0, 0).cords(), i.cords()) for i in points]
    assert b == [0.0, 5.0, 5.0, 5.0, 5.0, 7.0710678118654755]
    print(".dist worsk successfully ")

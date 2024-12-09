from enum import Enum
from math import dist
from typing_extensions import Tuple


class Side(Enum):
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    TOP = (0, -1)
    BOTTOM = (0, 1)


class Point:
    """
    A class to represent a point in a 2D Cartesian coordinate system.

    Attributes:
    ----------
    x : int
    y : int

    Methods:
    -------
    cords() -> Tuple[int, int]:
        Returns the coordinates of the point as a tuple (x, y).

    dist(other: Point) -> float:
        Calculates the distance from this point to another Point object.

    decriment_move(other: Point) -> Tuple[float, float]:
        Determines the directional change in x and y coordinates to "move"
        towards the other point.
    """

    def __init__(self, x: int, y: int):
        """
        Initializes a Point instance with specified coordinates.

        Parameters:
        ----------
        x : int
            The x-coordinate of the point.
        y : int
            The y-coordinate of the point.

        The coordinates are converted to integers to ensure that Point
        instances always represent integer-based coordinates.
        """
        self.x = int(x)
        self.y = int(y)

    def cords(self) -> Tuple[int, int]:
        """
        Returns the coordinates of the point.

        Returns:
        -------
        Tuple[int, int]
            A tuple "(x, y)" containing the x and y coordinates of the point.
        """
        return (self.x, self.y)

    def dist(self, other: "Point") -> float:
        """
        Calculates the Euclidean distance between this point and another Point.
        Parameters:
        ----------
        other : Point
            The other point to which the distance will be calculated.
        Returns:
        -------
        float
            The Euclidean distance between this point and the 'other' point.
        """
        return dist(self.cords(), other.cords())

    def decriment_move(self, other: "Point") -> Tuple[float, float]:
        """
        Computes the directional change needed to move from this point
        towards another point.

        This method considers the difference in x and y coordinates and
        determines how much to increment or decrement each coordinate to
        align with the other point. The movement is determined based on
        the relative positions of the two points.

        Parameters:
        ----------
        other : Point
            The target point to which movement is calculated.

        Returns:
        -------
        Tuple[float, float]
            A tuple (delta_x, delta_y) representing the change in
            x and y coordinates, that needed to move from self point to other
        """
        dif_x = self.x - other.x
        dif_y = self.y - other.y
        delta_x = -(abs(dif_x)) if self.x >= other.x else abs(dif_x)
        delta_y = -(abs(dif_y)) if self.y >= other.y else abs(dif_y)
        return delta_x, delta_y

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

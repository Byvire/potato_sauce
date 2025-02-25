#!/usr/bin/env python3
from __future__ import annotations

import collections
import dataclasses
import math
import sys
from typing import NamedTuple, Optional
import typing

from potato_sauce.proto import geom_pb2


_BIG_NUMBER = 10000  # for cheating math. If things go funky try making this bigger.


class Point(NamedTuple("Point", [("x", float), ("y", float)])):
    """A point in 2d space.

    Attributes:
      x: x coordinate
      y: y coordinate
    """
    # We have to use the function-call variant of NamedTuple because the normal
    # way isn't compatible with @typing.overload.

    def __add__(self, other: Vector) -> Point:
        if isinstance(other, Vector):
            return other.__add__(self)
        raise TypeError(f"Added {type(other)} to a Point")


    @typing.overload
    def __sub__(self, other: Point) -> Vector:
        ...

    @typing.overload
    def __sub__(self, other: Vector) -> Point:
        ...

    def __sub__(self, other):
        if isinstance(other, Point):
            return Vector(self.x - other.x, self.y - other.y)
        if isinstance(other, Vector):
            return Point(self.x - other.x, self.y - other.y)
        raise TypeError(f"Subtracted point {type(other)} from a Point")


class Vector(NamedTuple("Vector", [("x", float), ("y", float)])):

    @typing.overload
    def __add__(self, other: Point) -> Point:
        ...

    @typing.overload
    def __add__(self, other: Vector) -> Vector:
        ...

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        raise TypeError(f"Added {type(other)} to a Point")

    def __sub__(self, other: Vector) -> Vector:
        return self + other.scale(-1)

    def scale(self, number: float) -> Vector:
        return Vector(number * self.x, number * self.y)

    def orthonormal_vector(self) -> Vector:
        """Returns a unit-length vector pointing 90 degrees clockwise from this vector.

        Or, if this is the zero vector, this returns the zero vector.
        """
        if self.x == self.y == 0:
            return self
        return Vector(self.y, -self.x).make_unit_length()

    def magnitude(self) -> float:
        return (self.x**2 + self.y**2)**0.5

    def magnitude_squared(self) -> float:
        """More numerically stable than squaring self.magnitude()."""
        return self.x**2 + self.y**2

    def make_unit_length(self) -> Vector:
        magnitude = self.magnitude()
        if self.magnitude == 0:
            raise ValueError("Attempted to shorten the zero vector to unit length")
        result = Vector(self.x / magnitude, self.y / magnitude)
        assert 0.99 < result.magnitude() < 1.01
        return result

    def dot(self, other: Vector) -> float:
        return self.x * other.x + self.y * other.y

    def project_onto(self, other: Vector) -> Vector:
        return other.scale(self.dot(other) / other.magnitude()**2)

    @staticmethod
    def unit_from_direction(enum_val: geom_pb2.Direction) -> Vector:
        """Returns a unit-size vector in the indicated direction.

        Raises value error given DIRECTION_UNKNOWN. The caller must decide how
        to handle that case.
        """
        if enum_val == geom_pb2.DIRECTION_DOWN:
            return Vector(0, -1)
        if enum_val == geom_pb2.DIRECTION_UP:
            return Vector(0, 1)
        if enum_val == geom_pb2.DIRECTION_LEFT:
            return Vector(-1, 0)
        if enum_val == geom_pb2.DIRECTION_RIGHT:
            return Vector(1, 0)
        raise ValueError(f"Can't make vector for direction {enum_val}")


def ccw(a: Point, b: Point, c: Point) -> int:
    """Orientation of points a, b, and c (order matters).

    "ccw" is short for "counterclockwise".

    Returns:
      0 if colinear; 1 if counterclockwise; -1 if clockwise. (Assuming we're in
      a normal Cartesian layout. In practice this gives the wrong answer as far
      as down-is-positive computer graphic coordinates.)
    """
    magic = (c.y - b.y) * (b.x - a.x) - (b.y - a.y) * (c.x - b. x)
    if magic == 0: return 0
    if magic > 0: return 1
    return -1


def angle_from_origin_degrees(point: Point | Vector) -> float:
    """Returns the angle of the given point, relative to the origin and x axis.

    This is the angle by which the ray {(x, 0) : x >= 0} would need to be
    rotated counterclockwise around the origin to hit the given point. It's the
    standard way of doing angles you probably learned in school.

    Returns a number of degrees in the half-open range [0, 360).
    """
    point = Point(*point)
    if point.x == 0:
        if point.y == 0:
            print("Warning: Asked for angle from origin of point (0,0)", file=sys.stderr)
        return 270 if point.y < 0 else 90
    # Consider special-casing the y=0 case just to return an integer
    if point.x > 0:
        answer = math.atan(point.y / point.x) * 180 / math.pi
        if answer < 0:
            answer += 360
        return answer
    return 180 + math.atan(point.y / point.x) * 180 / math.pi


def angle_from_origin_radians(point: Point | Vector) -> float:
    # I don't think I need this, because pygame uses degrees.
    return math.pi / 180 * angle_from_origin_degrees(point)


def solve_quadratic(a: float, b: float, c: float) -> list[float]:
    """Solves the equation: a*x**2 + b*x + c = 0.

    As numerically stable as anything involving square roots can be.

    Returns:
      A list holding all real (float) solutions to the given quadratic equation.
      This has 0, 1 (unlikely), or 2 values.
    """
    det = b**2 - 4 * a * c
    if det < 0:
        return []
    if det == 0:
        return [- b / (2 * a)]
    return [(-b + det**0.5) / (2 * a), (-b - det**0.5) / (2 * a)]


def line_intersection(point0: Point,
                      vect0: Vector,
                      point1: Point,
                      vect1: Vector) -> Optional[Point]:
    """Finds the intersection of two lines if it exists uniquely.

    point0 and vect0 define the first line, and point1 and vect1 define the
    second line.

    Not numerically stable.
    """
    if vect0.x * vect1.y - vect0.y * vect1.x == 0:  # parallel vectors
        return None
    # Solve:  point0 + coeff0 * vect0 == point1 + coeff1 * vect1
    coeff0 = - ((point0.y - point1.y) * vect1.x - (point0.x - point1.x) * vect1.y
                ) / (vect0.y * vect1.x - vect0.x * vect1.y)
    return vect0.scale(coeff0) + point0


class Circle:
    def __init__(self, center: Point, radius: float):
        self._center = center
        self._radius = radius

    @property
    def center(self):
        return self._center

    @property
    def radius(self):
        return self._radius

    def __repr__(self) -> str:
        return f"Circle({self._center}, {self._radius}, {self._color})"


def circle_intersections(alice: Circle, bob: Circle) -> list[Point]:
    bob_to_alice = alice.center - bob.center
    if bob_to_alice.magnitude() == 0:
        # The circles have the same center. Note that we treat infinite
        # intersections as zero intersections. Which is not amazing.
        return []
    # elif bob.center.y == alice.center.y:
    #     x_coord = (bob_to_alice.magnitude_squared() - bob.radius**2 + alice.radius**2
    #                   ) / ( 2 * bob_to_alice.magnitude()) + alice.center.x
    #     y_vals = solve_quadratic(
    #         1, -2 * alice.center.y,
    #         alice.center.y**2 + (x_coord - alice.center.x) **2 - alice.radius**2)
    #     return [Point(x_coord, y_coord) for y_coord in y_vals]
    elif abs(bob.center.y - alice.center.y) < min(0.05, abs(bob.center.x - alice.center.x)):
        # The centers are horizontal, so the solutions lie on a vertical line.
        # To avoid divide-by-zero (for exact verticality) or
        # floating-point-related numerical instability, we flip the axes.
        transposed_result = circle_intersections(
            Circle(Point(alice.center.y, alice.center.x), alice.radius),
            Circle(Point(bob.center.y, bob.center.x), bob.radius))
        return [Point(pt.y, pt.x) for pt in transposed_result]
    # Finally the general case with 2 intersections. The centers' x and y
    # coordinates differ.
    # Solutions lie on a line defined by y = slope * x + y_int where
    slope = (alice.center.x - bob.center.x) / (bob.center.y - alice.center.y)
    y_int = (- alice.center.y**2 + bob.center.y**2
             - alice.center.x**2 + bob.center.x**2
             + alice.radius**2 - bob.radius**2) / (
                 2 * (bob.center.y - alice.center.y))
    x_vals = solve_quadratic(
        slope**2 + 1,
        2 * (slope * (y_int - alice.center.y) - alice.center.x),
        (y_int - alice.center.y) ** 2 + alice.center.x **2 - alice.radius**2)
    return [Point(x, slope * x + y_int) for x in x_vals]


def _bottom_left_or_center_to_bottom_left(
        width: float,
        height: float,
        bottom_left: Optional[Point],
        center: Optional[Point]) -> Point:
    if bottom_left is not None and center is not None:
        raise ValueError(
            "mutually exclusive center and bottom-left arguments were both provided")
    if bottom_left is None and center is None:
        raise ValueError("neither center not bottom-left argument was provided")
    if bottom_left is not None:
        return bottom_left
    return center - Vector(width / 2, height / 2)


class GridCoord(NamedTuple("GridCoord", [("x", int), ("y", int)])):
    """A coordinate in a grid (an integer grid of rectangles).

    Attributes:
      x: int, x coordinate.
      y: int, y coordinate. Usually by convention, positive y means up (toward
        the top of the screen).
    """

    def __add__(self, other: GridDisplacement) -> GridCoord:
        if isinstance(other, GridDisplacement):
            return GridCoord(self.x + other.x, self.y + other.y)
        raise TypeError(f"Unable to add {other} to a GridCoord")

    @typing.overload
    def __sub__(self, other: GridDisplacement) -> GridCoord:
        ...

    @typing.overload
    def __sub__(self, other: GridCoord) -> GridDisplacement:
        ...

    def __sub__(self, other):
        if isinstance(other, GridDisplacement):
            return GridCoord(self.x - other.x, self.y - other.y)
        if isinstance(other, GridCoord):
            return GridDisplacement(self.x - other.x, self.y - other.y)
        raise TypeError(f"Unable to subtract {other} from a GridCoord")

    @staticmethod
    def from_proto(proto: geom_pb2.GridCoord) -> GridCoord:
        return GridCoord(proto.x, proto.y)

    def to_proto(self) -> geom_pb2.GridCoord:
        return geom_pb2.GridCoord(x=self.x, y=self.y)


class GridDisplacement(NamedTuple("GridDisplacement", [("x", int), ("y", int)])):
    """A displacement measured in grid coordinates.

    GridDisplacement is to GridCoord as Vector is to Point.
    """

    @typing.overload
    def __add__(self, other: GridCoord) -> GridCoord:
        ...

    @typing.overload
    def __add__(self, other: GridDisplacement) -> GridDisplacement:
        ...

    def __add__(self, other):
        if isinstance(other, GridCoord):
            return GridCoord(other.x + self.x, other.y + self.y)
        if isinstance(other, GridDisplacement):
            return GridDisplacement(other.x + self.x, other.y + self.y)
        raise TypeError(f"Cannot add {other} to GridDisplacement")

    def __sub__(self, other: GridDisplacement) -> GridDisplacement:
        if isinstance(other, GridDisplacement):
            return GridDisplacement(self.x - other.x, self.y - other.y)
        raise TypeError(f"Cannot subtract {other} from GridDisplacement")


class Grid:
    """Maps a grid of integer coordinates to and from floating-point space.

    A "cell" in the grid (identified by a GridCoord) is identified with an
    axis-aligned rectangle in 2d space (ie probably the game map).

    The grid coordinate (0,0) might refer to a rectangular area near the bottom
    left of the map or screen.

    The grid only defines the mapping. It doesn't define bounds or keep track of
    game objects that use the layout.

    Grid layouts are common in video games. For example, objects in the 2D Zelda
    series are usually laid on a grid. This convention makes it easy for the
    user to understand the layout of a room, and allows for clean behavior in
    puzzles where you move objects around. Grid-aligned objects don't need to
    have uniform shapes and sizes. (E.g. buildings in the original Starcraft.)
    """

    def __init__(self,
                 cell_width: float,
                 cell_height: float,
                 bottom_left: Point) -> None:
        """Grid constructor. See class docstring.

        Args:
          cell_width: The width (x-direction) of one cell in the grid.
          cell_height: The height (y-direction) of one cell in the grid.
          bottom_left: The location of the bottom left of cell (0, 0). Note
            we're assuming y-is-up coordinates, not UI coordinates.
        """
        self._cell_width = cell_width
        self._cell_height = cell_height
        self._bottom_left = bottom_left

    @staticmethod
    def unit_grid() -> Grid:
        return Grid(1, 1, Point(0, 0))

    def cell_center(self, coord: GridCoord) -> Point:
        """Gets the location of the center of the given cell."""
        return (self.cell_bottom_left(coord)
                + Vector(0.5 * self._cell_width, 0.5 * self._cell_height))

    def cell_bottom_left(self, coord: GridCoord) -> Point:
        return self._bottom_left + Vector(coord.x * self._cell_width,
                                          coord.y * self._cell_height)

    def cell_top_right(self, coord: GridCoord) -> Point:
        return self.cell_bottom_left(coord + GridDisplacement(1, 1))

    @property
    def cell_width(self) -> float:
        return self._cell_width

    @property
    def cell_height(self) -> float:
        return self._cell_height

    def find_cell(self, point: Point) -> GridCoord:
        displacement: Vector = point - self._bottom_left
        return GridCoord(int(displacement.x / self._cell_width),
                         int(displacement.y / self._cell_height))

    def to_json_dict(self) -> dict:
        """Converts this grid to a dict that can be saved in a json map config."""
        return {
            "type": "grid",
            "cell_width": self.cell_width,
            "cell_height": self.cell_height,
            "bottom_left": list(self._bottom_left),
        }

    @staticmethod
    def from_json_dict(json_dict: dict) -> Grid:
        assert json_dict["type"] == "grid"
        return Grid(
            cell_width=json_dict["cell_width"],
            cell_height=json_dict["cell_height"],
            bottom_left=Point(*(int(x) for x in json_dict["bottom_left"])),
        )


def _grid_intervals_overlap(a_start: int, a_end: int,
                            b_start: int, b_end: int) -> bool:
    """Whether range(a_start, a_end + 1) overlaps range(b_start, b_end + 1)."""
    return a_start <= b_end and b_start <= a_end


def gridtangle_intersection(alice: Optional[Gridtangle],
                            bob: Optional[Gridtangle]) -> Optional[Gridtangle]:
    """Finds the intersection of two Gridtangles.

    In both input and output, None represents an empty Gridtangle.

    Prefer to use implicit boolean conversion to test if the return value is
    None, to be forward compatible with a patch that adds a proper empty
    gridtangle object.
    """
    if alice is None or bob is None:
        return None
    bottom_left = GridCoord(max(alice.bottom_left.x, bob.bottom_left.x),
                            max(alice.bottom_left.y, bob.bottom_left.y))
    top_right = GridCoord(min(alice.top_right.x, bob.top_right.x),
                          min(alice.top_right.y, bob.top_right.y))
    if bottom_left.x > top_right.x or bottom_left.y > top_right.y:
        return None
    return Gridtangle(bottom_left, top_right)


@dataclasses.dataclass(frozen=True)
class Gridtangle:
    """An axis-aligned rectangle defined by integer grid coordinates.

    Attributes:
      bottom_left: Bottom left cell location (inclusive).
      top_right: Top right cell location (inclusive). Note e.g. the width is
        top_right.x + 1 - bottom_left.x. So for a Gridtangle of area 1, the
        bottom_left and top_right should be equal.
    """

    bottom_left: GridCoord
    top_right: GridCoord

    def __post_init__(self):
        if (self.bottom_left.x > self.top_right.x or
            self.bottom_left.y > self.top_right.y):
            raise ValueError(
                f"Top right {self.top_right} of gridtangle is down/left of "
                f"bottom-left {self.bottom_left}")

    @staticmethod
    def with_size(bottom_left: GridCoord,
                  size: tuple[int, int]) -> Gridtangle:
        """Creates a Gridtangle at the given location with the given size.

        The size must be at least (1, 1).
        """
        return Gridtangle(
            bottom_left,
            bottom_left + GridDisplacement(size[0] - 1, size[1] - 1))

    def overlaps(self, other: Gridtangle) -> bool:
        """Do these two rectangles overlap?"""
        # Two rectangles overlap if their y-axis and x-axis projections both overlap.
        return gridtangle_intersection(self, other) is not None
        # return (
        #     _grid_intervals_overlap(
        #         self.bottom_left.x, self.top_right.x,
        #         other.bottom_left.x, other.top_right.x) and
        #     _grid_intervals_overlap(
        #         self.bottom_left.y, self.top_right.y,
        #         other.bottom_left.y, other.top_right.y))

    def displace(self, displacement: GridDisplacement) -> Gridtangle:
        return Gridtangle(
            self.bottom_left + displacement,
            self.top_right + displacement,
        )

    def width(self) -> int:
        return self.end.x - self.bottom_left.x
        # return 1 + self.top_right.x - self.bottom_left.x

    def height(self) -> int:
        # return 1 + self.top_right.y - self.bottom_left.y
        return self.end.y - self.bottom_left.y

    def area(self) -> int:
        return self.width() * self.height()

    @property
    def end(self) -> GridCoord:
        """Top-right cell plus (1, 1), for when you want an open-ended range."""
        return self.top_right + GridDisplacement(1, 1)

    def contains_coord(self, coord: GridCoord) -> bool:
        return (self.bottom_left.x <= coord.x <= self.top_right.x
                and self.bottom_left.y <= coord.y <= self.top_right.y)

    def contains_rect(self, rect: Gridtangle) -> bool:
        """True if rect is completely contained within self."""
        return (self.bottom_left.x <= rect.bottom_left.x
                and self.bottom_left.y <= rect.bottom_left.y
                and self.top_right.x >= rect.top_right.x
                and self.top_right.y >= rect.top_right.y)

    def touches_rect(self,
                     rect: Gridtangle,
                     diagonal_counts=False) -> bool:
        """True if the given rect is overlapping or snugly adjacent to self.

        By default, a diagonal adjacency between just the corners of the
        rectangle doesn't count... since it's the weakest form of adjacency.
        """
        if diagonal_counts:
            return Gridtangle(self.bottom_left - GridDisplacement(1, 1),
                              self.top_right + GridDisplacement(1, 1)
                              ).overlaps(rect)
        else:
            return (Gridtangle(
                self.bottom_left - GridDisplacement(1, 0),
                self.top_right + GridDisplacement(1, 0)).overlaps(rect)
                    or Gridtangle(
                        self.bottom_left - GridDisplacement(0, 1),
                self.top_right + GridDisplacement(0, 1)).overlaps(rect))

    @staticmethod
    def from_proto(proto: geom_pb2.Gridtangle) -> Gridtangle:
        return Gridtangle(
            GridCoord.from_proto(proto.bottom_left),
            GridCoord.from_proto(proto.top_right),
        )

    def to_proto(self) -> geom_pb2.Gridtangle:
        return geom_pb2.Gridtangle(
            bottom_left=self.bottom_left.to_proto(),
            top_right=self.top_right.to_proto(),
        )

    def corners(self) -> list[GridCoord]:
        return list({
            self.bottom_left,
            self.top_right,
            GridCoord(self.bottom_left.x, self.top_right.y),
            GridCoord(self.top_right.x, self.bottom_left.y),
        })

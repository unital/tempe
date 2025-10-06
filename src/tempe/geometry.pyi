# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

from array import array
from collections.abc import Sequence, Iterator, Iterable, Generator
from typing import Any, Generic, TypeVar

from .data_view import DataView

type point = tuple[int, int]
type points = tuple[int, int, int, int]
type point_array = array[int]

class Geometry[DataType](DataView[DataType]):
    """Efficient storage of geometric information."""

    geometry: Sequence
    coords: int | None

    def __init__(self, geometry: Sequence, coords: int | None = None) -> None: ...


class RowGeometry[DataType](Geometry[DataType]):
    """Geometry where coordinates are provided as ragged rows."""

    @classmethod
    def from_lists(cls, rows: Iterable[Sequence[int]]) -> RowGeometry[T]: ...

class ColumnGeometry[DataType](Geometry[DataType]):
    """Geometry where coordinates are provided as ragged columns"""

class StripGeometry(Geometry[point_array]):
    """Geometry generating connected strip of n-gons from vertices.

    Iterator provides vertex point buffers of the form [x0, y0, x1, y1, ...].
    """

    #: Grabbing pairs of coordinates for vertices.
    n_coords: int = 2

    def __init__(self, geometry: Sequence[Sequence[int]], n_vertices: int = 2, step: int = 1): ...


class PointsToLines(Geometry[points]):
    """Turn a generator of x, y values into a generator of (x0, y0, x1, y1)."""

    def __init__(self, geometry: Geometry[point]) -> None: ...

class Extend[DataType](Geometry[DataType]):
    """Concatenate multiple geometries row-wise."""

    def __init__(self, geometry: Sequence[Geometry]) -> None: ...

class ProductGeometry[DataType](Geometry[DataType]):

    def __init__(self, geometry: tuple[Sequence, Sequence]) -> None: ...

class Select[DataType](Geometry[DataType]):

    def __init__(self, geometry: Sequence[Sequence], selection: Sequence[int]) -> None: ...

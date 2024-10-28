# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

from array import array
from collections.abc import Sequence, Iterator, Iterable
from typing import Any, Generic, TypeVar

from .data_view import DataView

_T = TypeVar("_T", bound=Sequence[int])

class Geometry(DataView[_T]):
    """Efficient storage of geometric information."""

class RowGeometry(Geometry):
    """Geometry where coordinates are provided as ragged rows."""

    @classmethod
    def from_lists(cls, rows: Sequence[Sequence[int]]) -> RowGeometry: ...

class ColumnGeometry(Geometry):
    """Geometry where coordinates are provided as ragged columns"""

class StripGeometry(Geometry):
    """Geometry generating connected strip of n-gons from vertices.

    Iterator provides vertex point buffers of the form [x0, y0, x1, y1, ...].
    """

    #: Grabbing pairs of coordinates for vertices.
    n_coords: int = 2

    def __init__(self, geometry, n_vertices: int = 2, step: int = 1): ...

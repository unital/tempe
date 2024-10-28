# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

"""Draw wide lines

This takes the line geometry and draws rectanglular polygons that match
the thickened line's shape.  Joins and endpoints are rounded by default
by rendering circles at the vertices.

.. note:::

   This is an experimental module: it is not clear that this approach is
   the best way to draw thicker lines.  Eg. it may be better to render
   directly into the buffer using viper, or it may be better to provide
   functions that transform the line geometry to a polygon geometry.

"""

from array import array
from collections.abc import Sequence, Iterable
from math import sqrt
from typing import TypeAlias

from .shapes import ColoredGeometry, point_array, rectangle

points_widths: TypeAlias = tuple[int, int, int, int, int]

class WideLines(ColoredGeometry[points_widths]):
    """Render multiple colored line segments with variable width.

    Geometry should produce x0, y0, x1, y1, width arrays.

    For line widths less than 2, this renders using the standard framebuf
    line drawing routines.  For line widths of 2 or more, this renders each
    segment using a rectangular polygons and, if ``round`` is True, two
    circles at the ends.

    Parameters
    ----------
    geometry : Iterable[geom]
        The sequence of geometries to render.
    colors : Iterable[int]
        The sequence of colors for each geometry.
    round : bool
        Whether to round the ends with circles, or to leave as a flat end.
    surface : Surface | None
        The surface which this shape is associated with.
    clip : rectangle | None
        An (x, y, w, h) tuple to clip drawing to - anything drawn outside
        this region will not show on the display.
    """

    def __init__(
        self,
        geometry: Iterable[points_widths],
        colors: Iterable[int],
        *,
        round: bool = True,
        surface: "tempe.surface.Surface | None" = None,
        clip: rectangle | None = None,
    ): ...
    def __iter__(self) -> tuple[points_widths, int]: ...

class WidePolyLines(ColoredGeometry[point_array]):
    """Render multiple colored polylines with variable width.

    Geometry should produce array of [x0, y0, x1, y1, ..., width].

    For line widths less than 2, this renders using the standard framebuf
    line drawing routines.  For line widths of 2 or more, this renders each
    polyline using rectanglular polygons for the segments and circles at
    the vertices.
    """

def line_points(
    x0: int,
    y0: int,
    x1: int,
    y1: int,
    w: int,
    d: int,
    vertices: array[int],
) -> array[int]:
    """Compute the vertices of a thick line segment's rectangle.

    Parameters
    ----------
    x0, y0, x1, y1: int
        The coordinates of the endpoints of the line segment.
    w : int
        The width of the line segment.
    d : int
        A scale factor: twice the integer length of the line.
    vertices : array
        An empty array to hold the resulting 8 coordinates of the rectangle's
        corners.

    Note
    ----
    This is replaced by a viper-accelerated version of the code, where
    available.
    """

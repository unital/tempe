# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

"""Shape classes which efficiently draw fundamental geometries.

This module provides the core shape abstract base classes, along with
concrete classes that implement drawing of multiple rectangles, lines,
polygons and ellipses.  The latter are wrappers around calls to the
corresponding |FrameBuffer| routines, and have the same constraints,
such as lines being limited to 1 pixel width.

The shape types have expectations about the types of the data produced
by the geometries.  These are not formally defined as types or classes
for speed and memory efficiency, but are treated as type aliases by
Python type annotations.

.. py:type:: geom

   A generic geometry as a sequence of ints of unspecified length.

.. py:type:: point

   A sequence of ints of the form (x, y).

.. py:type:: points

   A sequence of ints of the form (x0, y0, x1, y1).

.. py:type:: point_length

   A sequence of ints of the form (x, y, length).  The length can also be
   used as a size parameter for markers or radius of a circle, as appropriate.

.. py:type:: point_array

   An array of signed 16-bit integers giving point coordinates of the
   form ``array('h', [x0, y0, x1, y1, ...])``.

.. py:type:: rectangle

   A sequence of ints of the form (x, y, w, h).

.. py:type:: ellipse

   A sequence of ints of the form (center_x, center_y, radius_x, radius_y).

.. |FrameBuffer| replace:: :py:class:`~framebuf.FrameBuffer`

Attributes
----------

BLIT_KEY_RGB565 : int
    The default transparency color when blitting an RGB565 |FrameBuffer|.
    This is a color which has 1 in the 6th (least significant) bit of
    green, and 0 red and blue.
"""

from array import array
import asyncio
from collections.abc import Sequence, Iterable
from framebuf import FrameBuffer
from typing import Any, Generic, TypeVar, TypeAlias

from .geometry import Geometry
from .data_view import DataView

geom = TypeVar("geom", bound=Sequence[int])
point: TypeAlias = tuple[int, int]
points: TypeAlias = tuple[int, int, int, int]
point_array: TypeAlias = array[int]
point_length: TypeAlias = tuple[int, int, int]
rectangle: TypeAlias = tuple[int, int, int, int]
ellipse: TypeAlias = tuple[int, int, int, int]

#: Transparent color when blitting bitmaps.
BLIT_KEY_RGB565 = 0b0000000000100000

class Shape:
    """ABC for drawable objects.

    Parameters
    ----------
    surface : Surface | None
        The surface which this shape is associated with.
    clip : rectangle | None
        An (x, y, w, h) tuple to clip drawing to - anything drawn outside
        this region will not show on the display.
    """

    def __init__(
        self,
        surface: "tempe.surface.Surface | None" = None,
        clip: rectangle | None = None,
    ): ...
    def draw(self, buffer: FrameBuffer, x: int = 0, y: int = 0) -> None:
        """Render the shape into the given buffer offset by x and y.

        Concrete subclasses need to translate any drawing they do in the
        buffer by the x and y offsets.

        Parameters
        ----------
        buffer : framebuf.FrameBuffer
            An array of pixels to be rendered into.
        x : int
            The x-offset of the left side of the buffer on the
            surface.
        y : int
            The y-offset of the top side of the buffer on the
            surface.
        """

    def update(self, **kwargs: Any) -> None:
        """Update the state of the Shape, marking a redraw as needed.

        This adds the clipping rectangle to the damaged regions of the
        Surface.  Subclasses should allow additional keyword arguments
        for updating geometry and other state as needed, and should
        either call ``super()`` or otherwise ensure that the Surface
        has its damage region updated.
        """

    def _get_bounds(self) -> rectangle:
        """Compute the bounds of the Shape.

        Subclasses need to override this.
        """

class ColoredGeometry(Shape, Generic[geom]):
    """ABC for geometries with colors applied.

    These classes draw each shape from the Geometry using the
    corresponding color from the color data.  ColoredGeometries
    are iterable with the iterator producing (geometry, color)
    pairs.

    Parameters
    ----------
    geometry : Iterable[geom]
        The sequence of geometries to render.
    colors : Iterable[int]
        The sequence of colors for each geometry.
    surface : Surface | None
        The surface which this shape is associated with.
    clip : rectangle | None
        An (x, y, w, h) tuple to clip drawing to - anything drawn outside
        this region will not show on the display.
    """

    def __init__(
        self,
        geometry: Iterable[geom],
        colors: Iterable[int],
        *,
        surface: "tempe.surface.Surface | None" = None,
        clip: rectangle | None = None,
    ): ...
    def update(
        self,
        geometry: Iterable[geom] | None = None,
        colors: Iterable[int] | None = None,
        **kwargs: DataView[Any] | None,
    ):
        """Update the state of the Shape, marking a redraw as needed.

        Parameters
        ----------
        geometry : Geometry[geom] | None
            The sequence of geometries to render.
        colors : Iterable[int] | None
            The sequence of colors for each geometry.
        """

    def __iter__(self) -> tuple: ...

class FillableGeometry(ColoredGeometry[geom]):
    """ABC for geometries which can either be filled or stroked.

    Stroked outlines always have line with 1.

    Parameters
    ----------
    geometry : Iterable[geom]
        The sequence of geometries to render.
    colors : Iterable[int]
        The sequence of colors for each geometry.
    fill : bool
        Whether to fill the shape or to draw the outline.
    surface : Surface | None
        The surface which this shape is associated with.
    clip : rectangle | None
        An (x, y, w, h) tuple to clip drawing to - anything drawn outside
        this region will not show on the display.
    """

    def __init__(
        self,
        geometry: Iterable[geom],
        colors: Iterable[int],
        *,
        fill: bool = True,
        surface: "tempe.surface.Surface | None" = None,
        clip: rectangle | None = None,
    ): ...

class Lines(ColoredGeometry[points]):
    """Render multiple colored line segments with line-width 1.

    Geometry should produce x0, y0, x1, y1 arrays.
    """

    def __init__(
        self,
        geometry: Iterable[points],
        colors: Iterable[int],
        *,
        surface: "tempe.surface.Surface | None" = None,
        clip: rectangle | None = None,
    ): ...
    def __iter__(self) -> tuple[points, int]: ...

class HLines(ColoredGeometry[point_length]):
    """Render multiple colored horizontal line segments with line-width 1.

    Geometry should produce x0, y0, length arrays.
    """

    def __init__(
        self,
        geometry: Iterable[point_length],
        colors: Iterable[int],
        *,
        surface: "tempe.surface.Surface | None" = None,
        clip: rectangle | None = None,
    ): ...
    def __iter__(self) -> tuple[point_length, int]: ...

class VLines(ColoredGeometry[point_length]):
    """Render multiple colored vertical line segments with line-width 1.

    Geometry should produce x0, y0, length arrays.
    """

    def __init__(
        self,
        geometry: Iterable[point_length],
        colors: Iterable[int],
        *,
        surface: "tempe.surface.Surface | None" = None,
        clip: rectangle | None = None,
    ): ...
    def __iter__(self) -> tuple[point_length, int]: ...

class Polygons(FillableGeometry[point_array]):
    """Render multiple polygons.

    Geometry should produce vertex arrays of the form [x0, y0, x1, y1, ...].
    """

    def __iter__(self) -> tuple[point_array, int]: ...

class PolyLines(ColoredGeometry[point_array]):
    """Render multiple polygons.

    Geometry should produce vertex arrays of the form [x0, y0, x1, y1, ...].
    """

    def __iter__(self) -> tuple[point_array, int]: ...

class Rectangles(FillableGeometry[rectangle]):
    """Render multiple rectangles.

    Geometry should produce x, y, w, h arrays.
    """

    def __init__(
        self,
        geometry: Iterable[rectangle],
        colors: Iterable[int],
        *,
        fill: bool = True,
        surface: "tempe.surface.Surface | None" = None,
        clip: rectangle | None = None,
    ): ...
    def __iter__(self) -> tuple[rectangle, int]: ...

class RoundedRectangles(Rectangles):
    """Render multiple rounded rectangles.

    Geometry should produce x, y, w, h arrays.
    """

    def __init__(
        self,
        geometry: Iterable[rectangle],
        colors: Iterable[int],
        *,
        radius: int = 4,
        fill: bool = True,
        surface: "tempe.surface.Surface | None" = None,
        clip: rectangle | None = None,
    ): ...
    def __iter__(self) -> tuple[rectangle, int]: ...

class Circles(FillableGeometry[point_length]):
    """Render multiple circles.

    Geometry should produce cx, cy, r arrays.
    """

    def __init__(
        self,
        geometry: Iterable[point_length],
        colors: Iterable[int],
        *,
        fill: bool = True,
        surface: "tempe.surface.Surface | None" = None,
        clip: rectangle | None = None,
    ): ...
    def __iter__(self) -> tuple[point_length, int]: ...

class Ellipses(FillableGeometry[ellipse]):
    """Render multiple ellipses.

    Geometry should produce cx, cy, rx, ry arrays.
    """

    def __init__(
        self,
        geometry: Iterable[ellipse],
        colors: Iterable[int],
        *,
        fill: bool = True,
        surface: "tempe.surface.Surface | None" = None,
        clip: rectangle | None = None,
    ): ...
    def __iter__(self) -> tuple[ellipse, int]: ...

__all__ = [
    "Shape",
    "ColoredGeometry",
    "FillableGeometry",
    "Lines",
    "HLines",
    "VLines",
    "Polygons",
    "Rectangles",
    "RoundedRectangles",
    "Circles",
    "Ellipses",
]

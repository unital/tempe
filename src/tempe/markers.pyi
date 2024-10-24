from collections.abc import Iterable
from array import array
import framebuf
from typing import Any

from .geometry import Geometry
from .shapes import ColoredGeometry, BLIT_KEY_RGB565, rectangle, point_length, point
from .surface import Surface


class Marker:
    """Enum for marker types"""
    PIXEL = 0
    CIRCLE = 1
    SQUARE = 2
    HLINE = 3
    VLINE = 4
    PLUS = 5
    CROSS = 6


class Markers(ColoredGeometry[point_length]):
    """Display sized, colored markers at points.

    Parameters
    ----------
    geometry : Iterable[geom] | None
        The sequence of geometries to render.
    colors : Iterable[int] | None
        The sequence of colors for each geometry.
    markers : Iterable[Any] | None
        The sequence of colors for each geometry.
    surface : Surface | None
        The surface which this shape is associated with.
    clip : rectangle | None
        An (x, y, w, h) tuple to clip drawing to - anything drawn outside
        this region will not show on the display.
    """

    def __init__(
        self,
        geometry: Geometry[point_length],
        colors: Iterable[int],
        markers: Iterable[Any],
        *,
        surface: Surface | None = None,
        clip: rectangle | None = None,
    ): ...

    def update(
        self,
        geometry: Iterable[point_length] | None = None,
        colors: Iterable[int] | None = None,
        markers: Iterable[Any] | None = None,
        **kwargs: Any,
    ):
        """Update the state of the Shape, marking a redraw as needed.

        Parameters
        ----------
        geometry : Iterable[geom] | None
            The sequence of geometries to render.
        colors : Iterable[int] | None
            The sequence of colors for each geometry.
        markers : Iterable[Any] | None
            The sequence of colors for each geometry.
        """

class Points(ColoredGeometry[point]):
    """Display colored markers at points.

    Parameters
    ----------
    geometry : Iterable[geom] | None
        The sequence of geometries to render.
    colors : Iterable[int] | None
        The sequence of colors for each geometry.
    markers : Iterable[Any] | None
        The sequence of colors for each geometry.
    surface : Surface | None
        The surface which this shape is associated with.
    clip : rectangle | None
        An (x, y, w, h) tuple to clip drawing to - anything drawn outside
        this region will not show on the display.
    """

    def __init__(
        self,
        geometry: Geometry[point],
        colors: Iterable[int],
        markers: Iterable[Any],
        *,
        surface: Surface | None = None,
        clip: rectangle | None = None,
    ): ...

    def update(
        self,
        geometry: Iterable[point] | None = None,
        colors: Iterable[int] | None = None,
        markers: Iterable[Any] | None = None,
        **kwargs: Any,
    ):
        """Update the state of the Shape, marking a redraw as needed.

        Parameters
        ----------
        geometry : Iterable[geom] | None
            The sequence of geometries to render.
        colors : Iterable[int] | None
            The sequence of colors for each geometry.
        markers : Iterable[Any] | None
            The sequence of colors for each geometry.
        """

# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

"""Markers and Points shape classes."""

from collections.abc import Iterable
from array import array
import framebuf
from typing import Any

import tempe
from .geometry import Geometry
from .shapes import ColoredGeometry, BLIT_KEY_RGB565, rectangle, point_length, point
from .colors import rgb565

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

    Markers expect a geometry of the form (x, y).

    Parameters
    ----------
    geometry : Iterable[geom]
        The sequence of geometries to render.
    colors : Iterable[rgb565]
        The sequence of colors for each geometry.
    sizes : Iterable[int]
        The sequence of sizes for each geometry.
    markers : Iterable[Any]
        The sequence of colors for each geometry.
    surface : Surface | None
        The surface which this shape is associated with.
    clip : rectangle | None
        An (x, y, w, h) tuple to clip drawing to - anything drawn outside
        this region will not show on the display.
    """
    markers: Iterable[Any]

    def __init__(
        self,
        geometry: Geometry[point_length],
        colors: Iterable[rgb565],
        sizes: Iterable[int],
        markers: Iterable[Any],
        *,
        surface: "tempe.surface.Surface | None" = None,
        clip: rectangle | None = None,
    ): ...
    def update(
        self,
        geometry: Iterable[point_length] | None = None,
        colors: Iterable[rgb565] | None = None,
        sizes: Iterable[int] | None = None,
        markers: Iterable[Any] | None = None,
        **kwargs: Any,
    ):
        """Update the state of the Shape, marking a redraw as needed.

        Parameters
        ----------
        geometry : Iterable[geom] | None
            The sequence of geometries to render.
        sizes : Iterable[int] | None
            The sequence of sizes for each geometry.
        colors : Iterable[rgb565] | None
            The sequence of colors for each geometry.
        markers : Iterable[Any] | None
            The sequence of colors for each geometry.
        """

class Points(ColoredGeometry[point]):
    """Display colored markers at points.

    Points expect a geometry of the form (x, y)

    Parameters
    ----------
    geometry : Iterable[geom] | None
        The sequence of geometries to render.
    colors : Iterable[rgb565] | None
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
        colors: Iterable[rgb565],
        markers: Iterable[Any],
        *,
        surface: Surface | None = None,
        clip: rectangle | None = None,
    ): ...
    def update(
        self,
        geometry: Iterable[point] | None = None,
        colors: Iterable[rgb565] | None = None,
        markers: Iterable[Any] | None = None,
        **kwargs: Any,
    ):
        """Update the state of the Shape, marking a redraw as needed.

        Parameters
        ----------
        geometry : Iterable[geom] | None
            The sequence of geometries to render.
        colors : Iterable[rgb565] | None
            The sequence of colors for each geometry.
        markers : Iterable[Any] | None
            The sequence of colors for each geometry.
        """

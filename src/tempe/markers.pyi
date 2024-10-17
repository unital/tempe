from collections.abc import Iterable
from array import array
import framebuf
from typing import Any

from .geometry import Geometry
from .shapes import ColoredGeometry, BLIT_KEY_RGB565, rectangle
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


class Markers(ColoredGeometry):
    """Display sized, colored markers at points."""

    def __init__(
        self,
        geometry: Geometry[tuple[int, int, int]],
        colors: Iterable[int],
        markers: Iterable[Any],
        *,
        surface: Surface | None = None,
        clip: rectangle | None = None,
    ): ...

    def update(
        self,
        geometry: Geometry[tuple[int, int, int]] | None = None,
        colors: Iterable[int] | None = None,
        markers: Iterable[Any] | None = None,
        **kwargs: Any,
    ): ...

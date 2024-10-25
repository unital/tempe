
from array import array
from collections.abc import Sequence, Iterable
import framebuf
from typing import Any

import tempe
from .shapes import ColoredGeometry, Shape, BLIT_KEY_RGB565, point, rectangle


class Bitmaps(Shape):
    """Draw framebuffer bitmaps at points"""

    def __init__(
        self,
        geometry: Iterable[point],
        buffers: Iterable[framebuf.FrameBuffer],
        *,
        key: int | None = None,
        palette: Sequence[int] | None = None,
        surface: "tempe.surface.Surface | None" = None,
        clip: rectangle | None = None,
    ): ...

    def update(
        self,
        geometry: Iterable[point] | None = None,
        buffers: Iterable[framebuf.FrameBuffer] | None = None,
        **kwargs: Any,
    ): ...

    def __iter__(self) -> tuple[point, framebuf.FrameBuffer]: ...


class ColoredBitmaps(ColoredGeometry[point]):
    """Draw 1-bit framebuffers bitmaps at points in given colors."""

    def __init__(
        self,
        geometry: Iterable[point],
        colors: Iterable[int],
        buffers: Iterable[framebuf.FrameBuffer],
        *,
        surface: "tempe.surface.Surface | None" = None,
        clip: rectangle | None = None,
    ): ...

    def update(
        self,
        geometry: Iterable[point] | None = None,
        colors: Iterable[int] | None = None,
        buffers: Iterable[framebuf.FrameBuffer] | None = None,
        **kwargs: Any,
    ): ...

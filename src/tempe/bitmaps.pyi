# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

"""Bitmap shape classes."""

from array import array
from collections.abc import Sequence, Iterable
import framebuf
from typing import Any

import tempe.surface
from .shapes import ColoredGeometry, Shape, BLIT_KEY_RGB565, point, rectangle
from .colors import rgb565

class Bitmaps(Shape):
    """Draw framebuffer bitmaps at points"""

    def __init__(
        self,
        geometry: Iterable[point],
        buffers: Iterable[framebuf.FrameBuffer],
        *,
        key: int | None = None,
        palette: Sequence[rgb565] | None = None,
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
        colors: Iterable[rgb565],
        buffers: Iterable[framebuf.FrameBuffer],
        *,
        surface: "tempe.surface.Surface | None" = None,
        clip: rectangle | None = None,
    ): ...
    def update(
        self,
        geometry: Iterable[point] | None = None,
        colors: Iterable[rgb565] | None = None,
        buffers: Iterable[framebuf.FrameBuffer] | None = None,
        **kwargs: Any,
    ): ...

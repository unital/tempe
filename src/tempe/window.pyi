# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

from .raster import Raster
from .surface import Surface, rectangle
from .shapes import Shape


class Window(Shape):
    """A Shape which displays a surface."""

    def __init__(
        self,
        offset: tuple[int, int] | None = None,
        *,
        surface: Surface | None = None,
        clip: rectangle | None = None,
    ): ...

    def draw_raster(self, raster: Raster):
        """Draw the Window's contents in the Raster"""

    def update(self, offset: tuple[int, int] | None = None, **kwargs): ...

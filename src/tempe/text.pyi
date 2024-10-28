# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

from collections.abc import Iterable
from typing import Any
import framebuf

import tempe
from .geometry import Geometry
from .font import AbstractFont
from .shapes import ColoredGeometry, BLIT_KEY_RGB565, rectangle, point

class Text(ColoredGeometry[tuple[int, int]]):
    def __init__(
        self,
        geometry: Iterable[point],
        colors: Iterable[int],
        texts: Iterable[str],
        *,
        bold: bool = False,
        font: AbstractFont | None = None,
        surface: "tempe.surface.Surface | None" = None,
        clip: rectangle | None = None,
    ): ...
    def __iter__(self) -> tuple[Geometry[tuple[int, int]], int, str]: ...
    def update(
        self,
        geometry: Iterable[tuple[int, int]] | None = None,
        colors: Iterable[int] | None = None,
        texts: Iterable[str] | None = None,
        **kwargs: Any,
    ): ...

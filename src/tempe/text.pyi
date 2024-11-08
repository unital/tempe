# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

from collections.abc import Iterable
from typing import Any, Literal, TypeAlias
import framebuf

import tempe
from .geometry import Geometry
from .font import AbstractFont
from .shapes import ColoredGeometry, BLIT_KEY_RGB565, rectangle, point

LEFT: Literal[0] = 0
RIGHT: Literal[1] = 1
CENTER: Literal[2] = 2
TOP: Literal[0] = 0
BOTTOM: Literal[1] = 1

HALIGN: TypeAlias = Literal[0, 1, 2]
VALIGN: TypeAlias = Literal[0, 1, 2]

class Text(ColoredGeometry[tuple[int, int]]):
    def __init__(
        self,
        geometry: Iterable[point],
        colors: Iterable[int],
        texts: Iterable[str],
        alignment: Iterable[tuple[HALIGN, VALIGN]],
        *,
        bold: bool = False,
        font: AbstractFont | None = None,
        letter_spacing: int = 0,
        surface: "tempe.surface.Surface | None" = None,
        clip: rectangle | None = None,
    ): ...
    def __iter__(self) -> tuple[Geometry[tuple[int, int]], int, str, tuple[HALIGN, VALIGN]]: ...
    def update(
        self,
        geometry: Iterable[tuple[int, int]] | None = None,
        colors: Iterable[int] | None = None,
        texts: Iterable[str] | None = None,
        alignment: Iterable[tuple[HALIGN, VALIGN]] | None = None,
        **kwargs: Any,
    ): ...

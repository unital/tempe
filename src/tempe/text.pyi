# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

from collections.abc import Iterable
from typing import Any, Literal, TypeAlias
import framebuf

import tempe
from .data_view import Repeat
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

class Text(ColoredGeometry[point]):
    """Draw coloured strings at points with alignment."""

    def __init__(
        self,
        geometry: Iterable[point],
        colors: Iterable[int],
        texts: Iterable[str],
        alignment: Iterable[tuple[HALIGN, VALIGN]] = Repeat((LEFT, TOP)),
        *,
        bold: bool = False,
        font: AbstractFont | None = None,
        line_spacing: int = 0,
        surface: "tempe.surface.Surface | None" = None,
        clip: rectangle | None = None,
    ): ...
    def __iter__(self) -> tuple[Geometry[point], int, str, tuple[HALIGN, VALIGN]]: ...
    def update(
        self,
        geometry: Iterable[point] | None = None,
        colors: Iterable[int] | None = None,
        texts: Iterable[str] | None = None,
        alignment: Iterable[tuple[HALIGN, VALIGN]] | None = None,
        **kwargs: Any,
    ): ...

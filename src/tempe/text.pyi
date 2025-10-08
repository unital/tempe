# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

from collections.abc import Iterable, Generator
from typing import Any, Literal, TypeAlias
import framebuf

import tempe
from .data_view import Repeat
from .geometry import Geometry
from .font import AbstractFont
from .shapes import ColoredGeometry, BLIT_KEY_RGB565, rectangle, point
from .colors import rgb565

LEFT: Literal[0] = 0
RIGHT: Literal[1] = 1
CENTER: Literal[2] = 2
TOP: Literal[3] = 3
BOTTOM: Literal[4] = 4

type HALIGN = Literal[0, 1, 2]
type VALIGN = Literal[2, 3, 4]

class Text(ColoredGeometry[point]):
    """Draw coloured strings at points with alignment."""

    def __init__(
        self,
        geometry: Iterable[point],
        colors: Iterable[rgb565],
        texts: Iterable[str],
        alignments: Iterable[tuple[HALIGN, VALIGN]] = Repeat((LEFT, TOP)),
        *,
        bold: bool = False,
        font: AbstractFont | None = None,
        line_spacing: int = 0,
        surface: "tempe.surface.Surface | None" = None,
        clip: rectangle | None = None,
    ): ...
    def __iter__(self) -> Generator[tuple[Geometry[point], int, str, tuple[HALIGN, VALIGN]], None, None]: ...
    def update(
        self,
        geometry: Iterable[point] | None = None,
        colors: Iterable[rgb565] | None = None,
        texts: Iterable[str] | None = None,
        alignments: Iterable[tuple[HALIGN, VALIGN]] | None = None,
        font: AbstractFont | None = None,
        **kwargs: Any,
    ): ...

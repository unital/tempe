# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

"""Color conversion routines."""

from typing import overload
from collections.abc import Iterable
from .types import color, rgb, rgb565

@overload
def normalize_color(color: color) -> rgb565: ...

@overload
def normalize_color(color: None) -> None: ...

def rgb_sequence_to_rgb565(colors: Iterable[rgb]) -> list[rgb565]: ...

def rgb444_to_rgb565(r: int, g: int, b: int, big_endian: bool = True) -> rgb565: ...

def rgb24_to_rgb565(r: int, g: int, b: int, big_endian: bool = True) -> rgb565: ...

def rgb_to_rgb565(r: float, g: float, b: float, big_endian: bool = True) -> rgb565: ...

def from_str(color_str: str) -> rgb565: ...

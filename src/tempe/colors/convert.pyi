# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

"""Color conversion routines."""

from collections.abc import Iterable

def rgb_to_rgb565(colors: Iterable[tuple[int, int, int]]) -> list[int]: ...

def rgb444_to_rgb565(r: int, g: int, b: int, big_endian: bool = True) -> int: ...

def rgb24_to_rgb565(r: int, g: int, b: int, big_endian: bool = True) -> int: ...

def rgb565(r: int, g: int, b: int, big_endian: bool = True) -> int: ...

def from_str(color_str: str) -> int: ...

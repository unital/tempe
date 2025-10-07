# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

"""Basic colors and conversion routines."""
from typing import Final

from .basic import (
    aqua,
    black,
    blue,
    fuchsia,
    gray,
    grey,
    green,
    lime,
    maroon,
    navy,
    olive,
    purple,
    red,
    silver,
    teal,
    white,
    yellow,
)
from .convert import from_str, rgb444_to_rgb565, rgb_to_rgb565, normalize_color
from .types import color, rgb565

grey_0: Final[rgb565] = 0x0000
grey_1: Final[rgb565] = 0x8210
grey_2: Final[rgb565] = 0x0421
grey_3: Final[rgb565] = 0x8631
grey_4: Final[rgb565] = 0x0842
grey_5: Final[rgb565] = 0x8a52
grey_6: Final[rgb565] = 0x0c63
grey_7: Final[rgb565] = 0x8e73
grey_8: Final[rgb565] = 0x1084
grey_9: Final[rgb565] = 0x9294
grey_a: Final[rgb565] = 0x14a5
grey_b: Final[rgb565] = 0x96b5
grey_c: Final[rgb565] = 0x18c6
grey_d: Final[rgb565] = 0x9ad6
grey_e: Final[rgb565] = 0x1ce7
grey_f: Final[rgb565] = 0x9ef7

__all__ = [
    "aqua",
    "black",
    "blue",
    "fuchsia",
    "gray",
    "grey",
    "green",
    "lime",
    "maroon",
    "navy",
    "olive",
    "purple",
    "red",
    "silver",
    "teal",
    "white",
    "yellow",
    "grey_0",
    "grey_1",
    "grey_2",
    "grey_3",
    "grey_4",
    "grey_5",
    "grey_6",
    "grey_7",
    "grey_8",
    "grey_9",
    "grey_a",
    "grey_b",
    "grey_c",
    "grey_d",
    "grey_e",
    "grey_f",
    "normalize_color",
    "from_str",
    "rgb_to_rgb565",
]
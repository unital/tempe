# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

"""Basic colors and conversion routines."""

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

grey_0 = const(0x0000)
grey_1 = const(0x8210)
grey_2 = const(0x0421)
grey_3 = const(0x8631)
grey_4 = const(0x0842)
grey_5 = const(0x8a52)
grey_6 = const(0x0c63)
grey_7 = const(0x8e73)
grey_8 = const(0x1084)
grey_9 = const(0x9294)
grey_a = const(0x14a5)
grey_b = const(0x96b5)
grey_c = const(0x18c6)
grey_d = const(0x9ad6)
grey_e = const(0x1ce7)
grey_f = const(0x9ef7)

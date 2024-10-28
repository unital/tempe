# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

"""Basic colors and conversion routines."""

from .basic import (
    aqua, black, blue, fuchsia, gray, grey, green, lime,
    maroon, navy, olive, purple, red, silver, teal, white,
    yellow,
)
from .convert import from_str, rgb444_to_rgb565, rgb565

grey_0 = 0x0000
grey_1 = rgb444_to_rgb565(0x1, 0x1, 0x1)
grey_2 = rgb444_to_rgb565(0x2, 0x2, 0x2)
grey_3 = rgb444_to_rgb565(0x3, 0x3, 0x3)
grey_4 = rgb444_to_rgb565(0x4, 0x4, 0x4)
grey_5 = rgb444_to_rgb565(0x5, 0x5, 0x5)
grey_6 = rgb444_to_rgb565(0x6, 0x6, 0x6)
grey_7 = rgb444_to_rgb565(0x7, 0x7, 0x7)
grey_8 = rgb444_to_rgb565(0x8, 0x8, 0x8)
grey_9 = rgb444_to_rgb565(0x9, 0x9, 0x9)
grey_a = rgb444_to_rgb565(0xA, 0xA, 0xA)
grey_b = rgb444_to_rgb565(0xB, 0xB, 0xB)
grey_c = rgb444_to_rgb565(0xC, 0xC, 0xC)
grey_d = rgb444_to_rgb565(0xD, 0xD, 0xD)
grey_e = rgb444_to_rgb565(0xE, 0xE, 0xE)
grey_f = rgb444_to_rgb565(0xF, 0xF, 0xF)

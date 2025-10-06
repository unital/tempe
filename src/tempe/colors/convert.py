# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

"""Color conversion routines."""


def rgb_to_rgb565(colors):
    rgb565_colors = []
    for color in colors:
        r, g, b = color
        bytes = (int(r * 0x1F) << 11) | (int(g * 0x3F) << 5) | int(b * 0x1F)
        rgb565_colors.append((bytes >> 8) | ((bytes & 0xFF) << 8))
    return rgb565_colors


def rgb444_to_rgb565(r, g, b, big_endian=True):
    bytes = (r << 12) | (g << 7) | (b << 1)
    if big_endian:
        return (bytes >> 8) | ((bytes & 0xFF) << 8)
    else:
        return bytes


def rgb24_to_rgb565(r, g, b, big_endian=True):
    bytes = ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)
    if big_endian:
        return (bytes >> 8) | ((bytes & 0xFF) << 8)
    else:
        return bytes


def rgb565(r, g, b, big_endian=True):
    bytes = (
        (int(round(r * 0x1F)) << 11)
        | (int(round(g * 0x3F)) << 5)
        | int(round(b * 0x1F))
    )
    if big_endian:
        return (bytes >> 8) | ((bytes & 0xFF) << 8)
    else:
        return bytes


def from_str(color_str):
    color_str = color_str.lower()
    if color_str.startswith("#"):
        if len(color_str) == 4:
            return rgb444_to_rgb565(*(int(c, 16) for c in color_str[1:]), big_endian=True)
        elif len(color_str) == 7:
            return rgb24_to_rgb565(
                *(int(f"{color_str[i:i+2]}", 16) for i in range(1, len(color_str), 2)),
                big_endian=True,
            )
    else:
        # is it a named Tempe color?
        from tempe import colors

        if (c := getattr(colors, color_str, None)) and isinstance(c, int):
            return c

        # try a named web color
        from .web import color

        c = color(color_str)
        if c != 0:
            return c
        else:
            raise ValueError(f"Unknown color string {color_str!r}")

# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

"""Basic conversion utility to take raw RGB565 to .png format."""

import array
from pathlib import Path

from PIL import Image


def read_rgb565(path):
    with open(path, "rb") as fp:
        buffer = fp.read()

    rgb565 = array.array("H", buffer)
    rgb565.byteswap()
    return rgb565


def rgb565_to_rgb24(rgb565):
    rgb24 = array.array("B", bytearray(3 * len(rgb565)))
    for i, pixel in enumerate(rgb565):
        r = (pixel & 0b1111100000000000) >> 11
        g = (pixel & 0b0000011111100000) >> 5
        b = pixel & 0b0000000000011111
        rgb24[3 * i] = int((r / 31) * 255)
        rgb24[3 * i + 1] = int(round((g / 63) * 255))
        rgb24[3 * i + 2] = int(round((b / 31) * 255))
    return rgb24


def rgb565_to_png(size, in_path, out_path=None):
    if out_path is None:
        out_path = Path(in_path.stem + ".png")

    rgb565 = read_rgb565(in_path)
    rgb24 = rgb565_to_rgb24(rgb565)
    image = Image.frombuffer("RGB", size, rgb24)
    image.save(out_path)


if __name__ == "__main__":
    import sys

    rgb565_to_png((320, 240), Path(sys.argv[1]))

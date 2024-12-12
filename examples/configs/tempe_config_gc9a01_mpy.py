# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

"""Example tempe_config file for GC9A01-based displays.

This example assumes you have the GC9A01 firmware from
https://github.com/russhughes/gc9a01_mpy installed on your
device and that you have a tft_config file as described in
the documentation: https://russhughes.github.io/gc9a01_mpy/examples.html
"""

from tft_config import config
from tempe.display import Display


# Change to match the characteristics of your display
ROTATION = 0


class GC9A01MpyDisplay(Display):
    """Display that wraps a gc9a01_mpy display."""

    def __init__(self, rotation=0, buffer_size=0, options=0):
        self.display = config(rotation, buffer_size, options)
        self.size = (self.display.width(), self.display.height())

    def blit(self, buffer, x, y, w, h):
        self.display.blit_buffer(buffer, x, y, w, h)


async def init_display():
    display = GC9A01MpyDisplay(ROTATION)
    return display

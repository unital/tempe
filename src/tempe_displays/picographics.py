# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

"""Example tempe_config file for PicoGraphics-based displays.

This example assumes you have the Pimoroni firmware installed on your
device.
"""
from framebuf import FrameBuffer, RGB565
from tempe.display import Display


class PicoGraphicsDisplay(Display):
    """Display that wraps a Pimoroni PicoGraphics display.

    This should work for any device which can support RGB565 color.
    """

    def __init__(self, display):
        self.display = display
        self.size = display.get_bounds()
        self.framebuf = FrameBuffer(display, self.size[0], self.size[1], RGB565)

    def blit(self, buffer, x, y, w, h):
        self.framebuf.blit((buffer, w, h, RGB565), x, y)
        self.display.update()


class PrestoDisplay(PicoGraphicsDisplay):
    """Display that wraps a Pimoroni Presto Picographics display."""

    def __init__(self, presto):
        super().__init__(presto.display)
        self.presto = presto

    def blit(self, buffer, x, y, w, h):
        super().blit(buffer, x, y, w, h)
        self.presto.update()

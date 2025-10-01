# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

"""Example tempe_config file for PicoGraphics-based displays.

This example assumes you have the Pimoroni firmware installed on your
device.
"""
from array import array
from framebuf import FrameBuffer, RGB565
from picographics import PicoGraphics
from presto import Presto

from tempe.display import Display


class PicoGraphicsDisplay(Display):
    """Display that wraps a Pimoroni PicoGraphics display.

    This should work for any device which can support RGB565 color.
    """

    def __init__(self, display: PicoGraphics): ...

    def blit(self, buffer: array, x: int, y: int, w: int, h: int): ...


class PrestoDisplay(PicoGraphicsDisplay):
    """Display that wraps a Pimoroni Presto Picographics display."""

    def __init__(self, presto: Presto): ...

    def blit(self, buffer: array, x: int, y: int, w: int, h: int): ...

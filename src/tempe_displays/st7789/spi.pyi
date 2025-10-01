# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

"""Generic support for SPI-based ST7789 screens."""

from collections.abc import Iterable, Iterator
from machine import SPI, Pin

from .base import ST7789


class ST7789_SPI(ST7789):
    """Generic support for SPI-based ST7789 screens."""

    spi: SPI

    cs_pin: Pin

    dc_pin: Pin

    def __init__(
        self,
        spi: SPI | None = None,
        cs_pin: int | Pin = 17,
        dc_pin: int | Pin = 16,
        size: tuple[int, int] = (320, 240),
        reset_pin: int | Pin | None = None,
    ): ...

    def send(self, dc: int, buf: Iterable[int]) -> None:
        """Send bytes to the device via SPI"""

    def send_iterator(self, dc, buf_iter: Iterator[int]) -> None:
        """Send iterated bytes to the device via SPI"""

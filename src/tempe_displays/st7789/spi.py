# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

"""Generic support for SPI-based ST7789 screens."""

from machine import SPI, Pin

from .base import ST7789


class ST7789_SPI(ST7789):
    """Generic support for SPI-based ST7789 screens."""

    spi: SPI

    cs_pin: Pin

    dc_pin: Pin

    def __init__(self, spi, cs_pin, dc_pin, size=(320, 240), reset_pin=None):
        super().__init__(size, reset_pin)
        self.spi = spi
        self.cs_pin = cs_pin
        self.dc_pin = dc_pin

    def send(self, dc, buf):
        """Send bytes to the device via SPI"""
        if buf:
            self.cs_pin(0)
            self.dc_pin(dc)
            self.spi.write(buf)
            self.cs_pin(1)

    def send_iterator(self, dc, buf_iter):
        """Send to the display."""
        write = self.spi.write
        self.cs_pin(0)
        self.dc_pin(dc)
        for buf in buf_iter:
            if buf:
                write(buf)
        self.cs_pin(1)

# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

from typing import Any, Literal

from machine import SPI, Pin

from .spi import ST7789_SPI


class PimoroniDisplay(ST7789_SPI):
    """Various Pimoroni SPI ST7780 SPI displays.

    This should work for the Pimoroni Pico W Explorer, Pico Display
    Pack 2.0/2.8, Pimoroni Explorer 2, SPI Breakout Garden LCD, etc.
    """

    def __init__(
        self,
        spi: SPI | None = None,
        cs_pin: int | Pin = 17,
        dc_pin: int | Pin = 16,
        backlight_pin: int | Pin =20,
        size: tuple[int, int] = (320, 240),
        centered: bool = False,
        reset_pin: int | Pin | None = None,
    ) -> None: ...

    async def init(self, rotation: Literal[0, 90, 180, 270] = 0) -> None: ...

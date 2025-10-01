# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

from typing import Literal

from machine import SPI, Pin

from .base import MADCTL_MV, MADCTL_MX, MADCTL_MY, MADCTL_MH
from .spi import ST7789_SPI


class PicoResTouchDisplay(ST7789_SPI):
    """Waveshare Pico-ResTouch-LCD-2.8.

    This should work for any other Waveshare devices with similar pinouts.
    See: https://github.com/orgs/micropython/discussions/16194
    """

    def __init__(
        self,
        spi: SPI | None = None,
        cs_pin: int | Pin = 17,
        dc_pin: int | Pin = 16,
        backlight_pin: int | Pin =20,
        size: tuple[int, int] = (320, 240),
        reset_pin: int | Pin | None = 15,
    ) -> None: ...

    async def init(self, rotation: Literal[0, 90, 180, 270] = 0) -> None: ...

# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

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
        spi=None,
        cs_pin=9,
        dc_pin=8,
        backlight_pin=13,
        size=(320, 240),
        reset_pin=15,
    ):
        if spi is None:
            spi = SPI(
                0,
                baudrate=62_500_000,
                phase=1,
                polarity=1,
                sck=Pin(10, Pin.OUT),
                mosi=Pin(11, Pin.OUT),
            )
        if isinstance(cs_pin, int):
            cs_pin = Pin(cs_pin, Pin.OUT, value=1)
        if isinstance(dc_pin, int):
            dc_pin = Pin(dc_pin, Pin.OUT)
        if isinstance(backlight_pin, int):
            backlight_pin = Pin(backlight_pin, Pin.OUT)
        self.backlight_pin = backlight_pin
        super().__init__(spi, cs_pin, dc_pin, size, reset_pin)

    async def init(self, rotation=0):
        await super().init()
        self.set_power_control_1(0xA4, 0xA1)
        self.set_frame_rate_control(0x0F)  # turn it way down ~39 fps

        # Same as PicoDisplay, but work: https://github.com/orgs/micropython/discussions/16194
        self.set_gate_control(0x35)
        self.set_vcom(0x1F)
        self.set_positive_gamma(
            b"\xD0\x08\x11\x08\x0C\x15\x39\x33\x50\x36\x13\x14\x29\x2D"
        )
        self.set_negative_gamma(
            b"\xD0\x08\x10\x08\x06\x06\x39\x44\x51\x0B\x16\x14\x2F\x31"
        )
        if self.size == (240, 360):
            # portrait
            rotation = (rotation + 90) % 360
        if rotation in {90, 270}:
            self.size = (240, 320)
        else:
            self.size = (320, 240)

        await self.inversion(True)
        await self.sleep(False)
        await self.normal_on()

        if rotation == 90:
            self.memory_data_access_control(MADCTL_MH | MADCTL_MX | MADCTL_MY)
            self.x_offset = 240 - self.size[0]
            self.y_offset = 320 - self.size[1]
        elif rotation == 180:
            self.memory_data_access_control(MADCTL_MH | MADCTL_MV | MADCTL_MY)
            self.x_offset = 320 - self.size[0]
            self.y_offset = 240 - self.size[1]
        elif rotation == 270:
            self.memory_data_access_control(MADCTL_MH)
        else:
            self.memory_data_access_control(MADCTL_MV | MADCTL_MX)

        self.clear()
        await self.display_on()

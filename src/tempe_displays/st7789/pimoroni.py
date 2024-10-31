# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

from machine import SPI, Pin

from .base import MADCTL_MV, MADCTL_MX, MADCTL_MY, MADCTL_MH
from .spi import ST7789_SPI


class PimoroniDisplay(ST7789_SPI):
    """Various Pimoroni SPI ST7780 SPI displays.

    This should work for the Pimoroni Pico W Explorer, Pico Display
    Pack 2.0/2.8, Pimoroni Explorer 2, SPI Breakout Garden LCD, etc.
    """

    def __init__(
        self,
        spi=None,
        cs_pin=17,
        dc_pin=16,
        backlight_pin=20,
        size=(320, 240),
        centered=False,
        reset_pin=None,
    ):
        if spi is None:
            spi = SPI(
                0,
                baudrate=62_500_000,
                phase=1,
                polarity=1,
                sck=Pin(18, Pin.OUT),
                mosi=Pin(19, Pin.OUT),
            )
        if isinstance(cs_pin, int):
            cs_pin = Pin(cs_pin, Pin.OUT, value=1)
        if isinstance(dc_pin, int):
            dc_pin = Pin(dc_pin, Pin.OUT)
        if isinstance(backlight_pin, int):
            backlight_pin = Pin(backlight_pin, Pin.OUT)
        self.backlight_pin = backlight_pin
        # whether the display is centered in ST7789 memory or not
        # this is true for round displays and the original Pico Display Pack
        self.centered = centered
        super().__init__(spi, cs_pin, dc_pin, size, reset_pin)

    async def init(self, rotation=0):
        # Adapted from PicoGraphics code
        # See https://github.com/pimoroni/pimoroni-pico/blob/24971349fcb3f92269c7f469b6c716e568941874/drivers/st7789/st7789.cpp#L49-L118
        await self.soft_reset()
        self.tearing_effect_on(0)
        self.set_color_mode(0x05)
        self.set_porch_control(0x0C, 0x0C, 0x00, 0x33, 0x33)
        self.set_lcm_control(0x2C)
        self.set_vdv_vrh_enable(0x01)
        self.set_vrh(0x12)
        self.set_vdv(0x20)
        self.set_power_control_1(0xA4, 0xA1)
        self.set_frame_rate_control(0x0F)  # turn it way down ~39 fps

        if self.size == (240, 240):
            # Pico SPI 240x240 Display Breakouts (including round display)
            self.set_gate_control(0x14)
            self.set_vcom(0x37)
            self.set_positive_gamma(
                b"\xD0\x04\x0D\x11\x13\x2B\x3F\x54\x4C\x18\x0D\x0B\x1F\x23"
            )
            self.set_negative_gamma(
                b"\xD0\x04\x0C\x11\x13\x2C\x3F\x44\x51\x2F\x1F\x1F\x20\x23"
            )
            # align with printing on device
            rotation = (rotation - 90) % 360
        elif set(self.size) == {320, 240}:
            # Pico Display 2.0/2.8, Pico Explorer W, Pimoroni Explorer
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
        elif set(self.size) == {240, 135}:
            # Pico Display Pack
            self.set_vdv(0x00)
            self.set_gate_control(0x75)
            self.set_vcom(0x3D)
            # PicoGraphics doesn't know why they are setting this undocumented value
            self.command(0xD6)
            self.data(0xA1)
            self.set_positive_gamma(
                b"\x70\x04\x08\x09\x09\x05\x2A\x33\x41\x07\x13\x13\x29\x2f"
            )
            self.set_negative_gamma(
                b"\x70\x03\x09\x0A\x09\x06\x2B\x34\x41\x07\x12\x14\x28\x2E"
            )
            if self.size == (135, 240):
                # sideways
                rotation = (rotation + 90) % 360
            if rotation in {90, 270}:
                self.size = (135, 240)
            else:
                self.size = (240, 135)

        await self.inversion(True)
        await self.sleep(False)
        await self.normal_on()

        if rotation == 90:
            self.memory_data_access_control(MADCTL_MH | MADCTL_MX| MADCTL_MY)
            if self.centered:
                self.x_offset = (240 - self.size[0]) // 2 + (240 - self.size[0]) % 2
                self.y_offset = (320 - self.size[1]) // 2 + (320 - self.size[0]) % 2
            else:
                self.x_offset = 240 - self.size[0]
                self.y_offset = 320 - self.size[1]
        elif rotation == 180:
            self.memory_data_access_control(MADCTL_MH | MADCTL_MV | MADCTL_MY)
            if self.centered:
                self.x_offset = (320 - self.size[0]) // 2
                self.y_offset = (240 - self.size[1]) // 2
            else:
                self.x_offset = 320 - self.size[0]
                self.y_offset = 240 - self.size[1]
        elif rotation == 270:
            self.memory_data_access_control(MADCTL_MH)
            if self.centered:
                self.x_offset = (240 - self.size[0]) // 2
                self.y_offset = (320 - self.size[1]) // 2
        else:
            if self.centered:
                self.x_offset = (320 - self.size[0]) // 2 + (320 - self.size[0]) % 2
                self.y_offset = (240 - self.size[1]) // 2 + (240 - self.size[0]) % 2
            self.memory_data_access_control(MADCTL_MV | MADCTL_MX)

        self.clear()
        await self.display_on()

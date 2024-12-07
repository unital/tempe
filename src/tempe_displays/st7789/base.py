# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

"""Base Display class for ST7789 screens."""

from machine import Pin
import asyncio
from struct import pack


_NOP = const(b"\x00")
_SWRESET = const(b"\x01")
_RDDID = const(b"\x04")
_RDDST = const(b"\x09")

_SLPIN = const(b"\x10")
_SLPOUT = const(b"\x11")
_PTLON = const(b"\x12")
_NORON = const(b"\x13")

_INVOFF = const(b"\x20")
_INVON = const(b"\x21")
_DISPOFF = const(b"\x28")
_DISPON = const(b"\x29")

_CASET = const(b"\x2A")
_RASET = const(b"\x2B")
_RAMWR = const(b"\x2C")
_RAMRD = const(b"\x2E")

_PTLAR = const(b"\x30")
_VSCRDEF = const(b"\x33")
_TEOFF = const(b"\x34")
_TEON = const(b"\x35")
_MADCTL = const(b"\x36")
_VSCSAD = const(b"\x37")
_IDMOFF = const(b"\x38")
_IDMON = const(b"\x39")
_COLMOD = const(b"\x3A")
_WRMEMC = const(b"\x3C")

_STE = const(b"\x44")

_WRDISBV = const(b"\x51")
_WRCTRLD = const(b"\x53")
_WRCACE = const(b"\x55")
_WRCABCMB = const(b"\x5E")

_RAMCTRL = const(b"\xB0")
_RGBCTRL = const(b"\xB1")
_PORCTRL = const(b"\xB2")
_FRMCTR1 = const(b"\xB3")

_GCTRL = const(b"\xB7")
_GTADJ = const(b"\xB8")
_DGMEN = const(b"\xBA")
_VCOMS = const(b"\xBB")
_POWSAVE = const(b"\xBC")
_DLPOFFSAVE = const(b"\xBD")

_LCMCTRL = const(b"\xC0")
_IDSET = const(b"\xC1")
_VDVVRHEN = const(b"\xC2")
_VRHS = const(b"\xC3")
_VDVS = const(b"\xC4")
_VCMOFSET = const(b"\xC5")
_FRCTRL2 = const(b"\xC6")
_CABCCTRL = const(b"\xC7")

_PWCTRL1 = const(b"\xD0")
_RDID1 = const(b"\xDA")
_RDID2 = const(b"\xDB")
_RDID3 = const(b"\xDC")
_RDID4 = const(b"\xDD")

_PVGAMCTRL = const(b"\xE0")
_NVGAMCTRL = const(b"\xE1")

_NVMSET = const(b"\xFC")

# COLMOD Flags
COLMOD_65K = const(0x05)
COLMOD_262K = const(0x06)
COLMOD_12bit = const(0x03)
COLMOD_16bit = const(0x05)
COLMOD_18bit = const(0x06)
COLMOD_16M = const(0x07)

# MADCTL command flags
MADCTL_MY = const(0x80)
MADCTL_MX = const(0x40)
MADCTL_MV = const(0x20)
MADCTL_ML = const(0x10)
MADCTL_BGR = const(0x08)
MADCTL_MH = const(0x04)
MADCTL_RGB = const(0x00)


class ST7789:
    """Base class for ST7789-based displays"""

    reset_pin: Pin | None

    def __init__(self, size, reset_pin=None):
        self.size = size
        if isinstance(reset_pin, int):
            reset_pin = Pin(reset_pin, Pin.OUT, value=True)
        self.reset_pin = reset_pin
        self.x_offset = 0
        self.y_offset = 0

    def send(self, dc, buf):
        """Send to the display."""
        raise NotImplementedError()

    def send_iterator(self, dc, buf_iter):
        """Send to the display."""
        raise NotImplementedError()

    def command(self, command):
        """Send a command to the display."""
        self.send(0, command)

    def data(self, data):
        """Send data to the display."""
        self.send(1, data)

    async def reset(self):
        """Perform a hard reset of the screen, if available."""
        if self.reset_pin is not None:
            self.reset_pin(False)
            await asyncio.sleep(0.500)
            self.reset_pin(True)
            await asyncio.sleep(0.500)

    async def soft_reset(self):
        """Perform a soft reset of the screen."""
        self.command(_SWRESET)
        await asyncio.sleep(0.150)

    async def sleep_in(self):
        """Enter minimum power consumption mode."""
        self.command(_SLPIN)
        await asyncio.sleep(0.005)

    async def sleep_out(self):
        """Exit minimum power consumption mode."""
        self.command(_SLPOUT)
        await asyncio.sleep(0.005)

    async def partial_on(self):
        """Enter partial mode."""
        self.command(_PTLON)
        await asyncio.sleep(0.010)

    async def normal_on(self):
        """Exit partial mode."""
        self.command(_NORON)
        await asyncio.sleep(0.010)

    async def inverse_off(self):
        """Exit display inversion mode."""
        self.command(_INVOFF)
        await asyncio.sleep(0.010)

    async def inverse_on(self):
        """Enter display inversion mode."""
        self.command(_INVON)
        await asyncio.sleep(0.010)

    async def display_on(self):
        """Turn the display on."""
        self.command(_DISPON)
        await asyncio.sleep(0.5)

    async def display_off(self):
        """Turn the display off."""
        self.command(_DISPOFF)
        await asyncio.sleep(0.5)

    def set_column_address(self, start, end):
        """Set the column range for writing."""
        self.command(_CASET)
        self.data(pack(">HH", start & 0xFFFF, end & 0xFFFF))

    def set_row_address(self, start, end):
        """Set the row range for writing."""
        self.command(_RASET)
        self.data(pack(">HH", start & 0xFFFF, end & 0xFFFF))

    def write_to_memory(self, buf):
        """Write data to memory."""
        self.command(_RAMWR)
        self.data(buf)

    def partial_area(self, start, end):
        """Define partial mode's area."""
        self.command(_PTLAR)
        self.data(pack(">HH", start & 0xFFFF, end & 0xFFFF))

    def vertical_scroll_area(self, top, height, bottom):
        """Define vertical scroll area."""
        self.command(_VSCRDEF)
        self.data(pack(">HHH", top & 0xFFFF, height & 0xFFFF, bottom & 0xFFFF))

    def tearing_effect_off(self):
        """Turn tearing effect line off."""
        self.command(_TEOFF)

    def tearing_effect_on(self, horizontal_blanking=False):
        """Turn tearing effect line on."""
        self.command(_TEON)
        self.data(bytes([horizontal_blanking]))

    def memory_data_access_control(self, parameter):
        """Set memory data access parameters."""
        self.command(_MADCTL)
        self.data(bytes([parameter]))

    def vertical_scroll_start_address(self, start):
        """Set the start address of the vertical scroll area."""
        self.command(_VSCSAD)
        self.data(pack(">H", start & 0xFFFF))

    def idle_mode_off(self):
        """Turn idle mode off."""
        self.command(_IDMOFF)

    def idle_mode_on(self):
        """Turn idle mode on."""
        self.command(_IDMON)

    def set_color_mode(self, parameter):
        """Set the color mode."""
        self.command(_COLMOD)
        self.data(bytes([parameter]))

    def write_to_memory_continue(self, buf):
        """Continue writing data to memory from last pixel location."""
        self.command(_WRMEMC)
        self.data(buf)

    def set_tear_scanline(self, start):
        """Set the tear scanline start."""
        self.command(_STE)
        self.data(pack(">H", start & 0xFFFF))

    def write_display_brightness(self, parameter):
        self.command(_WRDISBV)
        self.data(bytes([parameter]))

    def write_ctrl_display(self, parameter):
        self.command(_WRCTRLD)
        self.data(bytes([parameter]))

    def write_adaptive_enhancement(self, parameter):
        self.command(_WRCACE)
        self.data(bytes([parameter]))

    def write_adaptive_minimum_brightness(self, parameter):
        self.command(_WRCABCMB)
        self.data(bytes([parameter]))

    def set_ram_control(self, parameter_1, parameter_2):
        self.command(_RAMCTRL)
        self.data(bytes([parameter_1, parameter_2]))

    def set_rgb_control(self, parameter_1, parameter_2, parameter_3):
        self.command(_RGBCTRL)
        self.data(bytes([parameter_1, parameter_2, parameter_3]))

    def set_porch_control(
        self, parameter_1, parameter_2, parameter_3, parameter_4, parameter_5
    ):
        self.command(_PORCTRL)
        self.data(
            bytes([parameter_1, parameter_2, parameter_3, parameter_4, parameter_5])
        )

    def set_lcm_control(self, parameter_1):
        self.command(_LCMCTRL)
        self.data(bytes([parameter_1]))

    def set_vdv_vrh_enable(self, parameter_1):
        self.command(_VDVVRHEN)
        self.data(bytes([parameter_1, 0xFF]))

    def set_vrh(self, parameter_1):
        self.command(_VRHS)
        self.data(bytes([parameter_1]))

    def set_vdv(self, parameter_1):
        self.command(_VDVS)
        self.data(bytes([parameter_1]))

    def set_frame_control_1(self, parameter_1, parameter_2, parameter_3):
        self.command(_FRMCTR1)
        self.data(bytes([parameter_1, parameter_2, parameter_3]))

    def set_frame_rate_control(self, parameter_1):
        self.command(_FRCTRL2)
        self.data(bytes([parameter_1]))

    def set_power_control_1(self, parameter_1, parameter_2):
        self.command(_PWCTRL1)
        self.data(bytes([parameter_1, parameter_2]))

    def set_gate_control(self, parameter_1):
        self.command(_GCTRL)
        self.data(bytes([parameter_1]))

    def set_vcom(self, parameter_1):
        self.command(_VCOMS)
        self.data(bytes([parameter_1]))

    def set_gate_adjustment(self, parameter_1, parameter_2, parameter_3, parameter_4):
        self.command(_GTADJ)
        self.data(bytes([parameter_1, parameter_2, parameter_3, parameter_4]))

    def set_positive_gamma(self, curve):
        self.command(_PVGAMCTRL)
        self.data(curve)

    def set_negative_gamma(self, curve):
        self.command(_NVGAMCTRL)
        self.data(curve)

    async def sleep(self, value):
        if value:
            await self.sleep_in()
        else:
            await self.sleep_out()

    async def inversion(self, value):
        if value:
            await self.inverse_on()
        else:
            await self.inverse_off()

    def window(self, x, y, w, h):
        self.set_column_address(self.x_offset + x, self.x_offset + x + w - 1)
        self.set_row_address(self.y_offset + y, self.y_offset + y + h - 1)

    def clear(self):
        self.fill(0, 0, self.size[0], self.size[1], b"\x00\x00")

    def fill(self, x, y, w, h, color=b"\xff\xff"):
        self.window(x, y, w, h)
        row_bytes = color * w
        write = self.spi.write
        self.write_to_memory(b"")
        self.send_iterator(1, (row_bytes for _ in range(h)))

    async def init(self):
        await self.soft_reset()
        self.tearing_effect_on(0)
        self.set_color_mode(0x05)
        self.set_porch_control(0x0C, 0x0C, 0x00, 0x33, 0x33)
        self.set_lcm_control(0x2C)
        self.set_vdv_vrh_enable(0x01)
        self.set_vrh(0x12)
        self.set_vdv(0x20)

    def blit(self, buf, x, y, w, h, stride=None):
        self._blit565(buf, x, y, w, h, stride)

    def _blit565(self, buf, x, y, w, h, stride=None):
        """Transfer a 565 buffer to the display."""
        buf = memoryview(buf)
        self.window(x, y, w, h)
        if stride is None:
            # fast path for contiguous memory
            self.write_to_memory(buf[: 2 * w * h])
        else:
            buf = memoryview(buf)
            self.window(x, y, w, h)
            self.write_to_memory(b"")
            self.send_iterator(
                1,
                (
                    buf[offset : offset + 2 * w]
                    for offset in range(0, 2 * stride * h, 2 * stride)
                ),
            )

from machine import SPI, Pin
import uasyncio
import utime
from struct import pack
import array
import framebuf

NOP = const(b"\x00")
SWRESET = const(b"\x01")
RDDID = const(b"\x04")
RDDST = const(b"\x09")

SLPIN = const(b"\x10")
SLPOUT = const(b"\x11")
PTLON = const(b"\x12")
NORON = const(b"\x13")

INVOFF = const(b"\x20")
INVON = const(b"\x21")
DISPOFF = const(b"\x28")
DISPON = const(b"\x29")

CASET = const(b"\x2A")
RASET = const(b"\x2B")
RAMWR = const(b"\x2C")
RAMRD = const(b"\x2E")

PTLAR = const(b"\x30")
VSCRDEF = const(b"\x33")
TEOFF = const(b"\x34")
TEON = const(b"\x35")
MADCTL = const(b"\x36")
VSCSAD = const(b"\x37")
IDMOFF = const(b"\x38")
IDMON = const(b"\x39")
COLMOD = const(b"\x3A")
WRMEMC = const(b"\x3C")

STE = const(b"\x44")

WRDISBV = const(b"\x51")
WRCTRLD = const(b"\x53")
WRCACE = const(b"\x55")
WRCABCMB = const(b"\x5E")

RAMCTRL = const(b"\xB0")
RGBCTRL = const(b"\xB1")
PORCTRL = const(b"\xB2")
FRMCTR1 = const(b"\xB3")

GCTRL = const(b"\xB7")
GTADJ = const(b"\xB8")
DGMEN = const(b"\xBA")
VCOMS = const(b"\xBB")
POWSAVE = const(b"\xBC")
DLPOFFSAVE = const(b"\xBD")

LCMCTRL = const(b"\xC0")
IDSET = const(b"\xC1")
VDVVRHEN = const(b"\xC2")
VRHS = const(b"\xC3")
VDVS = const(b"\xC4")
VCMOFSET = const(b"\xC5")
FRCTRL2 = const(b"\xC6")
CABCCTRL = const(b"\xC7")

PWCTRL1 = const(b"\xD0")
RDID1 = const(b"\xDA")
RDID2 = const(b"\xDB")
RDID3 = const(b"\xDC")
RDID4 = const(b"\xDD")

PVGAMCTRL = const(b"\xE0")
NVGAMCTRL = const(b"\xE1")

NVMSET = const(b"\xFC")

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

    spi: SPI

    cs_pin: Pin

    dc_pin: Pin

    reset_pin: Pin

    def __init__(self, spi, cs_pin, dc_pin, reset_pin=None):
        self.spi = spi
        self.cs_pin = cs_pin
        self.dc_pin = dc_pin
        self.size = (320, 240)

    def send(self, dc, buf):
        if buf:
            self.cs_pin(0)
            self.dc_pin(dc)
            self.spi.write(buf)
            self.cs_pin(1)

    def command(self, command):
        self.send(0, command)

    def data(self, data):
        self.send(1, data)

    async def reset(self):
        """Perform a hard reset of the screen, if available."""
        if self.reset_pin is not None:
            self.reset_pin(True)
            uasyncio.sleep(0.500)
            self.reset_pin(False)
            uasyncio.sleep(0.500)
            self.reset_pin(True)
            uasyncio.sleep(0.500)

    async def soft_reset(self):
        """Perform a soft reset of the screen."""
        self.command(SWRESET)
        await uasyncio.sleep(0.150)

    async def sleep_in(self):
        """Enter minimum power consumption mode."""
        self.command(SLPIN)
        await uasyncio.sleep(0.005)

    async def sleep_out(self):
        """Exit minimum power consumption mode."""
        self.command(SLPOUT)
        await uasyncio.sleep(0.005)

    async def partial_on(self):
        """Enter partial mode."""
        self.command(PTLON)
        await uasyncio.sleep(0.010)

    async def normal_on(self):
        """Exit partial mode."""
        self.command(NORON)
        await uasyncio.sleep(0.010)

    async def inverse_off(self):
        """Exit display inversion mode."""
        self.command(INVOFF)
        await uasyncio.sleep(0.010)

    async def inverse_on(self):
        """Enter display inversion mode."""
        self.command(INVON)
        await uasyncio.sleep(0.010)

    async def display_on(self):
        """Turn the display on."""
        self.command(DISPON)
        await uasyncio.sleep(0.5)

    async def display_off(self):
        """Turn the display off."""
        self.command(DISPOFF)
        await uasyncio.sleep(0.5)

    def set_column_address(self, start, end):
        """Set the column range for writing."""
        self.command(CASET)
        self.data(pack(">HH", start & 0xFFFF, end & 0xFFFF))

    def set_row_address(self, start, end):
        """Set the row range for writing."""
        self.command(RASET)
        self.data(pack(">HH", start & 0xFFFF, end & 0xFFFF))

    def write_to_memory(self, buf):
        """Write data to memory."""
        self.command(RAMWR)
        self.data(buf)

    def partial_area(self, start, end):
        """Define partial mode's area."""
        self.command(PTLAR)
        self.data(pack(">HH", start & 0xFFFF, end & 0xFFFF))

    def vertical_scroll_area(self, top, height, bottom):
        """Define vertical scroll area."""
        self.command(VSCRDEF)
        self.data(pack(">HHH", top & 0xFFFF, height & 0xFFFF, bottom & 0xFFFF))

    def tearing_effect_off(self):
        """Turn tearing effect line off."""
        self.command(TEOFF)

    def tearing_effect_on(self, horizontal_blanking=False):
        """Turn tearing effect line on."""
        self.command(TEON)
        self.data(bytes([horizontal_blanking]))

    def memory_data_access_control(self, parameter):
        """Set memory data access parameters."""
        self.command(MADCTL)
        self.data(bytes([parameter]))

    def vertical_scroll_start_address(self, start):
        """Set the start address of the vertical scroll area."""
        self.command(VSCSAD)
        self.data(pack(">H", start & 0xFFFF))

    def idle_mode_off(self):
        """Turn idle mode off."""
        self.command(IDMOFF)

    def idle_mode_on(self):
        """Turn idle mode on."""
        self.command(IDMON)

    def set_color_mode(self, parameter):
        """Set the color mode."""
        self.command(COLMOD)
        self.data(bytes([parameter]))

    def write_to_memory_continue(self, buf):
        """Continue writing data to memory from last pixel location."""
        self.command(WRMEMC)
        self.data(buf)

    def set_tear_scanline(self, start):
        """Set the tear scanline start."""
        self.command(STE)
        self.data(pack(">H", start & 0xFFFF))

    def write_display_brightness(self, parameter):
        self.command(WRDISBV)
        self.data(bytes([parameter]))

    def write_ctrl_display(self, parameter):
        self.command(WRCTRLD)
        self.data(bytes([parameter]))

    def write_adaptive_enhancement(self, parameter):
        self.command(WRCACE)
        self.data(bytes([parameter]))

    def write_adaptive_minimum_brightness(self, parameter):
        self.command(WRCABCMB)
        self.data(bytes([parameter]))

    def set_ram_control(self, parameter_1, parameter_2):
        self.command(RAMCTRL)
        self.data(bytes([parameter_1, parameter_2]))

    def set_rgb_control(self, parameter_1, parameter_2, parameter_3):
        self.command(RGBCTRL)
        self.data(bytes([parameter_1, parameter_2, parameter_3]))

    def set_porch_control(
        self, parameter_1, parameter_2, parameter_3, parameter_4, parameter_5
    ):
        self.command(PORCTRL)
        self.data(
            bytes([parameter_1, parameter_2, parameter_3, parameter_4, parameter_5])
        )

    def set_lcm_control(self, parameter_1):
        self.command(LCMCTRL)
        self.data(bytes([parameter_1]))

    def set_vdv_vrh_enable(self, parameter_1):
        self.command(VDVVRHEN)
        self.data(bytes([parameter_1, 0xFF]))

    def set_vrh(self, parameter_1):
        self.command(VRHS)
        self.data(bytes([parameter_1]))

    def set_vdv(self, parameter_1):
        self.command(VDVS)
        self.data(bytes([parameter_1]))

    def set_frame_control_1(self, parameter_1, parameter_2, parameter_3):
        self.command(FRMCTR1)
        self.data(bytes([parameter_1, parameter_2, parameter_3]))

    def set_frame_rate_control(self, parameter_1):
        self.command(FRCTRL2)
        self.data(bytes([parameter_1]))

    def set_power_control_1(self, parameter_1, parameter_2):
        self.command(PWCTRL1)
        self.data(bytes([parameter_1, parameter_2]))

    def set_gate_control(self, parameter_1):
        self.command(GCTRL)
        self.data(bytes([parameter_1]))

    def set_vcom(self, parameter_1):
        self.command(VCOMS)
        self.data(bytes([parameter_1]))

    def set_gate_adjustment(self, parameter_1, parameter_2, parameter_3, parameter_4):
        self.command(GTADJ)
        self.data(bytes([parameter_1, parameter_2, parameter_3, parameter_4]))

    def set_positive_gamma(self, curve):
        self.command(PVGAMCTRL)
        self.data(curve)

    def set_negative_gamma(self, curve):
        self.command(NVGAMCTRL)
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
        self.set_column_address(x, x + w - 1)
        self.set_row_address(y, y + h - 1)

    async def init(self):
        await self.soft_reset()
        self.tearing_effect_on(0)
        self.set_color_mode(0x05)
        self.set_porch_control(0x0C, 0x0C, 0x00, 0x33, 0x33)
        self.set_lcm_control(0x2C)
        self.set_vdv_vrh_enable(0x01)
        self.set_vrh(0x12)
        self.set_vdv(0x20)
        self.set_power_control_1(0xA4, 0xA1)
        self.set_frame_rate_control(0x1F)  # turn it way down ~39 fps

        self.set_gate_control(0x35)
        self.set_vcom(0x1F)
        self.set_positive_gamma(
            b"\xD0\x08\x11\x08\x0C\x15\x39\x33\x50\x36\x13\x14\x29\x2D"
        )
        self.set_negative_gamma(
            b"\xD0\x08\x10\x08\x06\x06\x39\x44\x51\x0B\x16\x14\x2F\x31"
        )

        await self.inversion(True)
        await self.sleep(False)
        await self.normal_on()

        self.memory_data_access_control(MADCTL_MV | MADCTL_MX)
        self.clear()
        await self.display_on()

    def clear(self):
        self.fill(0, 0, self.size[0], self.size[1], b"\x00\x00")

    def fill(self, x, y, w, h, color=b"\xff\xff"):
        self.window(x, y, w, h)
        row_bytes = color * w
        write = self.spi.write
        self.write_to_memory(b"")
        start = utime.ticks_us()
        self.cs_pin(0)
        self.dc_pin(1)
        for _ in range(h):
            write(row_bytes)
        self.cs_pin(1)

    def hline(self, x, y, length, color=b"\xff\xff"):
        self.fill(x, y, length, 1, color)

    def vline(self, x, y, length, color=b"\xff\xff"):
        self.fill(x, y, 1, length, color)

    def _blit565(self, buf, x, y, w, h, stride=None):
        """Transfer a 565 buffer to the display (one row at a time)."""
        if stride is None:
            stride = w
        buf = memoryview(buf)
        write = self.spi.write
        self.window(x, y, w, h)
        self.write_to_memory(b"")
        start = utime.ticks_us()
        self.cs_pin(0)
        self.dc_pin(1)
        offset = 0
        for i in range(h):
            write(buf[offset : offset + w])
            offset += stride
        #         write(buf)
        self.cs_pin(1)

    def blit(self, buf, x, y, w, h, stride=None):
        self._blit565(buf, x, y, w, h, stride)

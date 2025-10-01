# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

"""Base Display class for ST7789 screens."""

from collections.abc import Iterable, Iterator, Sequence
from machine import Pin
from micropython import const
import asyncio
from struct import pack
from typing import Literal

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

    reset_pin: Pin

    def __init__(self, size:tuple[int, int], reset_pin: Pin | int | None = None): ...

    def send(self, dc: int, buf: Iterable[int]) -> None:
        """Send to the display."""

    def send_iterator(self, dc, buf_iter: Iterator[int]) -> None:
        """Send to the display."""

    def command(self, command: int) -> None:
        """Send a command to the display."""

    def data(self, data: Iterable[int]) -> None:
        """Send data to the display."""

    async def reset(self) -> None:
        """Perform a hard reset of the screen, if available."""

    async def soft_reset(self) -> None:
        """Perform a soft reset of the screen."""

    async def sleep_in(self) -> None:
        """Enter minimum power consumption mode."""

    async def sleep_out(self) -> None:
        """Exit minimum power consumption mode."""

    async def partial_on(self) -> None:
        """Enter partial mode."""

    async def normal_on(self) -> None:
        """Exit partial mode."""

    async def inverse_off(self) -> None:
        """Exit display inversion mode."""

    async def inverse_on(self) -> None:
        """Enter display inversion mode."""

    async def display_on(self) -> None:
        """Turn the display on."""

    async def display_off(self) -> None:
        """Turn the display off."""

    def set_column_address(self, start: int, end: int) -> None:
        """Set the column range for writing."""

    def set_row_address(self, start: int, end: int) -> None:
        """Set the row range for writing."""

    def write_to_memory(self, buf: Iterable[int]) -> None:
        """Write data to memory."""

    def partial_area(self, start: int, end: int) -> None:
        """Define partial mode's area."""

    def vertical_scroll_area(self, top: int, height: int, bottom: int) -> None:
        """Define vertical scroll area."""

    def tearing_effect_off(self) -> None:
        """Turn tearing effect line off."""

    def tearing_effect_on(self, horizontal_blanking: bool = False) -> None:
        """Turn tearing effect line on."""

    def memory_data_access_control(self, parameter: int) -> None:
        """Set memory data access parameters."""

    def vertical_scroll_start_address(self, start: int) -> None:
        """Set the start address of the vertical scroll area."""

    def idle_mode_off(self) -> None:
        """Turn idle mode off."""

    def idle_mode_on(self) -> None:
        """Turn idle mode on."""

    def set_color_mode(self, parameter: int) -> None:
        """Set the color mode."""

    def write_to_memory_continue(self, buf: int) -> None:
        """Continue writing data to memory from last pixel location."""

    def set_tear_scanline(self, start: int) -> None:
        """Set the tear scanline start."""

    def write_display_brightness(self, parameter: int) -> None: ...

    def write_ctrl_display(self, parameter: int) -> None: ...

    def write_adaptive_enhancement(self, parameter: int) -> None: ...

    def write_adaptive_minimum_brightness(self, parameter: int) -> None: ...

    def set_ram_control(self, parameter_1: int, parameter_2: int) -> None: ...

    def set_rgb_control(self, parameter_1: int, parameter_2: int, parameter_3: int) -> None: ...

    def set_porch_control(
        self, parameter_1: int, parameter_2: int, parameter_3: int, parameter_4: int, parameter_5: int
    ) -> None: ...

    def set_lcm_control(self, parameter_1: int) -> None: ...

    def set_vdv_vrh_enable(self, parameter_1: int) -> None: ...

    def set_vrh(self, parameter_1: int) -> None: ...

    def set_vdv(self, parameter_1: int) -> None: ...

    def set_frame_control_1(self, parameter_1: int, parameter_2: int, parameter_3: int) -> None: ...

    def set_frame_rate_control(self, parameter_1: int) -> None: ...

    def set_power_control_1(self, parameter_1: int, parameter_2: int) -> None: ...

    def set_gate_control(self, parameter_1: int) -> None: ...

    def set_vcom(self, parameter_1: int) -> None: ...

    def set_gate_adjustment(self, parameter_1: int, parameter_2: int, parameter_3: int, parameter_4: int) -> None: ...

    def set_positive_gamma(self, curve: Iterable[int]) -> None: ...

    def set_negative_gamma(self, curve: Iterable[int]) -> None: ...

    async def sleep(self, value: bool) -> None: ...

    async def inversion(self, value: bool) -> None: ...

    def window(self, x: int, y: int, w: int, h: int) -> None: ...

    def clear(self) -> None: ...

    def fill(self, x: int, y: int, w: int, h: int, color=b"\xff\xff") -> None: ...

    async def init(self, rotation: Literal[0, 90, 180, 270] = 0) -> None: ...

    def blit(self, buf: Sequence[int], x: int, y: int, w: int, h: int, stride: int | None = None) -> None: ...

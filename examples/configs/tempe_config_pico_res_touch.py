# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

"""Example tempe_config file for Waveshare PicoResTouch display.
"""

from tempe_displays.st7789.waveshare import PicoResTouchDisplay


# Change to match the characteristics of your display
SIZE = (320, 240)  # or (240, 320)
ROTATION = 0  # or 90, 180, 270


async def init_display():
    display = PicoResTouchDisplay(size=SIZE)
    await display.init(ROTATION)
    display.backlight_pin(1)
    return display

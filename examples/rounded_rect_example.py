# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

"""Example showing support for rounded rectangles."""

import asyncio

from tempe.colormaps.viridis import viridis
from tempe.data_view import Repeat, Range, Interpolated
from tempe.geometry import ColumnGeometry
from tempe.surface import Surface
from tempe.shapes import Rectangles, RoundedRectangles
from tempe.display import FileDisplay

surface = Surface()

# a buffer one half the size of the screen
working_buffer = bytearray(2 * 320 * 121)

# fill the background with white pixels
background = Rectangles([(0, 0, 320, 240)], [0xFFFF])
surface.add_shape("BACKGROUND", background)


# draw some rectangles
rectangles = RoundedRectangles(
    ColumnGeometry(
        [
            Range(24, 240, 80),
            Repeat(24),
            Range(32, 96, 16),
            Range(64, 16, -16),
        ]
    ),
    Interpolated(viridis, 3),
    fill=True,
)
surface.add_shape("DRAWING", rectangles)

surface.rounded_rectangles(
    "DRAWING",
    ColumnGeometry([
            Range(24, 240, 80),
            Range(96, 48, -16),
            Range(64, 16, -16),
            Range(32, 96, 16),
    ]),
    Interpolated(viridis, 3),
    radius=12,
    fill=False,
)

surface.rounded_rectangles(
    "DRAWING",
    ColumnGeometry([
            Range(24, 240, 80),
            Repeat(160),
            Range(32, 96, 16),
            Range(64, 16, -16),
    ]),
    Interpolated(viridis, 3),
    radius=32,
)

async def init_display():
    from tempe_displays.st7789.pimoroni import PimoroniDisplay as Display
    # or for Waveshare Pico-ResTouch-LCD-28:
    #     from tempe_displays.st7789.waveshare import PicoResTouchDisplay as Display

    display = Display(size=(240, 320))
    display.backlight_pin(1)
    await display.init()
    return display


def main(surface, working_buffer):
    # set up the display object
    display = asyncio.run(init_display())

    # refresh the display
    display.clear()
    surface.refresh(display, working_buffer)


if __name__ == "__main__":

    # if we have an actual screen, use it
    main(surface, working_buffer)

elif __name__ != "__test__":

    # set up the display object
    display = FileDisplay("lines.rgb565", (320, 240))
    # refresh the display
    with display:
        display.clear()
        surface.refresh(display, working_buffer)

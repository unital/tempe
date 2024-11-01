# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

"""Example showing support for thick lines."""

import asyncio
from array import array
import framebuf
import random
import math

from tempe.bitmaps import Bitmaps, ColoredBitmaps
from tempe.colormaps.viridis import viridis
from tempe.colormaps.viridis import viridis
from tempe.data_view import Repeat, Range, Interpolated
from tempe.geometry import RowGeometry, ColumnGeometry
from tempe.surface import Surface
from tempe.shapes import Rectangles
from tempe.lines import WideLines, WidePolyLines
from tempe.display import FileDisplay

random.seed(0)

surface = Surface()

# a buffer one half the size of the screen
working_buffer = bytearray(2 * 320 * 121)

# fill the background with white pixels
background = Rectangles([(0, 0, 320, 240)], [0xFFFF])
surface.add_shape("BACKGROUND", background)


# draw some lines
lines = WideLines(
    ColumnGeometry(
        [Range(8, 96, 8), Repeat(20), Range(8, 184, 16), Repeat(100), Range(1, 11)]
    ),
    Interpolated(viridis, 10),
    clip=(0, 0, 160, 120),
)
surface.add_shape("DRAWING", lines)


# draw some lines in the opposite direction
lines = WideLines(
    ColumnGeometry(
        [
            Range(8, 96, 8) + 160,
            Repeat(100),
            Range(8, 184, 16) + 160,
            Repeat(20),
            Range(1, 11),
        ]
    ),
    Interpolated(viridis, 10),
    clip=(160, 0, 160, 120),
    round=False,
)
surface.add_shape("DRAWING", lines)

# draw some polylines
polylines = WidePolyLines(
    RowGeometry(
        [
            array(
                "h",
                [
                    10 + 30 * i,
                    125,
                    10 + 30 * i,
                    225,
                    15 + 30 * i,
                    225,
                    25 + 30 * i,
                    165,
                    10 + 30 * i,
                    125,
                ]
                + [i + 1],
            )
            for i in range(10)
        ]
    ),
    Interpolated(viridis, 10),
    clip=(0, 120, 320, 120),
)
surface.add_shape("DRAWING", polylines)


async def init_display():
    from tempe_displays.st7789.pimoroni import PimoroniDisplay

    display = PimoroniDisplay(size=(240, 320))
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

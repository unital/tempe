# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

"""Example showing support for thick lines."""

import asyncio
from array import array
import random
import time
import gc

from tempe.colormaps.viridis import viridis
from tempe.colormaps.viridis import viridis
from tempe.data_view import Repeat, Range, Interpolated
from tempe.geometry import RowGeometry, ColumnGeometry
from tempe.surface import Surface
from tempe.shapes import Rectangles
from tempe.lines import WideLines, WidePolyLines

random.seed(0)

# maximize available memory before allocating buffer
gc.collect()

# A buffer one half the size of a 320x240 screen
# NOTE: If you get MemoryErrors, make this smaller
working_buffer = bytearray(2 * 320 * 121)


# create the surface
surface = Surface()

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


def main(display=None):
    """Render the surface and return the display object."""
    if display is None:
        try:
            from tempe_config import init_display

            display = asyncio.run(init_display())
        except ImportError:
            print(
                "Could not find tempe_config.init_display.\n\n"
                "To run examples, you must create a top-level tempe_config module containing\n"
                "an async init_display function that returns a display.\n\n"
                "See https://unital.github.io/tempe more information.\n\n"
                "Defaulting to file-based display.\n"
            )
            from tempe.display import FileDisplay

            display = FileDisplay("lines.rgb565", (320, 240))
            with display:
                display.clear()
                surface.refresh(display, working_buffer)

    start = time.ticks_us()
    surface.refresh(display, working_buffer)
    print(time.ticks_diff(time.ticks_us(), start))
    return display


if __name__ == '__main__':
    display = main()

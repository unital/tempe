# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

"""Example showing basic display of text."""

import time
import asyncio
import gc

from tempe.surface import Surface, BACKGROUND, DRAWING
from tempe.text import Text
from tempe.shapes import Rectangles
from tempe.font import TempeFont
from tempe.fonts import ubuntu16bold


# maximize available memory before allocating buffer
gc.collect()

# A buffer one half the size of a 320x240 screen
# NOTE: If you get MemoryErrors, make this smaller
working_buffer = bytearray(2 * 320 * 121)


# create the surface
surface = Surface()

# fill the background with white pixels
background = Rectangles([(0, 0, 320, 240)], [0xFFFF])
surface.add_shape(BACKGROUND, background)

# draw some black text in the main drawing layer
font = TempeFont(ubuntu16bold)
hello_tempe = Text(
    [(10, 10)], [0x0000], ["Hello Tempe!"], font=font, clip=(0, 0, 120, 60)
)
surface.add_shape(DRAWING, hello_tempe)


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

            display = FileDisplay("hello_world.rgb565", (320, 240))
            with display:
                display.clear()
                surface.refresh(display, working_buffer)

    start = time.ticks_us()
    surface.refresh(display, working_buffer)
    print(time.ticks_diff(time.ticks_us(), start))
    return display


if __name__ == '__main__':
    display = main()

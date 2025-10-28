# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

"""Example showing basic display of text."""

import time
import asyncio
import gc

from tempe.colors import grey_6, grey_a
from tempe.surface import Surface, BACKGROUND, DRAWING
from tempe.text import Text
from tempe.shapes import Rectangles
from tempe.font import TempeFont
from tempe.fonts import ubuntu16
from tempe_components.component import Box, Component, component_style
from tempe_components.label import Label, label_style
from tempe_components.style import Style, StateColor

# maximize available memory before allocating buffer
gc.collect()

# A buffer one half the size of a 320x240 screen
# NOTE: If you get MemoryErrors, make this smaller
working_buffer = bytearray(2 * 320 * 121)


# create the surface
surface = Surface()

# fill the background with white pixels
bounds = (0, 0, 320, 240)

background = Component(
    surface=surface,
    style=component_style,
    box=Box(x=0, y=0, content_width=320, content_height=240),
)

label = Label(
    surface=surface,
    style=Style(
        parent=label_style,
        font=TempeFont(ubuntu16),
        shadow=StateColor(enabled=grey_a),
        border=StateColor(enabled=grey_6),
    ),
    box=Box(x=100, y=100, content_width=100, content_height=50, pad_top=4, pad_left=4, pad_bottom=4, pad_right=4),
    text="Hello Tempe\nComponents",
)

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

            display = FileDisplay("component_example.rgb565", (320, 240))
            with display:
                display.clear()
                surface.refresh(display, working_buffer)

    start = time.ticks_us()
    surface.refresh(display, working_buffer)
    print(time.ticks_diff(time.ticks_us(), start))
    return display


if __name__ == '__main__':
    display = main()

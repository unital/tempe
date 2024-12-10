# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

"""Example showing basic display of text."""

from tempe.surface import Surface
from tempe.text import Text
from tempe.shapes import Rectangles
from tempe.font import TempeFont
from tempe.fonts import ubuntu16bold


# a buffer one half the size of the screen
working_buffer = bytearray(2 * 320 * 121)

surface = Surface()

# fill the background with white pixels
background = Rectangles([(0, 0, 320, 240)], [0xFFFF])
surface.add_shape("BACKGROUND", background)

# draw some black text in the main drawing layer
font = TempeFont(ubuntu16bold)
hello_tempe = Text(
    [(10, 10)], [0x0000], ["Hello Tempe!"], font=font, clip=(0, 0, 120, 60)
)
surface.add_shape("DRAWING", hello_tempe)

if __name__ == '__main__':
    try:
        import asyncio
        from tempe_config import init_display

        display = asyncio.run(init_display())
        surface.refresh(display, working_buffer)

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

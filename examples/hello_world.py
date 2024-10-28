# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

"""Example showing basic display of text."""

from array import array

from tempe.surface import Surface
from tempe.text import Text
from tempe.shapes import Rectangles
from tempe.display import FileDisplay
from tempe.font import TempeFont
from tempe.fonts import roboto16bold


# a buffer one quarter the size of the screen
working_buffer = array("H", bytearray(2 * 320 * 61))

surface = Surface()

# fill the background with white pixels
background = Rectangles([(0, 0, 320, 240)], [0xFFFF])
surface.add_shape("BACKGROUND", background)

# draw some black text in the main drawing layer
font = TempeFont(roboto16bold)
hello_tempe = Text(
    [(10, 10)], [0x0000], ["Hello Tempe!"], font=font, clip=(0, 0, 120, 60)
)
surface.add_shape("DRAWING", hello_tempe)

# set up the display object
display = FileDisplay("hello_world.rgb565", (320, 240))

# refresh the display
with display:
    display.clear()
    surface.refresh(display, working_buffer)

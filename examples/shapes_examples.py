# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

"""Example showing core Tempe Shapes."""

import asyncio
from array import array
import framebuf
import random
import math

from tempe.bitmaps import Bitmaps, ColoredBitmaps
from tempe.colormaps.magma import magma
from tempe.colormaps.viridis import viridis
from tempe.data_view import Repeat, Range, Interpolated
from tempe.geometry import RowGeometry, ColumnGeometry
from tempe.surface import Surface
from tempe.text import Text
from tempe.markers import Marker, Markers
from tempe.shapes import (
    Rectangles,
    Lines,
    HLines,
    VLines,
    Polygons,
    Circles,
    Ellipses,
    BLIT_KEY_RGB565,
)
from tempe.display import FileDisplay
from tempe.font import TempeFont
from tempe.fonts import roboto16bold

random.seed(0)

surface = Surface()

# a buffer one half the size of the screen
working_buffer = bytearray(2 * 320 * 121)

# fill the background with white pixels
background = Rectangles([(0, 0, 320, 240)], [0xFFFF])
surface.add_shape("BACKGROUND", background)

# draw some black text in the main drawing layer
font = TempeFont(roboto16bold)
labels = Text(
    [
        (4, 4),
        (4, 44),
        (4, 84),
        (4, 124),
        (4, 184),
        (164, 4),
        (164, 44),
        (164, 124),
        (164, 184),
    ],
    Repeat(0x0000),
    [
        "Lines",
        "HLines",
        "VLines",
        "Polygons",
        "Circles",
        "Markers",
        "Bitmaps",
        "Rectangles",
        "Ellipses",
    ],
    font=font,
)
surface.add_shape("OVERLAY", labels)

# draw some lines
lines = Lines(
    ColumnGeometry([Range(4, 44, 4), Repeat(20), Range(8, 88, 8), Repeat(40)]),
    Interpolated(magma, 10),
)
surface.add_shape("DRAWING", lines)

# draw some hlines
hlines = HLines(
    ColumnGeometry([Range(4, 44, 4), Range(60, 80, 2), Range(8, 88, 8)]),
    Interpolated(magma, 10),
)
surface.add_shape("DRAWING", hlines)

# draw some vlines
vlines = VLines(
    ColumnGeometry(
        [
            Range(8, 84, 4),
            Repeat(100),
            [random.randint(10, 20) for _ in range(20)],
        ]
    ),
    Interpolated(magma, 20),
)
surface.add_shape("DRAWING", vlines)

# draw some polygons
stars = [
    [
        (
            16 + x + int((16 - 8 * (a % 2)) * math.sin(math.pi * a / 5)),
            160 - int((16 - 8 * (a % 2)) * math.cos(math.pi * a / 5)),
        )
        for a in range(10)
    ]
    for x in range(0, 128, 32)
]
polys = Polygons(
    RowGeometry.from_lists([[x for p in star for x in p] for star in stars[:3]]),
    Interpolated(viridis, 3),
)
surface.add_shape("DRAWING", polys)
outlines = Polygons(
    RowGeometry.from_lists([[x for p in star for x in p] for star in stars]),
    Repeat(0x0000),
    fill=False,
)
surface.add_shape("DRAWING", outlines)

# draw some circles
circles = Circles(
    ColumnGeometry(
        [
            Range(16, 128, 32),
            Repeat(220),
            Range(8, 16, 2),
        ]
    ),
    Interpolated(viridis, 3),
)
surface.add_shape("DRAWING", circles)
circle_outlines = Circles(
    ColumnGeometry(
        [
            Range(16, 128, 32),
            Repeat(220),
            Range(8, 16, 2),
        ]
    ),
    Repeat(0x0000),
    fill=False,
)
surface.add_shape("DRAWING", circle_outlines)

# draw some markers
star = array(
    "h",
    [
        x
        for p in [
            (
                int((8 - 4 * (a % 2)) * math.sin(math.pi * a / 5)),
                -int((8 - 4 * (a % 2)) * math.cos(math.pi * a / 5)),
            )
            for a in range(10)
        ]
        for x in p
    ],
)
smiley = framebuf.FrameBuffer(
    array(
        "B",
        [
            0b00111100,
            0b01111110,
            0b11011011,
            0b11011011,
            0b11111111,
            0b11011011,
            0b01100110,
            0b00111100,
        ],
    ),
    8,
    8,
    framebuf.MONO_HLSB,
)
markers = Markers(
    ColumnGeometry(
        [
            Range(160, 320, 16),
            Repeat(30),
            Range(5, 16, 1),
        ]
    ),
    Interpolated(viridis, 10),
    [
        Marker.PIXEL,
        Marker.CIRCLE,
        Marker.SQUARE,
        Marker.HLINE,
        Marker.VLINE,
        Marker.PLUS,
        Marker.CROSS,
        star,
        smiley,
        "#",
    ],
)
surface.add_shape("DRAWING", markers)

# draw some buffers
t_buf = framebuf.FrameBuffer(bytearray(32 * 32 * 2), 32, 32, framebuf.RGB565)
t_buf.fill(BLIT_KEY_RGB565)
for x in range(2, 30):
    for y in range(2, 8):
        t_buf.pixel(x, y, viridis[32 + 6 * x + 3 * y])
for x in range(13, 19):
    for y in range(8, 30):
        t_buf.pixel(x, y, viridis[32 + 6 * x + 3 * y])

bitmaps = Bitmaps(
    [(164, 60, 32, 32)],
    [t_buf],
    key=BLIT_KEY_RGB565,
)
surface.add_shape("DRAWING", bitmaps)

grey_buf = framebuf.FrameBuffer(bytearray(32 * 32), 32, 32, framebuf.GS8)
grey_buf.fill(0)
for x in range(1, 14):
    for y in range(1, 4):
        grey_buf.pixel(x, y, 32 + 12 * x + 6 * y)
for x in range(6, 9):
    for y in range(4, 15):
        grey_buf.pixel(x, y, 32 + 12 * x + 6 * y)
greyscale = Bitmaps(
    [(196, 60, 16, 16), (196, 76, 16, 16)],
    [grey_buf, grey_buf],
    key=magma[0],
    palette=magma,
)
surface.add_shape("DRAWING", greyscale)

smileys = ColoredBitmaps(
    ColumnGeometry(
        [
            [random.randint(212, 312) for _ in range(20)],
            [random.randint(60, 84) for _ in range(20)],
            Repeat(8),
            Repeat(8),
        ]
    ),
    Interpolated(viridis, 20),
    Repeat(smiley),
)
surface.add_shape("DRAWING", smileys)

colormap = framebuf.FrameBuffer(bytearray(128 * 8), 128, 8, framebuf.GS8)
for x in range(128):
    colormap.vline(x, 0, 8, 2 * x)
v = Bitmaps(
    [(164, 96, 128, 8)],
    [colormap],
    palette=viridis,
)
surface.add_shape("DRAWING", v)
m = Bitmaps(
    [(164, 106, 128, 8)],
    [colormap],
    palette=magma,
)
surface.add_shape("DRAWING", m)

# draw some rectangles
rectangles = Rectangles(
    ColumnGeometry(
        [
            Range(164, 260, 32),
            Repeat(144),
            Range(16, 32, 4),
            Range(32, 16, -4),
        ]
    ),
    Interpolated(viridis, 3),
)
surface.add_shape("DRAWING", rectangles)
rectangles_outlines = Rectangles(
    ColumnGeometry(
        [
            Range(164, 292, 32),
            Repeat(144),
            Range(16, 32, 4),
            Range(32, 16, -4),
        ]
    ),
    Repeat(0x0000),
    fill=False,
)
surface.add_shape("DRAWING", rectangles_outlines)

# draw some ellipses
ellipses = Ellipses(
    ColumnGeometry(
        [
            Range(172, 300, 32),
            Repeat(220),
            Range(8, 16, 2),
            Range(16, 8, -2),
        ]
    ),
    Interpolated(viridis, 3),
)
surface.add_shape("DRAWING", ellipses)
ellipses_outlines = Ellipses(
    ColumnGeometry(
        [
            Range(172, 300, 32),
            Repeat(220),
            Range(8, 16, 2),
            Range(16, 8, -2),
        ]
    ),
    Repeat(0x0000),
    fill=False,
)
surface.add_shape("DRAWING", ellipses_outlines)


async def init_display():
    from tempe_displays.st7789.pimoroni import PimoroniDisplay

    display = PimoroniDisplay(size = (240, 320))
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
    from tempe.display import FileDisplay

    # set up the display object
    display = FileDisplay("shapes.rgb565", (320, 240))

    # refresh the display
    with display:
        display.clear()
        surface.refresh(display, working_buffer)

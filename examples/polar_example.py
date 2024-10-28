# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

"""Example showing support for polar geometries."""

import asyncio
from array import array
import framebuf
import random
import math

from tempe.colors import grey_e, grey_3
from tempe.colormaps.viridis import viridis
from tempe.data_view import Repeat, Range, Interpolated
from tempe.geometry import ColumnGeometry, Extend, RowGeometry
from tempe.polar_geometry import (
    polar_rects,
    polar_point_arrays,
    polar_points,
    polar_r_lines,
)
from tempe.surface import Surface
from tempe.shapes import Rectangles, Polygons, Circles, Lines
from tempe.markers import Markers
from tempe.display import FileDisplay

random.seed(0)

surface = Surface()

# a buffer one quarter the size of the screen
working_buffer = array("H", bytearray(2 * 320 * 61))

# fill the background with white pixels
background = Rectangles([(0, 0, 320, 240)], [0xFFFF])
surface.add_shape("BACKGROUND", background)


# draw a coxcomb plot
circle_grid = Circles(
    ColumnGeometry(
        [
            Repeat(64),
            Repeat(64),
            Range(10, 70, 10),
        ]
    ),
    Repeat(grey_e),
    fill=False,
    clip=(0, 0, 320, 240),
)
surface.add_shape("UNDERLAY", circle_grid)
ray_grid = Lines(
    polar_r_lines(
        64,
        64,
        ColumnGeometry(
            [
                Repeat(0),
                Range(0, 360, 60),
                Repeat(60),
            ]
        ),
    ),
    Repeat(grey_e),
    clip=(0, 0, 320, 240),
)
surface.add_shape("UNDERLAY", ray_grid)
coxcomb = Polygons(
    polar_rects(
        64,
        64,
        ColumnGeometry(
            [Repeat(0), Range(0, 360, 60), [30, 15, 45, 5, 45, 60], Repeat(60)]
        ),
    ),
    Interpolated(viridis, 6),
    clip=(0, 0, 320, 240),
)
surface.add_shape("DRAWING", coxcomb)

# draw a radar plot
circle_grid = Circles(
    ColumnGeometry(
        [
            Repeat(196),
            Repeat(64),
            Range(10, 70, 10),
        ]
    ),
    Repeat(grey_e),
    fill=False,
    clip=(0, 0, 320, 240),
)
surface.add_shape("UNDERLAY", circle_grid)
ray_grid = Lines(
    polar_r_lines(
        196,
        64,
        ColumnGeometry(
            [
                Repeat(0),
                Range(0, 360, 60),
                Repeat(60),
            ]
        ),
    ),
    Repeat(grey_e),
    clip=(0, 0, 320, 240),
)
surface.add_shape("UNDERLAY", ray_grid)
radar = Polygons(
    polar_point_arrays(
        196,
        64,
        RowGeometry.from_lists(
            [
                [30, 0, 15, 60, 45, 120, 5, 180, 45, 240, 60, 300],
                [12, 0, 18, 60, 43, 120, 35, 180, 25, 240, 20, 300],
            ]
        ),
    ),
    Interpolated(viridis, 6),
    fill=False,
    clip=(0, 0, 320, 240),
)
surface.add_shape("DRAWING", radar)
markers = Markers(
    Extend(
        [
            polar_points(
                196,
                64,
                ColumnGeometry(
                    [
                        [30, 15, 45, 5, 45, 60],
                        Range(0, 360, 60),
                    ]
                ),
            ),
            ColumnGeometry([Repeat(24)]),
        ]
    ),
    Repeat(grey_3),
    [f" {x}" for x in [6, 3, 9, 1, 9, 12]],
    clip=(0, 0, 320, 240),
)
surface.add_shape("OVERLAY", markers)

circle_bar = Polygons(
    polar_rects(
        128,
        240 - 64,
        ColumnGeometry(
            [
                Range(24, 60, 12),
                Repeat(-90),
                Repeat(8),
                [240, 320, 100],
            ]
        ),
        decimation=6,
    ),
    Interpolated(viridis, 3),
    clip=(0, 0, 320, 240),
)
surface.add_shape("DRAWING", circle_bar)
circle_bar_ends = Circles(
    Extend(
        [
            polar_points(
                128,
                240 - 64,
                ColumnGeometry(
                    [
                        Range(28, 60, 12),
                        [240 - 90, 320 - 90, 100 - 90],
                    ]
                ),
            ),
            ColumnGeometry([Repeat(4)]),
        ]
    ),
    Interpolated(viridis, 3),
    fill=True,
    clip=(0, 0, 320, 240),
)
surface.add_shape("DRAWING", circle_bar_ends)

values = [6, 3, 9, 1, 9, 12]
cumsum = [sum(values[:i]) for i in range(len(values) + 1)]
angles = [int(values * 360 / cumsum[-1]) for values in cumsum]
deltas = [angles[i + 1] - angles[i] for i in range(len(values))]

donut = Polygons(
    polar_rects(
        256,
        240 - 64,
        ColumnGeometry(
            [
                Repeat(30),
                angles[:-1],
                Repeat(24),
                deltas,
            ]
        ),
        decimation=10,
    ),
    Interpolated(viridis, 6),
    fill=True,
    clip=(0, 0, 320, 240),
)
surface.add_shape("DRAWING", donut)


def main(surface, working_buffer):
    async def init_display():
        from devices.st7789 import ST7789
        from machine import Pin, SPI

        spi = SPI(
            0,
            baudrate=62_500_000,
            phase=1,
            polarity=1,
            sck=Pin(18, Pin.OUT),
            mosi=Pin(19, Pin.OUT),
            miso=Pin(16, Pin.OUT),
        )
        backlight = Pin(20, Pin.OUT)
        display = ST7789(spi, cs_pin=Pin(17, Pin.OUT, value=1), dc_pin=Pin(16, Pin.OUT))
        backlight(1)
        await display.init()
        return display

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
    display = FileDisplay("polar.rgb565", (320, 240))
    # refresh the display
    with display:
        display.clear()
        surface.refresh(display, working_buffer)

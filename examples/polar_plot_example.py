# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

"""Example showing how to build a polar plot from Tempe Shapes."""

from array import array
import asyncio
import gc
import time

from tempe import colors
from tempe.colormaps.viridis import viridis
from tempe.data_view import Repeat
from tempe.geometry import ColumnGeometry, PointsToLines
from tempe.polar_geometry import polar_points, polar_r_lines
from tempe.surface import Surface
from tempe.text import LEFT, CENTER, RIGHT, TOP, BOTTOM


# maximize available memory before allocating buffer
gc.collect()

# A buffer one third the size of a 320x240 screen
# NOTE: If you get MemoryErrors, make this smaller
working_buffer = bytearray(2 * 320 * 81)


# create the surface
surface = Surface()

# fill the background with off-black pixels
surface.rectangles("BACKGROUND", [(0, 0, 320, 240)], [colors.grey_1])


class LinearScale:
    """Object that maps data to screen values linearly."""

    def __init__(self, low_data, low_screen, high_data, high_screen):
        self.low_data = low_data
        self.low_screen = low_screen
        self.high_data = high_data
        self.high_screen = high_screen
        data_range = high_data - low_data
        screen_range = high_screen - low_screen
        self.scale = screen_range / data_range

    def scale_values(self, data):
        """Scale data values to screen values."""
        screen = array("h", bytearray(2 * len(data)))
        low_data = self.low_data
        low_screen = self.low_screen
        scale = self.scale
        for i, value in enumerate(data):
            screen[i] = int(low_screen + scale * (value - low_data))
        return screen


class ColorScale:
    """Object that maps data to color values."""

    def __init__(self, colormap, low_data, low_screen, high_data, high_screen):
        self.colormap = colormap
        self.low_data = low_data
        self.low_screen = low_screen
        self.high_data = high_data
        self.high_screen = high_screen
        data_range = high_data - low_data
        screen_range = high_screen - low_screen
        self.scale = screen_range / data_range

    def scale_values(self, data):
        """Scale data values to screen values."""
        screen = array("h", bytearray(2 * len(data)))
        low_data = self.low_data
        low_screen = self.low_screen
        scale = self.scale
        colormap = self.colormap
        max_color = len(colormap) - 1
        for i, value in enumerate(data):
            screen[i] = colormap[
                max(
                    min(
                        int(low_screen + scale * (value - low_data)),
                        max_color,
                    ),
                    0,
                )
            ]
        return screen


gc.collect()
from data.environmental import timestamps, air_quality

# Plot screen bounds
cx = 160
cy = 120
max_r = 100

# Map the data to polar coordinates
air_quality_scale = LinearScale(0, 0, 150, max_r)
time_scale = LinearScale(1729551600, -90, 1729638000, 270)
color_scale = ColorScale(viridis, 1729500000, 0, 1729500000 + 48 * 60 * 60, 255)

thetas = time_scale.scale_values(timestamps)
line_colors = color_scale.scale_values(timestamps)
quality_rs = air_quality_scale.scale_values(air_quality)

# Create polar line geometry for the data points
quality_lines = PointsToLines(
    polar_points(cx, cy, ColumnGeometry([quality_rs, thetas]))
)
gc.collect()

# draw the plot
surface.lines(
    "DRAWING",
    quality_lines,
    line_colors,
    clip=(cx - max_r, cy - max_r, 2 * max_r + 1, 2 * max_r + 1),
)

quality_label_values = [50, 100, 150]
quality_label_rs = air_quality_scale.scale_values(quality_label_values)
time_label_values = [1729551600 + i * 3600 for i in range(6, 24, 6)]
time_label_strings = ["0:00", "9:00", "12:00", "18:00"]
time_label_alignment = [(CENTER, BOTTOM), (LEFT, CENTER), (CENTER, TOP), (RIGHT, CENTER)]
time_label_xs = [cx, cx + max_r + 4, cx, cx - max_r - 4]
time_label_ys = [cy - max_r - 4, cy, cy + max_r + 4, cy]


surface.circles(
    "BACKGROUND",
    (cx, cy, max_r),
    colors.black,
    clip=(cx - max_r, cy - max_r, 2 * max_r + 1, 2 * max_r + 1),
)
surface.circles(
    "UNDERLAY",
    ColumnGeometry(
        [
            Repeat(cx),
            Repeat(cy),
            quality_label_rs,
        ]
    ),
    colors.grey_3,
    fill=False,
    clip=(cx - max_r, cy - max_r, 2 * max_r + 1, 2 * max_r + 1),
)
surface.lines(
    "UNDERLAY",
    polar_r_lines(
        cx,
        cy,
        ColumnGeometry(
            [
                Repeat(air_quality_scale.scale_values([50])[0]),
                time_scale.scale_values([1729551600 + 3600 * i for i in range(24)]),
                Repeat(int(air_quality_scale.scale * 100)),
            ]
        ),
    ),
    colors.grey_3,
    clip=(cx - max_r, cy - max_r, 2 * max_r + 1, 2 * max_r + 1),
)

quality_label_geometry = polar_points(
    cx, cy, ColumnGeometry([quality_label_rs, Repeat(270)])
)
surface.text(
    "OVERLAY",
    quality_label_geometry,
    colors.grey_7,
    [f"{value:d}" for value in quality_label_values],
    clip=(cx, cy - max_r - 4, 64, 100),
)
time_label_geometry = ColumnGeometry([time_label_xs, time_label_ys])
surface.text(
    "OVERLAY",
    time_label_geometry,
    colors.grey_7,
    time_label_strings,
    time_label_alignment,
    clip=(0, 0, 320, 240),
)
gc.collect()

# Plot title and additional information
from tempe.fonts import ubuntu16bold, ubuntu16
from tempe.font import TempeFont

surface.text(
    "DRAWING",
    (4, 0),
    colors.grey_a,
    "Air Quality (ppb)",
    font=TempeFont(ubuntu16bold),
)
surface.text(
    "DRAWING",
    (4, 20),
    colors.grey_8,
    "20/8/24--\n22/8/24",
    font=TempeFont(ubuntu16),
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

            display = FileDisplay("polar_plot.rgb565", (320, 240))
            with display:
                display.clear()
                surface.refresh(display, working_buffer)

    start = time.ticks_us()
    surface.refresh(display, working_buffer)
    print(time.ticks_diff(time.ticks_us(), start))
    return display


if __name__ == '__main__':
    display = main()

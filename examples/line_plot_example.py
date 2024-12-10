# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

"""Example showing how to create a line plot from Tempe Shapes."""

from array import array
import asyncio
import gc

from tempe import colors
from tempe.data_view import Repeat
from tempe.geometry import ColumnGeometry, PointsToLines
from tempe.surface import Surface
from tempe.text import CENTER, TOP, RIGHT


surface = Surface()

# a buffer one half the size of the screen
working_buffer = bytearray(2 * 320 * 121)


# fill the background with off-white pixels
surface.rectangles("BACKGROUND", (0, 0, 320, 240), colors.grey_f)


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


gc.collect()
from data.environmental import timestamps, temperature

# Plot screen bounds
x = 24
w = 288
x1 = x + w
y = 20
h = 200
y1 = y + h

# Map the data to screen coordinates
temperature_scale = LinearScale(11, y1, 21, y)
time_scale = LinearScale(1729586400, x, 1729672200, x1)

ys = temperature_scale.scale_values(temperature)
xs = time_scale.scale_values(timestamps)

# Create line geometry for the data points
points = ColumnGeometry([xs, ys])
lines = PointsToLines(points)

# draw the plot
surface.lines(
    "DRAWING",
    lines,
    colors.grey_3,
    clip=(x, y, w, h),
)

# Plot Decoration:

# fill the plot with white pixels
surface.rectangles("BACKGROUND", (x, y, w, h), colors.white)
# border the plot
# surface.rects('BACKGROUND', (x, y, w, h), colors.grey_d, fill=False)
# draw axes
surface.hlines("UNDERLAY", (x, y1, w), colors.grey_c)
surface.vlines("UNDERLAY", (x, y, h), colors.grey_c)


# Temperature axis: tick marks, grid lines, labels
tick_length = 4
temp_marks = temperature_scale.scale_values(list(range(12, 22)))
label_temps = [15, 20]
temp_labels = temperature_scale.scale_values([15, 20])
surface.hlines(
    "UNDERLAY",
    ColumnGeometry([Repeat(x - tick_length), temp_labels, Repeat(tick_length)]),
    colors.grey_c,
)
surface.hlines(
    "UNDERLAY",
    ColumnGeometry([Repeat(x), temp_labels, Repeat(w)]),
    colors.grey_f,
)
surface.text(
    "OVERLAY",
    ColumnGeometry([Repeat(x - tick_length - 1), temp_labels]),
    colors.grey_a,
    [f"{t}" for t in label_temps],
    (RIGHT, CENTER),
)

# Time axis: tick marks, grid lines, labels
day_start = 1729551600
tick_times = list(range(12, 36, 4))
time_marks = time_scale.scale_values(
    [day_start + t * 3600 for t in tick_times],
)
label_times = list(range(12, 36, 12))
time_labels = time_scale.scale_values(
    [day_start + t * 3600 for t in label_times],
)
surface.vlines(
    "OVERLAY",
    ColumnGeometry([time_marks, Repeat(y1), Repeat(tick_length)]),
    colors.grey_c,
)
surface.vlines(
    "UNDERLAY",
    ColumnGeometry([time_labels, Repeat(y), Repeat(h)]),
    colors.grey_f,
)
surface.text(
    "OVERLAY",
    ColumnGeometry([time_labels, Repeat(y1 + 8)]),
    colors.grey_a,
    [f"{t % 24}:00" for t in label_times],
    (CENTER, TOP),
)

# Plot title and additional information
from tempe.fonts import ubuntu16bold, ubuntu16
from tempe.font import TempeFont

surface.text(
    "DRAWING",
    (4, 0),
    colors.grey_a,
    "Temperature (°C)",
    font=TempeFont(ubuntu16bold),
)
surface.text(
    "DRAWING",
    (320, 0),
    colors.grey_a,
    "October 21-22, 2024",
    (RIGHT, TOP),
    font=TempeFont(ubuntu16),
)


def main(surface, working_buffer):
    import time
    from tempe_config import init_display

    # set up the display object
    display = asyncio.run(init_display())

    start = time.ticks_us()
    surface.refresh(display, working_buffer)
    print(time.ticks_diff(time.ticks_us(), start))


if __name__ == '__main__':
    try:
        main(surface, working_buffer)
    except ImportError:
        print(
            "Could not find tempe_config.init_display.\n\n"
            "To run examples, you must create a top-level tempe_config module containing\n"
            "an async init_display function that returns a display.\n\n"
            "See https://unital.github.io/tempe more information.\n\n"
            "Defaulting to file-based display.\n"
        )

        from tempe.display import FileDisplay

        display = FileDisplay("line_plot.rgb565", (320, 240))
        with display:
            display.clear()
            surface.refresh(display, working_buffer)

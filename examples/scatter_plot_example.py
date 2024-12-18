# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

"""Example showing how to create a scatter plot from Tempe Shapes."""

from array import array
import asyncio
import gc
from math import sqrt, log
import time

from tempe import colors
from tempe.colormaps.twilight import twilight
from tempe.data_view import Range, Repeat
from tempe.geometry import ColumnGeometry, RowGeometry
from tempe.markers import Marker
from tempe.polar_geometry import polar_rects
from tempe.surface import Surface
from tempe.text import TOP, BOTTOM, CENTER, RIGHT


# maximize available memory before allocating buffer
gc.collect()

# A buffer one half the size of a 320x240 screen
# NOTE: If you get MemoryErrors, make this smaller
working_buffer = bytearray(2 * 320 * 121)


# create the surface
surface = Surface()

# fill the background with off-white pixels
surface.rectangles("BACKGROUND", [(0, 0, 320, 240)], [colors.grey_f])


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


class LogScale:
    """Object that maps data to screen values linearly."""

    def __init__(self, low_data, low_screen, high_data, high_screen):
        self.low_data = log(low_data)
        self.low_screen = low_screen
        self.high_data = log(high_data)
        self.high_screen = high_screen
        data_range = log(high_data) - log(low_data)
        screen_range = high_screen - low_screen
        self.scale = screen_range / data_range

    def scale_values(self, data):
        """Scale data values to screen values."""
        screen = array("h", bytearray(2 * len(data)))
        low_data = self.low_data
        low_screen = self.low_screen
        scale = self.scale
        for i, value in enumerate(data):
            screen[i] = int(low_screen + scale * (log(value) - low_data))
        return screen


class AreaScale:
    """Object that maps data area for a radius parameter"""

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
            screen[i] = int(sqrt(low_screen + scale * (value - low_data)) // 2)
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


class CyclicColorScale:
    """Object that maps data to color values."""

    def __init__(self, colormap, period, phase=0):
        self.colormap = colormap
        self.period = period
        self.phase = phase

    def scale_values(self, data):
        """Scale data values to screen values."""
        screen = array("h", bytearray(2 * len(data)))
        phase = self.phase
        period = self.period
        colormap = self.colormap
        scale = len(colormap) / period
        for i, value in enumerate(data):
            screen[i] = colormap[int(scale * ((value - phase) % period))]
        return screen


gc.collect()
from data.environmental import timestamps, temperature, humidity, air_quality

# Plot screen bounds
x = 24
w = 180
x1 = x + w
y = 40
h = 180
y1 = y + h

# Map the data to screen coordinates
temperature_scale = LinearScale(11, y1, 21, y)
air_quality_scale = LinearScale(0, x, 150, x1)
humidity_scale = AreaScale(40, 9, 60, 50)
time_scale = CyclicColorScale(twilight, 24 * 60 * 60, 12 * 60 * 60)

ys = temperature_scale.scale_values(temperature)
xs = air_quality_scale.scale_values(air_quality)
marker_sizes = humidity_scale.scale_values(humidity)
marker_colors = time_scale.scale_values(timestamps)

# Create point-size geometry for the data points
markers = ColumnGeometry([xs, ys, marker_sizes])

# draw the plot
surface.markers(
    "DRAWING",
    markers,
    marker_colors,
    Repeat(Marker.CIRCLE),
    clip=(x, y, w, h),
)

# data for histograms
temp_hist = {t: 0 for t in range(11, 22)}
for t in temperature:
    temp_hist[int(t)] += 1
temp_hist_temps, temp_hist_counts = zip(*sorted(temp_hist.items()))

quality_hist = {q: 0 for q in range(0, 150, 15)}
for q in air_quality:
    quality_hist[int(q / 15) * 15] += 1
quality_hist_temps, quality_hist_counts = zip(*sorted(quality_hist.items()))

# histogram plots
temp_count_scale = LinearScale(0, 0, 100, 20)
quality_count_scale = LinearScale(0, 0, 100, -20)

temp_rects = ColumnGeometry(
    [
        Repeat(x1 + 2),
        temperature_scale.scale_values(temp_hist_temps),
        temp_count_scale.scale_values(temp_hist_counts),
        Repeat(int(temperature_scale.scale + 2)),
    ]
)
surface.rectangles(
    "DRAWING",
    temp_rects,
    Repeat(colors.red),
    clip=(x1, y, 20, h),
)

quality_rects = ColumnGeometry(
    [
        air_quality_scale.scale_values(quality_hist_temps),
        Repeat(y - 2),
        Repeat(int(15 * air_quality_scale.scale - 2)),
        quality_count_scale.scale_values(quality_hist_counts),
    ]
)
surface.rectangles(
    "DRAWING",
    quality_rects,
    Repeat(colors.green),
    clip=(x, y - 20, w, 20),
)

# Scales
cx = x1 + 20 + 45
cy = y + 50
time_scale_geometry = polar_rects(
    cx,
    cy,
    ColumnGeometry(
        [
            Repeat(20),
            Range(0, 360, 15),
            Repeat(15),
            Repeat(15),
        ]
    ),
)
surface.polygons(
    "DRAWING",
    time_scale_geometry,
    time_scale.scale_values([i * 3600 + 6 * 3600 for i in range(24)]),
)
surface.text(
    "DRAWING",
    RowGeometry.from_lists([[cx, cy - 35], [cx, cy + 38]]),
    Repeat(colors.grey_a),
    ["0:00", "12:00"],
    [(CENTER, BOTTOM), (CENTER, TOP)]
)

sample_humidities = [40, 50, 60, 70]
surface.markers(
    "DRAWING",
    ColumnGeometry(
        [
            Repeat(x1 + 30),
            Range(cy + 74, cy + 114, 12),
            humidity_scale.scale_values(sample_humidities),
        ]
    ),
    Repeat(colors.blue),
    Repeat(Marker.CIRCLE),
)
surface.markers(
    "DRAWING",
    ColumnGeometry(
        [
            Repeat(x1 + 40),
            Range(cy + 75, cy + 115, 12),
            humidity_scale.scale_values(sample_humidities),
        ]
    ),
    Repeat(colors.grey_a),
    [f"{h}%" for h in sample_humidities],
    clip=(x1 + 30, cy + 70, 40, 48),
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
    ColumnGeometry([Repeat(x - tick_length), temp_marks, Repeat(tick_length)]),
    Repeat(colors.grey_c),
)
surface.hlines(
    "UNDERLAY",
    ColumnGeometry([Repeat(x), temp_labels, Repeat(w)]),
    Repeat(colors.grey_f),
)
surface.text(
    "OVERLAY",
    ColumnGeometry([Repeat(x - tick_length), temp_labels]),
    Repeat(colors.grey_a),
    [f"{t}" for t in label_temps],
    (RIGHT, CENTER),
)

# Air Quality axis: tick marks, grid lines, labels
tick_quality = list(range(0, 150, 10))
quality_marks = air_quality_scale.scale_values(tick_quality)
label_air_quality = [50, 100]
air_quality_labels = air_quality_scale.scale_values(label_air_quality)
surface.vlines(
    "OVERLAY",
    ColumnGeometry([quality_marks, Repeat(y1), Repeat(tick_length)]),
    Repeat(colors.grey_c),
)
surface.vlines(
    "UNDERLAY",
    ColumnGeometry([air_quality_labels, Repeat(y), Repeat(h)]),
    Repeat(colors.grey_f),
)
surface.text(
    "OVERLAY",
    ColumnGeometry([air_quality_labels, Repeat(y1 + 8)]),
    Repeat(colors.grey_a),
    [str(t) for t in label_air_quality],
    (CENTER, TOP),
)

# Plot title and additional information
from tempe.fonts import ubuntu16bold
from tempe.font import TempeFont

surface.text(
    "DRAWING",
    (4, 0),
    colors.grey_a,
    "Temperature (°C) vs. Air Quality (ppb)",
    font=TempeFont(ubuntu16bold),
)
surface.text(
    "DRAWING",
    (x1 + 20, y - 20),
    colors.grey_a,
    "20-22/8/24",
    font=TempeFont(ubuntu16bold),
)
surface.text(
    "DRAWING",
    (x1 + 20, cy + 50),
    colors.grey_a,
    "Humidity",
    font=TempeFont(ubuntu16bold),
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

            display = FileDisplay("scatter_plot.rgb565", (320, 240))
            with display:
                display.clear()
                surface.refresh(display, working_buffer)

    start = time.ticks_us()
    surface.refresh(display, working_buffer)
    print(time.ticks_diff(time.ticks_us(), start))
    return display


if __name__ == '__main__':
    display = main()

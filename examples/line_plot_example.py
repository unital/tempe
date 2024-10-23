from array import array
import gc

from tempe import colors
from tempe.data_view import Repeat
from tempe.geometry import ColumnGeometry, PointsToLines
from tempe.markers import Marker
from tempe.surface import Surface


surface = Surface()

# a buffer one half the size of the screen
working_buffer = array('H', bytearray(2*320*121))


# fill the background with off-white pixels
surface.rects('BACKGROUND', [(0, 0, 320, 240)], [colors.grey_f])

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
        screen = array('h', bytearray(2*len(data)))
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
    Repeat(colors.grey_3),
    clip=(x, y, w, h),
)

# Plot Decoration:

# fill the plot with white pixels
surface.rects('BACKGROUND', [(x, y, w, h)], [colors.white])
# border the plot
# surface.rects('BACKGROUND', [(x, y, w, h)], [colors.grey_d], fill=False)
# draw axes
surface.hlines('UNDERLAY', [(x, y1, w)], [colors.grey_c])
surface.vlines('UNDERLAY', [(x, y, h)], [colors.grey_c])


# Temperature axis: tick marks, grid lines, labels
tick_length = 4
temp_marks = temperature_scale.scale_values(list(range(12, 22)))
label_temps = [15, 20]
temp_labels = temperature_scale.scale_values([15, 20])
surface.hlines(
    'UNDERLAY',
    ColumnGeometry([Repeat(x - tick_length), temp_labels, Repeat(tick_length)]),
    Repeat(colors.grey_c),
)
surface.hlines(
    'UNDERLAY',
    ColumnGeometry([Repeat(x), temp_labels, Repeat(w)]),
    Repeat(colors.grey_f),
)
surface.text(
    'OVERLAY',
    ColumnGeometry([Repeat(4), temp_labels]),
    Repeat(colors.grey_a),
    [f"{t}" for t in label_temps],
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
    'OVERLAY',
    ColumnGeometry([time_marks, Repeat(y1), Repeat(tick_length)]),
    Repeat(colors.grey_c),
)
surface.vlines(
    'UNDERLAY',
    ColumnGeometry([time_labels, Repeat(y), Repeat(h)]),
    Repeat(colors.grey_f),
)
surface.text(
    'OVERLAY',
    ColumnGeometry([time_labels, Repeat(y1 + 8)]),
    Repeat(colors.grey_a),
    [f"{t % 24}:00" for t in label_times],
)

# Plot title and additional information
from tempe.fonts import roboto16bold, roboto16
from tempe.font import TempeFont
surface.text(
    'DRAWING',
    [[4, 0]],
    [colors.grey_a],
    ["Temperature (°C)"],
    font=TempeFont(roboto16bold),
)
surface.text(
    'DRAWING',
    [[160, 0]],
    [colors.grey_a],
    ["October 21-22, 2024"],
    font=TempeFont(roboto16),
)


def main(surface, working_buffer):
    import asyncio

    async def init_display():
        from devices.st7789 import ST7789
        from machine import Pin, SPI

        spi = SPI(0, baudrate=62_500_000, phase=1, polarity=1, sck=Pin(18, Pin.OUT), mosi=Pin(19, Pin.OUT), miso=Pin(16, Pin.OUT))
        backlight = Pin(20, Pin.OUT)
        display = ST7789(spi, cs_pin=Pin(17, Pin.OUT, value=1), dc_pin=Pin(16, Pin.OUT))
        backlight(1)
        await display.init()
        return display

    # set up the display object
    display = asyncio.run(init_display())

    # refresh the display
    display.clear()
    import time
    start = time.ticks_us()
    surface.refresh(display, working_buffer)
    print(time.ticks_diff(time.ticks_us(), start))

if __name__ == '__main__':

    # if we have an actual screen, use it
    main(surface, working_buffer)

elif __name__ != '__test__':
    from tempe.display import FileDisplay

    # set up the display object
    display = FileDisplay('line_plot.rgb565', (320, 240))
    # refresh the display
    with display:
        display.clear()
        surface.refresh(display, working_buffer)

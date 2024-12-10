# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

"""Example showing Unital logo."""

import array
import asyncio
import math

from tempe import colors
from tempe.geometry import ColumnGeometry, RowGeometry, PointsToLines, Extend
from tempe.colormaps.viridis import viridis
from tempe.colormaps.twilight import twilight
from tempe.data_view import Repeat
from tempe.surface import Surface
from tempe.text import Text
from tempe.shapes import Rectangles
from tempe.font import TempeFont
from tempe.lines import WidePolyLines, WideLines

from example_fonts import roboto88boldunital


# a buffer one half the size of the screen
working_buffer = bytearray(2 * 320 * 121)

surface = Surface()

bg = colors.black

# fill the background
background = Rectangles([(0, 0, 320, 240)], [bg])
surface.add_shape("BACKGROUND", background)

# points = array.array('h', [
#     int(x)
#     for theta in range(180, 360, 10)
#     for x in (
#         160 + 125 * math.cos(theta * math.pi / 180),
#         157 + 25 * math.sin(theta * math.pi / 180),
#     )
# ])
# points.append(9)

# lines = WidePolyLines([points], [colors.grey_c])
# surface.add_shape("DRAWING", lines)

# points1 = array.array('h', [
#     int(x)
#     for theta in range(180, 30, -10)
#     for x in (
#         160 + 125 * math.cos(theta * math.pi / 180),
#         157 + 25 * math.sin(theta * math.pi / 180),
#     )
# ])
# points1.append(9)
# points2 = array.array('h', [160 + 100, 157 + 14, 160 + 75, 158 + 14 - 3, 9])
# points3 = array.array('h', [160 + 100, 157 + 14, 160 + 78, 158 + 14 + 12, 9])

# lines = WidePolyLines([points1, points2, points3], Repeat(colors.grey_d))
# surface.add_shape("DRAWING", lines)


points = RowGeometry(
    [
        (
            int(160 + 125 * math.cos(theta * math.pi / 180)),
            int(157 + 25 * math.sin(theta * math.pi / 180)),
            int(160 + 125 * math.cos((theta + 10) * math.pi / 180)),
            int(157 + 25 * math.sin((theta + 10) * math.pi / 180)),
            9,
        )
        for theta in range(40, 350, 5)
    ]
)

line_colors = [
    twilight[int(255 * ((-theta + 90) % 360) / 360)] for theta in range(40, 360, 5)
]
print(line_colors[0])
lines = WideLines(points, line_colors)
surface.add_shape("DRAWING", lines)

points2 = array.array("h", [160 + 100, 157 + 14, 160 + 75, 158 + 14 - 3, 9])
points3 = array.array("h", [160 + 100, 157 + 14, 160 + 78, 158 + 14 + 12, 9])

lines = WidePolyLines([points2, points3], Repeat(line_colors[1]))
surface.add_shape("DRAWING", lines)


surface.circles("DRAWING", (10 + 275, 32 + 125, 22), bg)
surface.circles("DRAWING", (10 + 275, 32 + 125, 15), "#f00")

font = TempeFont(roboto88boldunital)
widths = [font.measure(c)[2] - 4 for c in "Unital"]
total = sum(widths)
positions = [sum(widths[:i]) for i in range(6)]
color_index = [int(255 * (p + w / 2) / total) for p, w in zip(positions, widths)]
text_colors = [viridis[index] for index in color_index]
print(text_colors)

x = total - 20

for dx, dy in [(dx, dy) for dx in [-3, 3] for dy in [-3, 3]]:
    surface.text(
        "DRAWING",
        [(148 - x // 2 + p + dx, 32 + 98 - font.baseline + dy) for p in positions],
        bg,
        ["U", "n", "i", "t", "a", "l"],
        font=font,
        clip=(0, 0, 320, 240),
    )


unital = surface.text(
    "DRAWING",
    [(148 - x // 2 + p, 32 + 98 - font.baseline) for p in positions],
    text_colors,
    ["U", "n", "i", "t", "a", "l"],
    font=font,
    clip=(0, 0, 320, 240),
)


async def init_display():
    from tempe_displays.st7789.pimoroni import PimoroniDisplay

    display = PimoroniDisplay(size=(240, 320))
    display.backlight_pin(1)
    await display.init()
    return display


def main(surface, working_buffer):
    # set up the display object
    display = asyncio.run(init_display())

    # refresh the display
    display.clear()

    import time

    start = time.ticks_us()
    surface.refresh(display, working_buffer)
    print(time.ticks_diff(time.ticks_us(), start))


if __name__ == "__main__":

    # if we have an actual screen, use it
    main(surface, working_buffer)

elif __name__ != "__test__":
    from tempe.display import FileDisplay

    # set up the display object
    display = FileDisplay("unital.rgb565", (320, 240))

    # refresh the display
    with display:
        display.clear()
        surface.refresh(display, working_buffer)

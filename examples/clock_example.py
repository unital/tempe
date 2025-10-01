# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

"""Example showing asyncio updating a clock face drawn with polar coordinates."""

import asyncio
from machine import RTC
import gc

from tempe import colors
from tempe.geometry import ColumnGeometry, RowGeometry
from tempe.data_view import Repeat
from tempe.font import TempeFont
from tempe.polar_geometry import polar_r_lines, polar_points, polar_point_arrays
from tempe.surface import Surface, BACKGROUND, UNDERLAY, DRAWING, OVERLAY
from tempe.text import CENTER
from example_fonts import roboto24boldnumbers

# maximize available memory before allocating buffer
gc.collect()

# A buffer one half the size of a 320x240 screen
# NOTE: If you get MemoryErrors, make this smaller
working_buffer = bytearray(2 * 320 * 121)


class Clock:
    """Class for clock face that updates asynchronously."""

    def __init__(self, rtc, cx, cy, r, font=TempeFont(roboto24boldnumbers)):
        self.rtc = rtc
        self.cx = cx
        self.cy = cy
        self.r = r
        self.font = font
        self.h, self.m, self.s = self.rtc.datetime()[4:7]

    def create_shapes(self, surface):
        surface.circles(BACKGROUND, (self.cx, self.cy, self.r), colors.grey_1)
        surface.circles(
            BACKGROUND, (self.cx, self.cy, self.r), colors.grey_2, fill=False
        )

        minute_angles = [360 * i // 60 for i in range(0, 60)]
        minue_ticks = polar_r_lines(
            self.cx,
            self.cy,
            ColumnGeometry([Repeat(self.r), minute_angles, Repeat(-5)]),
        )
        surface.lines(UNDERLAY, minue_ticks, colors.grey_3)

        hour_angles = [360 * i // 12 - 90 for i in range(1, 13)]
        hour_ticks = polar_r_lines(
            self.cx, self.cy, ColumnGeometry([Repeat(self.r), hour_angles, Repeat(-10)])
        )
        surface.lines(UNDERLAY, hour_ticks, colors.grey_4)

        hour_numbers = polar_points(
            self.cx, self.cy, ColumnGeometry([Repeat(self.r - 28), hour_angles])
        )
        surface.text(
            UNDERLAY,
            hour_numbers,
            colors.grey_6,
            [str(i) for i in range(1, 13)],
            (CENTER, CENTER),
            font=self.font,
        )

        self.hour_hand = surface.polygons(
            DRAWING, self.hour_geometry(), colors.grey_8
        )
        self.minute_hand = surface.polygons(
            DRAWING, self.minute_geometry(), colors.grey_a
        )
        self.second_hand = surface.lines(DRAWING, self.second_geometry(), "#c22")

        surface.circles(OVERLAY, (self.cx, self.cy, 3), colors.grey_2)

    def hour_geometry(self):
        angle = int(360 * (self.h % 12 + self.m / 60) / 12 - 90)
        return polar_point_arrays(
            self.cx,
            self.cy,
            RowGeometry.from_lists(
                [
                    [
                        self.r - 50,
                        angle - 3,
                        self.r - 50,
                        angle + 3,
                        -10,
                        angle - 30,
                        -10,
                        angle + 30,
                    ]
                ]
            ),
        )

    def minute_geometry(self):
        angle = int(360 * (self.m + self.s / 60) / 60 - 90)
        return polar_point_arrays(
            self.cx,
            self.cy,
            RowGeometry.from_lists(
                [
                    [
                        self.r - 20,
                        angle - 1,
                        self.r - 20,
                        angle + 1,
                        -20,
                        angle - 5,
                        -20,
                        angle + 5,
                    ]
                ]
            ),
        )

    def second_geometry(self):
        angle = int(360 * self.s / 60 - 90)
        return polar_r_lines(self.cx, self.cy, [[-15, angle, self.r]])

    async def update_time(self):
        while True:
            h, m, s = self.rtc.datetime()[4:7]
            if m != self.m:
                self.h = h
                self.m = m
                self.s = s
                self.hour_hand.update(geometry=self.hour_geometry())
                self.minute_hand.update(geometry=self.minute_geometry())
                self.second_hand.update(geometry=self.second_geometry())
            elif s != self.s:
                self.m = m
                self.s = s
                self.minute_hand.update(geometry=self.minute_geometry())
                self.second_hand.update(geometry=self.second_geometry())

            await asyncio.sleep(0.1)


async def refresh_display(surface, display, working_buffer):
    import time

    while True:
        await surface.refresh_needed.wait()
        start = time.ticks_us()
        surface.refresh(display, working_buffer)
        print(time.ticks_diff(time.ticks_us(), start))


async def run(display=None):
    """Initialize the devices and update when values change."""
    if display is None:
        try:
            from tempe_config import init_display

            display = await init_display()
        except ImportError:
            print(
                "Could not find tempe_config.init_display.\n\n"
                "To run examples, you must create a top-level tempe_config module containing\n"
                "an async init_display function that returns a display.\n\n"
                "See https://unital.github.io/tempe more information.\n\n"
            )
            raise

    rtc = RTC()
    surface = Surface()
    surface.rectangles(BACKGROUND, (0, 0) + display.size, colors.black)
    clock = Clock(
        rtc, display.size[0] // 2, display.size[1] // 2, min(display.size) // 2
    )
    clock.create_shapes(surface)

    # update time and display forever
    await asyncio.gather(
        refresh_display(surface, display, working_buffer),
        clock.update_time(),
    )


def main(display=None):
    """Run the application asynchronously."""
    return asyncio.run(run(display))


if __name__ == "__main__":
    display = main()

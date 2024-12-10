# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

"""Example showing support for rounded rectangles."""

import asyncio

from tempe.colormaps.viridis import viridis
from tempe.data_view import Repeat, Range, Interpolated
from tempe.geometry import ColumnGeometry
from tempe.surface import Surface
from tempe.shapes import Rectangles, RoundedRectangles
from tempe.display import FileDisplay

surface = Surface()

# a buffer one half the size of the screen
working_buffer = bytearray(2 * 320 * 121)

# fill the background with white pixels
background = Rectangles([(0, 0, 320, 240)], [0xFFFF])
surface.add_shape("BACKGROUND", background)


# draw some rectangles
rectangles = RoundedRectangles(
    ColumnGeometry(
        [
            Range(24, 240, 80),
            Repeat(24),
            Range(32, 96, 16),
            Range(64, 16, -16),
        ]
    ),
    Interpolated(viridis, 3),
    fill=True,
)
surface.add_shape("DRAWING", rectangles)

surface.rounded_rectangles(
    "DRAWING",
    ColumnGeometry([
            Range(24, 240, 80),
            Range(96, 48, -16),
            Range(64, 16, -16),
            Range(32, 96, 16),
    ]),
    Interpolated(viridis, 3),
    radius=12,
    fill=False,
)

surface.rounded_rectangles(
    "DRAWING",
    ColumnGeometry([
            Range(24, 240, 80),
            Repeat(160),
            Range(32, 96, 16),
            Range(64, 16, -16),
    ]),
    Interpolated(viridis, 3),
    radius=32,
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

        display = FileDisplay("rounded_rect.rgb565", (320, 240))
        with display:
            display.clear()
            surface.refresh(display, working_buffer)

import asyncio
from array import array
import framebuf
import random
import math

from tempe.bitmaps import Bitmaps, ColoredBitmaps
from tempe.colormaps.viridis import viridis
from tempe.colormaps.viridis import viridis
from tempe.data_view import Repeat, Range, Interpolated
from tempe.geometry import RowGeometry, ColumnGeometry
from tempe.surface import Surface
from tempe.shapes import Rectangles
from tempe.lines import WideLines, WidePolyLines
from tempe.display import FileDisplay

random.seed(0)

surface = Surface()

# a buffer one quarter the size of the screen
working_buffer = array("H", bytearray(2 * 320 * 61))

# fill the background with white pixels
background = Rectangles([(0, 0, 320, 240)], [0xFFFF])
surface.add_shape("BACKGROUND", background)


# draw some lines
lines = WideLines(
    ColumnGeometry(
        [Range(8, 96, 8), Repeat(20), Range(8, 184, 16), Repeat(100), Range(1, 11)]
    ),
    Interpolated(viridis, 10),
    clip=(0, 0, 160, 120),
)
surface.add_shape("DRAWING", lines)


# draw some lines in the opposite direction
lines = WideLines(
    ColumnGeometry(
        [
            Range(8, 96, 8) + 160,
            Repeat(100),
            Range(8, 184, 16) + 160,
            Repeat(20),
            Range(1, 11),
        ]
    ),
    Interpolated(viridis, 10),
    clip=(160, 0, 160, 120),
    round=False,
)
surface.add_shape("DRAWING", lines)

# draw some polylines
polylines = WidePolyLines(
    RowGeometry(
        [
            array(
                "h",
                [
                    10 + 30 * i,
                    125,
                    10 + 30 * i,
                    225,
                    15 + 30 * i,
                    225,
                    25 + 30 * i,
                    165,
                    10 + 30 * i,
                    125,
                ]
                + [i + 1],
            )
            for i in range(10)
        ]
    ),
    Interpolated(viridis, 10),
    clip=(0, 120, 320, 120),
)
surface.add_shape("DRAWING", polylines)


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
    display = FileDisplay("lines.rgb565", (320, 240))
    # refresh the display
    with display:
        display.clear()
        surface.refresh(display, working_buffer)

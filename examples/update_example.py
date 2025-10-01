# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

"""Example showing asyncio updating of a surface."""

import asyncio
from machine import ADC, RTC
import gc

from tempe import colors
from tempe.font import TempeFont
from tempe.surface import Surface, BACKGROUND, DRAWING
from tempe.text import BOTTOM, CENTER, TOP

# maximize available memory before allocating buffer
gc.collect()

# A buffer one half the size of a 320x240 screen
# NOTE: If you get MemoryErrors, make this smaller
working_buffer = bytearray(2 * 320 * 121)


def init_surface(surface, size):
    from example_fonts import roboto32boldnumbers

    # fill the background with off-white pixels
    surface.rectangles(BACKGROUND, (0, 0) + size, "#fff")

    center = (size[0] // 2, size[1] // 2)

    # prepare the text fields
    time_field = surface.text(
        DRAWING,
        center,
        "#aaa",
        "",
        (CENTER, BOTTOM),
        font=TempeFont(roboto32boldnumbers),
    )
    temp_field = surface.text(
        DRAWING,
        center,
        colors.grey_a,
        "",
        (CENTER, TOP),
        font=TempeFont(roboto32boldnumbers),
    )
    return time_field, temp_field


async def update_time(rtc, time_field):
    while True:
        h, m, s = rtc.datetime()[4:7]
        text = f"{h:>2d}:{m:02d}:{s:02d}"
        # only update if the text has changed
        if time_field.texts[0] != text:
            time_field.update(texts=[text])
        await asyncio.sleep(0.1)


async def update_temperature(adc, text_field):
    while True:
        value = adc.read_u16()
        temp = 27 - (3.3 * value / 0xFFFF - 0.706) / 0.001721
        text = f"{temp:.1f}°C"
        # only update when needed
        if text != text_field.texts[0]:
            text_field.update(texts=[text])
        await asyncio.sleep(1)


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

    surface = Surface()
    time_field, temp_field = init_surface(surface, display.size)

    # Note: this assumes a Raspberry Pi Pico
    temp_adc = ADC(ADC.CORE_TEMP)
    rtc = RTC()

    # poll the temperature and update the display forever
    await asyncio.gather(
        refresh_display(surface, display, working_buffer),
        update_time(rtc, time_field),
        update_temperature(temp_adc, temp_field),
    )


def main(display=None):
    """Run the application asynchronously."""
    return asyncio.run(run(display))


if __name__ == '__main__':
    display = main()

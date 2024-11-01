# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

"""Example showing asyncio updating of a surface."""

import asyncio
from machine import ADC, RTC

from tempe import colors
from tempe.font import TempeFont
from tempe.surface import Surface


# a buffer one half the size of the screen
WORKING_BUFFER = bytearray(2 * 240 * 161)


async def init_surface(surface):
    # fill the background with off-white pixels
    surface.rectangles("BACKGROUND", (0, 0, 240, 320), "#fff")

    # prepare the text fields
    from example_fonts import roboto32boldnumbers

    time_field = surface.text(
        "DRAWING",
        (10, 10),
        "#aaa",
        "",
        font=TempeFont(roboto32boldnumbers),
        clip=(10, 10, 229, 40),
    )
    temp_field = surface.text(
        "DRAWING",
        (10, 50),
        colors.grey_a,
        "",
        font=TempeFont(roboto32boldnumbers),
        clip=(10, 50, 229, 40),
    )
    return time_field, temp_field


async def init_display():
    from tempe_displays.st7789.pimoroni import PimoroniDisplay

    display = PimoroniDisplay(size=(240, 320))
    display.backlight_pin(1)
    await display.init(270)
    return display


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


async def main(working_buffer):

    # initialize objects
    surface = Surface()
    temp_adc = ADC(ADC.CORE_TEMP)
    rtc = RTC()
    display, fields = await asyncio.gather(
        init_display(),
        init_surface(surface),
    )
    time_field, temp_field = fields

    # poll the temperature and update the display forever
    await asyncio.gather(
        refresh_display(surface, display, working_buffer),
        update_time(rtc, time_field),
        update_temperature(temp_adc, temp_field),
    )


if __name__ == "__main__":
    asyncio.run(main(WORKING_BUFFER))

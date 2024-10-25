import asyncio
from array import array
from machine import ADC, Pin, SPI, RTC

from tempe import colors
from tempe.font import TempeFont
from tempe.surface import Surface


# a buffer one third the size of the screen
WORKING_BUFFER = array('H', bytearray(2*320*81))


async def init_surface(surface):
    # fill the background with off-white pixels
    surface.rects('BACKGROUND', (0, 0, 320, 240), "#fff")

    # prepare the text fields
    from example_fonts import roboto32boldnumbers
    time_field = surface.text(
        "DRAWING",
        (10, 10),
        "#aaa",
        "",
        font=TempeFont(roboto32boldnumbers),
        clip=(10, 10, 240, 40),
    )
    temp_field = surface.text(
        "DRAWING",
        (10, 50),
        colors.grey_a,
        "",
        font=TempeFont(roboto32boldnumbers),
        clip=(10, 50, 240, 40),
    )
    return time_field, temp_field


async def init_display():
    from devices.st7789 import ST7789

    spi = SPI(0, baudrate=62_500_000, phase=1, polarity=1, sck=Pin(18, Pin.OUT), mosi=Pin(19, Pin.OUT), miso=Pin(16, Pin.OUT))
    backlight = Pin(20, Pin.OUT)
    display = ST7789(spi, cs_pin=Pin(17, Pin.OUT, value=1), dc_pin=Pin(16, Pin.OUT))
    backlight(1)
    await display.init()
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
    while True:
        await surface.refresh_needed.wait()
        surface.refresh(display, working_buffer)


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


if __name__ == '__main__':
    asyncio.run(main(WORKING_BUFFER))

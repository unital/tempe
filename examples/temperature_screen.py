from array import array
import asyncio
from machine import SPI, Pin
from machine import ADC, RTC

from ultimo.pipelines import Dedup, EWMA, pipe
from ultimo_machine.gpio import PollADC
from ultimo_machine.time import PollRTC

from tempe.surface import Surface
from tempe.components import Label

from devices import ST7789


w = 320
h = 240

DRAWING_BUFFER = array('H', bytearray(2*w*61))


async def init_display():
    spi = SPI(0, baudrate=62_500_000, phase=1, polarity=1, sck=Pin(18, Pin.OUT), mosi=Pin(19, Pin.OUT), miso=Pin(16, Pin.OUT))
    backlight = Pin(20,Pin.OUT)
    display = ST7789(spi, cs_pin=Pin(17, Pin.OUT, value=1), dc_pin=Pin(16, Pin.OUT))
    backlight(1)
    await display.init()
    return display


@pipe
def u16_to_celcius(value: int) -> float:
    """Convert raw uint16 values to temperatures."""
    return 27 - (3.3 * value / 0xFFFF - 0.706) / 0.001721


async def display_temperature(surface):
    temp_source = PollADC(ADC.CORE_TEMP, 1)
    temp_display = Label(surface, (4, 32, 100, 60), await temp_source(), format="{t:5.1f}°C".format)
    async for t in PollADC(ADC.CORE_TEMP, 1) | u16_to_celcius() | EWMA(0.05):
        temp_display.value = t
        temp_display.value.update()


async def refresh(surface):
    while True:
        await surface.refresh_needed.wait()
        surface.refresh(display, DRAWING_BUFFER)


async def main():
    display = await init_display()
    surface = Surface()
    label = Label(surface, (4, 4, 100, 20), 'Temperature')

    task1 = asyncio.create_task(update_temperature())
    task2 = asyncio.create_task(refresh(surface))
    await asyncio.gather(task1, task2)


if __name__ == '__main__':
    asyncio.run(main())
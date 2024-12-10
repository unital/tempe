# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

"""Example showing live updating of microcontroller state.

This is designed to work with a Raspberry Pi Pico.

Note: this uses some experimental features (such as Plot object types) that
will likely have a changed API in the future and are not included in the mip
distribution.  You will need to install from source to use this example.

It could also do with some clean-up of duplicated code.
"""


import asyncio
import gc
from machine import ADC, freq
import micropython
import time

from ultimo.pipelines import Dedup, pipe
from ultimo.poll import poll
from ultimo.value import Value
from ultimo_machine.gpio import PollADC

from tempe.colors import grey_7, grey_d
from tempe.font import TempeFont
from tempe.fonts import ubuntu16bold
from tempe.markers import Marker
from tempe.surface import Surface
from tempe.component import LinePlot, ScatterPlot, BarPlot
from tempe.text import LEFT, RIGHT, TOP
from tempe.colormaps.plasma import plasma
from tempe.colormaps.viridis import viridis

from example_fonts import roboto32boldnumbers, roboto24boldnumbers


w = 320
h = 240

gc.collect()
DRAWING_BUFFER = bytearray(2 * w * 61)

large_numbers = TempeFont(roboto32boldnumbers)
small_numbers = TempeFont(roboto24boldnumbers)

async def init_display():
    from tempe_displays.st7789.pimoroni import PimoroniDisplay as Display
    # or for Waveshare Pico-ResTouch-LCD-28:
    #     from tempe_displays.st7789.waveshare import PicoResTouchDisplay as Display

    display = Display()
    await display.init()
    display.backlight_pin(1)
    return display


def temp_to_color(temp):
    index = int((len(plasma) - 1) * (temp - 20) / 10)
    return plasma[index]


def free_to_color(free):
    index = int((len(viridis) - 1) * ((1 << 18) - free) / (1 << 18))
    return viridis[index]


def alloc_to_color(alloc):
    index = int((len(viridis) - 1) * (alloc / (1 << 18)))
    return viridis[index]


def stack_to_color(stack):
    index = int((len(viridis) - 1) * (stack / (1 << 13)))
    return viridis[index]


@pipe
def u16_to_celcius(value: int) -> float:
    """Convert raw uint16 values to temperatures."""
    return 27 - (3.3 * value / 0xFFFF - 0.706) / 0.001721


async def display_temperature(surface, value):
    temp_display = surface.text(
        "DRAWING",
        (316, 20),
        "#000",
        "",
        (RIGHT, TOP),
        font=large_numbers,
        clip=(164, 20, 152, 60),
    )
    format = pipe("{:.1f}°C".format)
    async for temp in value | format() | Dedup():
        temp_display.update(texts=[temp], colors=[temp_to_color(await value())])


@pipe
def format_memory(memory):
    return f"{memory >> 10:d}"


async def display_free(surface, value):
    free = await value()
    free_display = surface.text(
        "DRAWING",
        (244, 144),
        free_to_color(free),
        str(free),
        (RIGHT, TOP),
        font=large_numbers,
        clip=(164, 144, 80, 60),
    )
    free_units = surface.text(
        "DRAWING",
        (252, 144),
        free_to_color(free),
        "KiB",
        (LEFT, TOP),
        font=small_numbers,
        clip=(252, 144, 64, 60),
    )
    async for free in value | format_memory() | Dedup():
        colors = [free_to_color(await value())]
        free_display.update(texts=[free], colors=colors)
        free_units.update(colors=colors)


async def display_alloc(surface, value):
    alloc = await value()
    alloc_display = surface.text(
        "DRAWING",
        (244, 84),
        "#000",
        str(alloc),
        (RIGHT, TOP),
        font=large_numbers,
        clip=(164, 84, 80, 60),
    )
    alloc_units = surface.text(
        "DRAWING",
        (252, 84),
        "#000",
        "KiB",
        (LEFT, TOP),
        font=small_numbers,
        clip=(252, 84, 64, 60),
    )
    async for alloc in value | format_memory() | Dedup():
        colors = [alloc_to_color(await value())]
        alloc_display.update(texts=[alloc], colors=colors)
        alloc_units.update(colors=colors)


async def display_stack(surface, value):
    stack = await value()
    stack_display = surface.text(
        "DRAWING",
        (128, 204),
        "#000",
        str(stack),
        (RIGHT, TOP),
        font=large_numbers,
        clip=(4, 204, 128, 35),
    )
    stack_units = surface.text(
        "DRAWING",
        (132, 204),
        "#000",
        "B",
        (LEFT, TOP),
        font=small_numbers,
        clip=(132, 204, 20, 35),
    )
    format = pipe(str)
    async for stack in value | format() | Dedup():
        colors = [stack_to_color(await value())]
        stack_display.update(texts=[stack], colors=colors)
        stack_units.update(colors=colors)


async def plot_average_temperature(surface, value, temp_range=(20, 30)):
    times = [0] * 180
    temps = [0] * 180
    colors = [0] * 180
    temp = await value()
    temp_plot = LinePlot(
        surface,
        (4, 24, 156, 60 - 24),
        values=temps,
        index=times,
        colors=colors,
        value_range=temp_range,
        index_range=(time.time() - 180, time.time()),
    )
    temp_plot.style["background_color"] = None
    async for temp in value:
        t = time.time()
        times[:-1] = times[1:]
        times[-1] = t
        temps[:-1] = temps[1:]
        temps[-1] = temp
        temp_plot.index_range = (t - 180, t)
        colors[:-1] = colors[1:]
        colors[-1] = temp_to_color(temp)
        temp_plot.update()

async def plot_spot_temperature(surface):
    temp_source = PollADC(ADC.CORE_TEMP, 1)
    times = [0] * 180
    temps = [0] * 180
    temp_plot = ScatterPlot(
        surface,
        (4, 24, 156, 60 - 24),
        values=temps,
        index=times,
        colors=grey_d,
        sizes=4,
        value_range=(25, 30),
        index_range=(time.time() - 180, time.time()),
    )
    temp_plot.style["background_color"] = None
    extreme_times = []
    extreme_temps = []
    extreme_colors = []
    extreme_markers = []
    extreme_plot = ScatterPlot(
        surface,
        (4, 24, 160, 60 - 24),
        values=extreme_temps,
        index=extreme_times,
        colors=extreme_colors,
        markers=extreme_markers,
        sizes=5,
        value_range=(25, 30),
        index_range=(time.time() - 180, time.time()),
    )
    extreme_plot.style["background_color"] = None
    async for temp in temp_source | u16_to_celcius():
        t = time.time()
        times[:-1] = times[1:]
        times[-1] = t
        temps[:-1] = temps[1:]
        temps[-1] = temp
        temp_plot.index_range = (t - 180, t)
        temp_plot.update()
        extreme_temps[:] = [min(temp for temp in temps if temp != 0), max(temps)] * 2
        indices = [temps.index(temp) for temp in extreme_temps]
        extreme_times[:] = [times[index] for index in indices]
        extreme_colors[:] = [temp_to_color(temp) for temp in extreme_temps]
        extreme_markers[:] = [f" {temp:4.1f}" for temp in extreme_temps[:2]] + [
            Marker.PLUS
        ] * 2
        extreme_plot.index_range = (t - 180, t)
        extreme_plot.update()


async def plot_allocated(surface, value):
    index = list(range(39))
    allocs = [0] * 39
    colors = [0] * 39
    alloc = await value()
    alloc_plot = BarPlot(
        surface,
        (4, 88, 156, 60 - 24),
        values=allocs,
        index=index,
        colors=colors,
        value_range=(0, 1 << 18),
        index_range=(0, 39),
    )
    alloc_plot.style["background_color"] = None
    async for alloc in value:
        allocs[:-1] = allocs[1:]
        allocs[-1] = alloc
        colors[:-1] = colors[1:]
        colors[-1] = alloc_to_color(alloc)
        alloc_plot.update()


async def plot_free(surface, value):
    index = list(range(39))
    frees = [0] * 39
    colors = [0] * 39
    free = await value()
    free_plot = BarPlot(
        surface,
        (4, 148, 156, 60 - 24),
        values=frees,
        index=index,
        colors=colors,
        value_range=(0, 1 << 17),
        index_range=(0, 39),
    )
    free_plot.style["background_color"] = None
    async for free in value:
        frees[:-1] = frees[1:]
        frees[-1] = free
        colors[:-1] = colors[1:]
        colors[-1] = free_to_color(free)
        free_plot.update()


async def refresh(surface, display):
    while True:
        await surface.refresh_needed.wait()
        surface.refresh(display, DRAWING_BUFFER)


@poll
def check_free():
    return gc.mem_free()


@poll
def check_allocated():
    return gc.mem_alloc()


@poll
def check_stack():
    return micropython.stack_use()


async def main():
    from tempe_config import init_display

    display = await init_display()
    surface = Surface()
    surface.rectangles("BACKGROUND", (0, 0, 320, 240), "#fff")
    labels = surface.text(
        "DRAWING",
        [(4, 4), (4, 64), (4, 124), (4, 184), (164, 184)],
        "#aaa",
        ["Temperature", "Memory Pressure", "Free Memory", "Stack Use", "Frequency"],
        font=TempeFont(ubuntu16bold),
    )
    freq_display = surface.text(
        "DRAWING",
        (240, 204),
        grey_7,
        str(freq() // 1000000),
        (RIGHT, TOP),
        font=large_numbers,
        clip=(164, 204, 76, 35),
    )
    freq_units = surface.text(
        "DRAWING",
        (252, 204),
        grey_7,
        "MHz",
        font=small_numbers,
        clip=(252, 204, 64, 35),
    )

    temp_source = PollADC(ADC.CORE_TEMP, 1)
    temperature = Value(25)
    free_memory = Value(0)
    allocated_memory = Value(0)
    stack_use = Value(0)

    update_temperature = temp_source | u16_to_celcius() | temperature
    update_free_memory = check_free(5) | free_memory
    update_allocated_memory = check_allocated(5) | allocated_memory
    update_stack_use = check_stack(5) | stack_use

    task1 = asyncio.create_task(display_temperature(surface, temperature))
    #task2 = asyncio.create_task(plot_spot_temperature(surface))
    task3 = asyncio.create_task(plot_average_temperature(surface, temperature))
    task4 = asyncio.create_task(refresh(surface, display))
    task5 = asyncio.create_task(display_free(surface, free_memory))
    task6 = asyncio.create_task(display_alloc(surface, allocated_memory))
    task7 = asyncio.create_task(display_stack(surface, stack_use))
    task8 = asyncio.create_task(plot_allocated(surface, allocated_memory))
    task9 = asyncio.create_task(plot_free(surface, free_memory))
    await asyncio.gather(
        update_temperature.create_task(),
        update_free_memory.create_task(),
        update_allocated_memory.create_task(),
        update_stack_use.create_task(),
        task1,
        #task2,
        task3,
        task4,
        task5,
        task6,
        task7,
        task8,
        task9,
        #return_exceptions=True,
    )


if __name__ == "__main__":
    asyncio.run(main())

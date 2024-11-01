# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

"""Example showing live updating of microcontroller state.

Note: this is currently not working as it uses earlier version of code.
"""


import asyncio
import gc
from machine import SPI, Pin, ADC, RTC
import micropython
import time

from ultimo.pipelines import Dedup, EWMA, pipe
from ultimo.poll import poll
from ultimo.value import Value
from ultimo_machine.gpio import PollADC
from ultimo_machine.time import PollRTC

from tempe.colors import grey_7, grey_a, grey_d, grey_e, grey_f
from tempe.markers import Marker
from tempe.surface import Surface
from tempe.component import Component, Label, LinePlot, ScatterPlot, BarPlot
from tempe.fonts import roboto16bold, roboto32boldnumbers, roboto24boldnumbers
from tempe.colormaps.plasma import plasma
from tempe.colormaps.viridis import viridis

from devices.st7789 import ST7789


w = 320
h = 240

gc.collect()
DRAWING_BUFFER = bytearray(2 * w * 31)


async def init_display():
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


def temp_to_color(temp):
    index = int((len(plasma) - 1) * (temp - 25) / 10)
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
    temp = await value()
    temp_display = Label(
        surface,
        (164, 20, 152, 60),
        temp,
        color=temp_to_color(temp),
        font=roboto32boldnumbers,
    )
    format = pipe("{:.1f}°C".format)
    async for temp in value | format() | Dedup():
        temp_display.value = temp
        temp_display.style["color"] = temp_to_color(await value())
        temp_display.update()


@pipe
def format_memory(memory):
    return f"{memory >> 10:d}"


async def display_free(surface, value):
    free = await value()
    free_display = Label(
        surface,
        (164, 144, 80, 60),
        free,
        color=free_to_color(free),
        font=roboto32boldnumbers,
    )
    free_units = Label(
        surface,
        (252, 144, 64, 60),
        "KiB",
        color=free_to_color(free),
        font=roboto24boldnumbers,
    )
    async for free in value | format_memory() | Dedup():
        free_display.value = free
        free_display.style["color"] = free_to_color(await value())
        free_units.style["color"] = free_to_color(await value())
        free_display.update()
        free_units.update()


async def display_alloc(surface, value):
    alloc = await value()
    alloc_display = Label(
        surface,
        (164, 84, 80, 60),
        alloc,
        color=alloc_to_color(alloc),
        font=roboto32boldnumbers,
    )
    alloc_units = Label(
        surface,
        (252, 84, 64, 60),
        "KiB",
        color=alloc_to_color(alloc),
        font=roboto24boldnumbers,
    )
    async for alloc in value | format_memory() | Dedup():
        alloc_display.value = alloc
        alloc_display.style["color"] = alloc_to_color(await value())
        alloc_units.style["color"] = alloc_to_color(await value())
        alloc_display.update()
        alloc_units.update()


async def display_stack(surface, value):
    stack = await value()
    stack_display = Label(
        surface,
        (4, 204, 152, 35),
        stack,
        color=stack_to_color(stack),
        font=roboto32boldnumbers,
    )
    format = pipe("{} B".format)
    async for stack in value | format() | Dedup():
        stack_display.value = stack
        stack_display.style["color"] = stack_to_color(await value())
        stack_display.update()


async def plot_average_temperature(surface, value):
    temp_source = PollADC(ADC.CORE_TEMP, 1)
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
        value_range=(27, 32),
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
        value_range=(27, 32),
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
        value_range=(27, 32),
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
        value_range=(0, 1 << 18),
        index_range=(0, 39),
    )
    free_plot.style["background_color"] = None
    async for free in value:
        frees[:-1] = frees[1:]
        frees[-1] = free
        colors[:-1] = colors[1:]
        colors[-1] = free_to_color(free)
        free_plot.update()


async def plot_stack(surface, value):
    index = list(range(39))
    stacks = [0] * 39
    colors = [0] * 39
    stack = await value()
    stack_plot = BarPlot(
        surface,
        (4, 200, 156, 20),
        values=stacks,
        index=index,
        colors=colors,
        value_range=(0, 1 << 13),
        index_range=(0, 39),
    )
    stack_plot.style["background_color"] = None
    stack_plot.draw()
    async for stack in value:
        print(stack)
        try:
            stacks[:-1] = stacks[1:]
            stacks[-1] = stack
            colors[:-1] = colors[1:]
            colors[-1] = stack_to_color(stack)
            stack_plot.update()
        except Exception as exc:
            print(exc)


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
    display = await init_display()
    surface = Surface()
    background = Component(surface, (0, 0, w, h))
    label_1 = Label(surface, (4, 4, 100, 20), "Temperature", font=roboto16bold)
    label_2 = Label(surface, (4, 64, 152, 20), "Memory Pressure", font=roboto16bold)
    label_3 = Label(surface, (4, 124, 152, 20), "Free Memory", font=roboto16bold)
    label_4 = Label(surface, (4, 184, 152, 20), "Stack Use", font=roboto16bold)
    label_5 = Label(surface, (164, 184, 152, 20), "Frequency", font=roboto16bold)
    freq_display = Label(
        surface,
        (164, 204, 76, 35),
        machine.freq() // 1000000,
        color=grey_7,
        font=roboto32boldnumbers,
    )
    freq_units = Label(
        surface,
        (252, 204, 64, 35),
        "MHz",
        color=grey_7,
        font=roboto24boldnumbers,
    )
    background.draw()
    label_1.draw()
    label_2.draw()
    label_3.draw()
    label_4.draw()
    label_5.draw()
    freq_display.draw()
    freq_units.draw()
    surface.damage((0, 0, w, h))

    temp_source = PollADC(ADC.CORE_TEMP, 1)
    temperature = Value(25)
    free_memory = Value(0)
    allocated_memory = Value(0)
    stack_use = Value(0)

    update_temperature = temp_source | u16_to_celcius() | EWMA(0.05) | temperature
    update_free_memory = check_free(5) | free_memory
    update_allocated_memory = check_allocated(5) | allocated_memory
    update_stack_use = check_stack(5) | stack_use

    task1 = asyncio.create_task(display_temperature(surface, temperature))
    task2 = asyncio.create_task(plot_spot_temperature(surface))
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
        task2,
        task3,
        task4,
        task5,
        task6,
        task7,
        task8,
        task9,
        return_exceptions=True,
    )


if __name__ == "__main__":
    asyncio.run(main())

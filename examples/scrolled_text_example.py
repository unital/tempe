# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

"""Example showing scrolling text up/down with buttons."""

import asyncio
import gc
from machine import Signal, Pin

from tempe.font import TempeFont
from tempe.fonts import ubuntu16bold
from tempe.surface import Surface, BACKGROUND, DRAWING
from tempe.text import CENTER, TOP
from tempe.window import Window
from example_fonts import ubuntu12italic


# maximize available memory before allocating buffer
gc.collect()

# A buffer one half the size of a 320x240 screen
# NOTE: If you get MemoryErrors, make this smaller
working_buffer = bytearray(2 * 320 * 121)


# Buttons
up = Signal(15, Pin.IN, Pin.PULL_UP, invert=True)
down = Signal(14, Pin.IN, Pin.PULL_UP, invert=True)

# Japperwocky by Lewis Caroll
JABBERWOCKY = """'Twas brillig, and the slithy toves
Did gyre and gimble in the wabe;
All mimsy were the borogoves,
And the mome raths outgrabe.

"Beware the Jabberwock, my son!
The jaws that bite, the claws that catch!
Beware the Jubjub bird, and shun
The frumious Bandersnatch!"

He took his vorpal sword in hand:
Long time the manxome foe he sought-
So rested he by the Tumtum tree,
And stood awhile in thought.

And as in uffish thought he stood,
The Jabberwock, with eyes of flame,
Came whiffling through the tulgey wood,
And burbled as it came!

One, two! One, two! And through and through
The vorpal blade went snicker-snack!
He left it dead, and with its head
He went galumphing back.

"And hast thou slain the Jabberwock?
Come to my arms, my beamish boy!
O frabjous day! Callooh! Callay!"
He chortled in his joy.

'Twas brillig, and the slithy toves
Did gyre and gimble in the wabe;
All mimsy were the borogoves,
And the mome raths outgrabe."""

class Scroller:

    def __init__(self, window, max_scroll, step=10):
        self.window = window
        self.max_scroll = max_scroll
        self.step = step
        self.top = window.clip[1]
        self.height = window.clip[3]
        self._scroll = 0

    @property
    def scroll(self):
        return self._scroll

    @scroll.setter
    def scroll(self, value):
        self._scroll = min(max(value, 0), self.max_scroll - self.height)
        x = self.window.offset[0]
        y = self.top - self._scroll
        self.window.update(offset=(x, y))

    def up(self):
        self.scroll += self.step

    def down(self):
        self.scroll -= self.step


async def init_surface(surface):
    # fill the background with off-white pixels
    surface.rectangles(BACKGROUND, (0, 0, 320, 240), "#fff")
    title = surface.text(DRAWING, (0, 0, 160, 16), "#222", "Jabberwocky", font=TempeFont(ubuntu16bold))

    window = Window(offset=(4, 20), clip=(4, 20, 312, 212))
    surface.add_shape(DRAWING, window)
    text = window.subsurface.text(DRAWING, (156, 0), "#222", JABBERWOCKY, (CENTER, TOP), font=TempeFont(ubuntu12italic))
    x, y, w, h = text._get_bounds()
    scroller = Scroller(window, h, text.font.height)
    return scroller


async def refresh_display(surface, display, working_buffer):
    import time

    while True:
        await surface.refresh_needed.wait()
        await surface.arefresh(display, working_buffer)

async def scroll(scroller):
    while True:
        await asyncio.sleep(0.1)
        if down():
            scroller.down()
            while down():
                await asyncio.sleep(0.1)
        if up():
            scroller.up()
            while up():
                await asyncio.sleep(0.1)


async def run(display=None):
    """Initialize the devices and update when values change."""

    # initialize objects
    tasks = []
    if display is None:
        try:
            from tempe_config import init_display

            tasks.append(init_display())
        except ImportError:
            print(
                "Could not find tempe_config.init_display.\n\n"
                "To run examples, you must create a top-level tempe_config module containing\n"
                "an async init_display function that returns a display.\n\n"
                "See https://unital.github.io/tempe more information.\n\n"
            )
            raise

    surface = Surface()
    tasks.append(init_surface(surface))

    # asynchronously initialize
    results = await asyncio.gather(*tasks)
    if display is None:
        display = results[0]
    scroller = results[-1]

    # poll scroll buttons and update display forever
    await asyncio.gather(
        refresh_display(surface, display, working_buffer),
        scroll(scroller),
    )


def main(display=None):
    """Render the surface and return the display object."""
    asyncio.run(run(display))
    return display


if __name__ == '__main__':
    display = main()

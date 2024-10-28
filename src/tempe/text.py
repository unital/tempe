# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

from array import array
import framebuf

from .font import BitmapFont
from .shapes import ColoredGeometry, BLIT_KEY_RGB565


class Text(ColoredGeometry):
    def __init__(
        self, geometry, colors, texts, *, bold=False, font=None, surface=None, clip=None
    ):
        super().__init__(geometry, colors, surface=surface, clip=clip)
        self.texts = texts
        self.bold = bold
        self.font = font

    def __iter__(self):
        yield from zip(self.geometry, self.colors, self.texts)

    def draw(self, buffer, x=0, y=0):
        if self.font is None:
            line_height = 10
            for geometry, color, text in self:
                px = geometry[0] - x
                py = geometry[1] - y
                for i, line in enumerate(text.splitlines()):
                    buffer.text(line, px, py + i * line_height, color)
                    if self.bold:
                        buffer.text(line, px + 1, py + i * line_height, color)
        elif isinstance(self.font, BitmapFont):
            line_height = self.font.height
            palette_buf = array("H", [BLIT_KEY_RGB565, 0xFFFF])
            palette = framebuf.FrameBuffer(palette_buf, 2, 1, framebuf.RGB565)
            for geometry, color, text in self:
                palette_buf[1] = color
                py = geometry[1] - y
                for i, line in enumerate(text.splitlines()):
                    px = geometry[0] - x
                    for char in line:
                        buf, height, width = self.font.bitmap(char)
                        buf = bytearray(buf)
                        fbuf = framebuf.FrameBuffer(
                            buf, width, height, framebuf.MONO_HLSB
                        )
                        buffer.blit(fbuf, px, py, BLIT_KEY_RGB565, palette)
                        px += width
                    py += line_height

    def update(self, geometry=None, colors=None, texts=None):
        if texts is not None:
            if self.clip is None:
                # invalidate old text bounds
                if self._get_bounds is None:
                    self._get_bounds = self._get_bounds()
                self.surface.damage(self._get_bounds)
            self.texts = texts
            # bounds are no longer valid
            self._get_bounds = None
        super().update(geometry=geometry, colors=colors)

    def _get_bounds(self):
        max_x = -0x7FFF
        min_x = 0x7FFF
        max_y = -0x7FFF
        min_y = 0x7FFF
        if self.font is None:
            for geometry, text in zip(self.geometry, self.texts):
                width = 8 * max(len(line) for line in text.splitlines())
                height = 8 * len(text.splitlines())
                max_x = max(max_x, geometry[0] + width)
                min_x = min(min_x, geometry[0])
                max_y = max(max_y, geometry[1] + height)
                min_y = min(min_y, geometry[1])
        else:
            for geometry, text in zip(self.geometry, self.texts):
                width = max(self.font.measure(line)[2] for line in text.splitlines())
                height = self.font.height * len(text.splitlines())
                max_x = max(max_x, geometry[0] + width)
                min_x = min(min_x, geometry[0])
                max_y = max(max_y, geometry[1] + height)
                min_y = min(min_y, geometry[1])

        return (min_x, min_y, max_x - min_x, max_y - min_y)

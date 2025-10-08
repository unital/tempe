# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

from array import array
import framebuf

from .data_view import Repeat
from .font import BitmapFont
from .shapes import ColoredGeometry, BLIT_KEY_RGB565

LEFT = 0
RIGHT = 1
CENTER = 2
TOP = 3
BOTTOM = 4

class Text(ColoredGeometry):
    def __init__(
        self,
        geometry,
        colors,
        texts,
        alignments=Repeat((LEFT, TOP)),
        *,
        bold=False,
        font=None,
        line_spacing=0,
        surface=None,
        clip=None,
    ):
        super().__init__(geometry, colors, surface=surface, clip=clip)
        self.texts = texts
        self.bold = bold
        self.font = font
        self.line_spacing = line_spacing
        self.alignments = alignments

    def __iter__(self):
        yield from zip(self.geometry, self.colors, self.texts, self.alignments)

    def draw_raster(self, raster):
        buffer = raster.fbuf
        x = raster.x
        y = raster.y
        w = raster.w
        h = raster.h
        if self.font is None:
            line_height = 10 + self.line_spacing
            for geometry, color, text, alignment in self:
                px = geometry[0] - x
                py = geometry[1] - y + 1
                halign, valign = alignment
                lines = text.splitlines()
                text_height = len(lines) * line_height - self.line_spacing
                if valign == BOTTOM:
                    py -= text_height
                elif valign == CENTER:
                    py -= text_height // 2
                if py > h or py + text_height < 0:
                    continue
                for i, line in enumerate(lines):
                    ly = py + i * line_height
                    if ly > h:
                        break
                    line_width = 8 * len(line)
                    lx = px
                    if halign == RIGHT:
                        lx = px - line_width
                    elif halign == CENTER:
                        lx = px - line_width // 2
                    if lx + line_width < 0 or lx > w or ly + line_height < 0:
                        continue
                    buffer.text(line, lx, ly, color)
                    if self.bold:
                        buffer.text(line, lx + 1, ly, color)
        elif isinstance(self.font, BitmapFont):
            line_height = self.font.height + self.line_spacing
            palette_buf = array("H", [BLIT_KEY_RGB565, 0xFFFF])
            palette = framebuf.FrameBuffer(palette_buf, 2, 1, framebuf.RGB565)
            char_buf = [None, None, None, framebuf.MONO_HLSB]
            for geometry, color, text, alignments in self:
                palette_buf[1] = color
                py = geometry[1] - y
                px = geometry[0] - x
                halign, valign = alignments
                lines = text.splitlines()
                text_height = len(lines) * line_height - self.line_spacing
                if valign == BOTTOM:
                    py -= text_height
                elif valign == CENTER:
                    py -= text_height // 2
                if py > h or py + text_height < 0:
                    continue
                for line in lines:
                    widths = [self.font.measure(c)[2] for c in line]
                    line_width = sum(widths)
                    lx = px
                    if halign == RIGHT:
                        lx = px - line_width
                    elif halign == CENTER:
                        lx = px - line_width // 2
                    if lx + line_width >= 0 and py + line_height >= 0:
                        for char, width in zip(line, widths):
                            char_buf[1] = width
                            if lx > w:
                                break
                            if lx + width >= 0:
                                char_buf[0], char_buf[2], _ = self.font.bitmap(char)
                                buffer.blit(char_buf, lx, py, BLIT_KEY_RGB565, palette)
                            lx += width
                    py += line_height
                    if py > h:
                        break

    def update(self, geometry=None, colors=None, texts=None, alignments=None, font=None):
        if texts is not None or alignments is not None:
            if self.clip is None:
                # invalidate old text bounds
                if self._bounds is None:
                    self._bounds = self._get_bounds()
                if self.surface:
                    self.surface.damage(self._bounds)
            if texts is not None:
                self.texts = texts
            if alignments is not None:
                self.alignments = alignments
            if font is not None:
                self.font = font
            # bounds are no longer valid
            self._bounds = None
        super().update(geometry=geometry, colors=colors)

    def _get_bounds(self):
        max_x = -0x7FFF
        min_x = 0x7FFF
        max_y = -0x7FFF
        min_y = 0x7FFF
        if self.font is None:
            line_height = 10 + self.line_spacing
            for geometry, text, alignments in zip(self.geometry, self.texts, self.alignments):
                if not text:
                    continue
                width = 8 * max(len(line) for line in text.splitlines())
                height = line_height * len(text.splitlines()) - self.line_spacing
                halign, valign = alignments
                if halign == RIGHT:
                    max_x = max(max_x, geometry[0])
                    min_x = min(min_x, geometry[0] - width)
                elif halign == CENTER:
                    max_x = max(max_x, geometry[0] + width // 2)
                    min_x = min(min_x, geometry[0] - width // 2)
                else:
                    max_x = max(max_x, geometry[0] + width)
                    min_x = min(min_x, geometry[0])
                if valign == BOTTOM:
                    max_y = max(max_y, geometry[1])
                    min_y = min(min_y, geometry[1] - height)
                elif valign == CENTER:
                    max_y = max(max_y, geometry[1] + height // 2)
                    min_y = min(min_y, geometry[1] - height // 2)
                else:
                    max_y = max(max_y, geometry[1] + height)
                    min_y = min(min_y, geometry[1])
        else:
            line_height = self.font.height + self.line_spacing
            for geometry, text, alignments in zip(self.geometry, self.texts, self.alignments):
                if not text:
                    continue
                width = max(self.font.measure(line)[2] for line in text.splitlines())
                height = line_height * len(text.splitlines()) - self.line_spacing
                halign, valign = alignments
                if halign == RIGHT:
                    max_x = max(max_x, geometry[0])
                    min_x = min(min_x, geometry[0] - width)
                elif halign == CENTER:
                    max_x = max(max_x, geometry[0] + width // 2 + 1)
                    min_x = min(min_x, geometry[0] - width // 2 - 1)
                else:
                    max_x = max(max_x, geometry[0] + width)
                    min_x = min(min_x, geometry[0])
                if valign == BOTTOM:
                    max_y = max(max_y, geometry[1])
                    min_y = min(min_y, geometry[1] - height)
                elif valign == CENTER:
                    max_y = max(max_y, geometry[1] + height // 2 + 1)
                    min_y = min(min_y, geometry[1] - height // 2 - 1)
                else:
                    max_y = max(max_y, geometry[1] + height)
                    min_y = min(min_y, geometry[1])
        if max_x < min_x or max_y < min_y:
            return (0, 0, 0, 0)
        return (min_x, min_y, max_x - min_x, max_y - min_y)

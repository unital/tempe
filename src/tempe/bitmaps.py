# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

from array import array
import framebuf

from .shapes import ColoredGeometry, Shape, BLIT_KEY_RGB565
from .util import blit_argb16_rgb565


class Bitmaps(Shape):
    """Draw framebuffer bitmaps at points"""

    def __init__(
        self, geometry, buffers, *, key=-1, palette=None, alpha=False, surface=None, clip=None
    ):
        super().__init__(surface, clip=clip)
        self.geometry = geometry
        self.buffers = buffers
        self.key = key
        self.palette = palette
        self.alpha = alpha

    def update(self, geometry=None, buffers=None):
        if geometry is not None:
            if self.clip is None:
                # invalidate old geometry bounds
                if self._bounds is None:
                    self._bounds = self._get_bounds()
                self.surface.damage(self._bounds)
            self.geometry = geometry
            # bounds are no longer valid
            self._bounds = None
        if buffers is not None:
            self.buffers = buffers
        super().update()

    def __len__(self):
        return len(self.geometry)

    def __iter__(self):
        yield from zip(self.geometry, self.buffers)

    def draw_raster(self, raster):
        buffer = raster.fbuf
        x = raster.x
        y = raster.y
        w = raster.w
        h = raster.h
        if self.palette is not None:
            palette = framebuf.FrameBuffer(
                self.palette, len(self.palette), 1, framebuf.RGB565
            )
        for geometry, fbuf in self:
            px = geometry[0] - x
            py = geometry[1] - y
            pw = geometry[2]
            ph = geometry[3]
            if (px + pw < 0 or px > w or py + ph < 0 or py > h):
                continue
            if self.palette is not None:
                buffer.blit(fbuf, px, py, self.key, palette)
            elif self.alpha:
                blit_argb16_rgb565(
                    raster.buf, w, h, raster.stride, memoryview(fbuf), px, py, pw, ph, pw
                )
            else:
                buffer.blit(fbuf, px, py, self.key)

    def _get_bounds(self):
        max_x = -0x7FFF
        min_x = 0x7FFF
        max_y = -0x7FFF
        min_y = 0x7FFF
        for geometry in self.geometry:
            max_x = max(max_x, geometry[0], geometry[0] + geometry[2])
            min_x = min(min_x, geometry[0], geometry[0] + geometry[2])
            max_y = max(max_y, geometry[1], geometry[1] + geometry[3])
            min_y = min(min_y, geometry[1], geometry[1] + geometry[3])

        return (min_x, min_y, max_x - min_x, max_y - min_y)


class ColoredBitmaps(ColoredGeometry):
    """Draw 1-bit framebuffers bitmaps at points in given colors."""

    def __init__(self, geometry, colors, buffers, *, surface=None, clip=None):
        super().__init__(geometry, colors, surface=surface, clip=clip)
        self.buffers = buffers

    def update(self, geometry=None, colors=None, buffers=None):
        if buffers is not None:
            self.buffers = buffers
        super().update(geometry=geometry, colors=colors)

    def __len__(self):
        return len(self.geometry)

    def __iter__(self):
        yield from zip(self.geometry, self.colors, self.buffers)

    def draw_raster(self, raster):
        buffer = raster.fbuf
        x = raster.x
        y = raster.y
        w = raster.w
        h = raster.h
        palette_buf = array("H", [BLIT_KEY_RGB565, 0x0000])
        palette = framebuf.FrameBuffer(palette_buf, 2, 1, framebuf.RGB565)
        for geometry, color, buf in self:
            palette_buf[1] = color
            px = geometry[0] - x
            py = geometry[1] - y
            pw = geometry[2]
            ph = geometry[3]
            if (px + pw < 0 or px > w or py + ph < 0 or py > h):
                continue
            buffer.blit(buf, px, py, BLIT_KEY_RGB565, palette)

    def _get_bounds(self):
        max_x = -0x7FFF
        min_x = 0x7FFF
        max_y = -0x7FFF
        min_y = 0x7FFF
        for geometry in self.geometry:
            max_x = max(max_x, geometry[0], geometry[0] + geometry[2])
            min_x = min(min_x, geometry[0], geometry[0] + geometry[2])
            max_y = max(max_y, geometry[1], geometry[1] + geometry[3])
            min_y = min(min_y, geometry[1], geometry[1] + geometry[3])

        return (min_x, min_y, max_x - min_x, max_y - min_y)

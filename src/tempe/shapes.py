# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

"""Shape classes which efficiently draw primitives."""

import asyncio
from .util import intersect_poly_rect

#: Transparent color when blitting bitmaps.
BLIT_KEY_RGB565 = const(0b0000000000100000)


class Shape:
    """ABC for drawable objects."""

    def __init__(self, surface=None, clip=None):
        self.surface = surface
        self.clip = clip
        self._bounds = None

    def draw(self, buffer, x=0, y=0):
        # draw nothing
        pass

    def draw_raster(self, raster):
        self.draw(raster.fbuf, raster.x, raster.y)

    def update(self):
        if self.clip is None:
            if self._bounds is None:
                self._bounds = self._get_bounds()
            if self.surface:
                self.surface.damage(self._bounds)
        elif self.surface:
            self.surface.damage(self.clip)

    def _get_bounds(self):
        raise NotImplementedError()


class ColoredGeometry(Shape):
    """ABC for geometries with colors applied."""

    def __init__(self, geometry, colors, *, surface=None, clip=None):
        super().__init__(surface, clip=clip)
        self.geometry = geometry
        self.colors = colors

    def update(self, geometry=None, colors=None):
        if geometry is not None:
            if self.clip is None:
                # invalidate old geometry bounds
                if self._bounds is None:
                    self._bounds = self._get_bounds()
                if self.surface:
                    self.surface.damage(self._bounds)
            self.geometry = geometry
            # bounds are no longer valid
            self._bounds = None
        if colors is not None:
            self.colors = colors
        super().update()

    def __len__(self):
        return len(self.geometry)

    def __iter__(self):
        yield from zip(self.geometry, self.colors)


class SizedGeometry(ColoredGeometry):
    """ABC for geometries where there is a size associated with each object."""

    def __init__(self, geometry, colors, sizes, *, surface=None, clip=None):
        super().__init__(geometry, colors, surface=surface, clip=clip)
        self.sizes = sizes

    def update(self, geometry=None, colors=None, sizes=None):
        if sizes is not None:
            if self.clip is None:
                # invalidate old geometry bounds
                if self._bounds is None:
                    self._bounds = self._get_bounds()
                if self.surface:
                    self.surface.damage(self._bounds)
            self.sizes = sizes
            if geometry is not None:
                # don't need to redo bounds in super call, just record changes
                self.geometry = geometry
                geometry = None
            # bounds are no longer valid
            self._bounds = None
        super().update(geometry, colors)

    def __len__(self):
        return len(self.geometry)

    def __iter__(self):
        yield from zip(self.geometry, self.colors, self.sizes)


class FillableGeometry(ColoredGeometry):
    """ABC for geometries which can either be filled or stroked.

    Stroked outlines always have line with 1.
    """

    def __init__(self, geometry, colors, *, fill=True, surface=None, clip=None):
        super().__init__(geometry, colors, surface=surface, clip=clip)
        self.fill = fill

    def update(self, geometry=None, colors=None, fill=None):
        if fill is not None:
            self.fill = fill
        super().update(geometry=geometry, colors=colors)


class Lines(ColoredGeometry):
    """Render multiple colored line segments with line-width 1.

    Geometry should produce x0, y0, x1, y1 arrays.
    """

    def draw_raster(self, raster):
        buffer = raster.fbuf
        x = raster.x
        y = raster.y
        w = raster.w
        h = raster.h
        for geometry, color in self:
            if intersect_poly_rect(geometry, 4, x, y, w, h):
                x0 = geometry[0] - x
                y0 = geometry[1] - y
                x1 = geometry[2] - x
                y1 = geometry[3] - y
                buffer.line(x0, y0, x1, y1, color)

    def _get_bounds(self):
        max_x = -0x7FFF
        min_x = 0x7FFF
        max_y = -0x7FFF
        min_y = 0x7FFF
        for geometry in self.geometry:
            max_x = max(max_x, geometry[0], geometry[2])
            min_x = min(min_x, geometry[0], geometry[2])
            max_y = max(max_y, geometry[1], geometry[3])
            min_y = min(min_y, geometry[1], geometry[3])

        return (min_x - 1, min_y - 1, max_x - min_x + 2, max_y - min_y + 2)


class HLines(ColoredGeometry):
    """Render multiple colored horizontal line segments with line-width 1.

    Geometry should produce x0, y0, l arrays.
    """

    def draw(self, buffer, x=0, y=0):
        for geometry, color in self:
            px = geometry[0] - x
            py = geometry[1] - y
            l = geometry[2]
            buffer.hline(px, py, l, color)

    def _get_bounds(self):
        max_x = -0x7FFF
        min_x = 0x7FFF
        max_y = -0x7FFF
        min_y = 0x7FFF
        for geometry in self.geometry:
            max_x = max(max_x, geometry[0], geometry[0] + geometry[2])
            min_x = min(min_x, geometry[0], geometry[0] + geometry[2])
            max_y = max(max_y, geometry[1])
            min_y = min(min_y, geometry[1])

        return (min_x - 1, min_y - 1, max_x - min_x + 2, max_y - min_y + 2)


class VLines(ColoredGeometry):
    """Render multiple colored vertical line segments with line-width 1.

    Geometry should produce x0, y0, l arrays.
    """

    def draw(self, buffer, x=0, y=0):
        for geometry, color in self:
            px = geometry[0] - x
            py = geometry[1] - y
            l = geometry[2]
            buffer.vline(px, py, l, color)

    def _get_bounds(self):
        max_x = -0x7FFF
        min_x = 0x7FFF
        max_y = -0x7FFF
        min_y = 0x7FFF
        for geometry in self.geometry:
            max_x = max(max_x, geometry[0])
            min_x = min(min_x, geometry[0])
            max_y = max(max_y, geometry[1], geometry[1] + geometry[2])
            min_y = min(min_y, geometry[1], geometry[1] + geometry[2])

        return (min_x - 1, min_y - 1, max_x - min_x + 2, max_y - min_y + 2)


class PolyLines(ColoredGeometry):
    """Render multiple colored polylines with line-width 1.

    Geometry should produce x0, y0, x1, y1 arrays.
    """

    def draw_raster(self, raster):
        buffer = raster.fbuf
        x = raster.x
        y = raster.y
        w = raster.w
        h = raster.h
        for geometry, color in self:
            if intersect_poly_rect(geometry, len(geometry), x, y, w, h):
                for i in range(0, len(geometry) - 2, 2):
                    x0 = geometry[i] - x
                    y0 = geometry[i + 1] - y
                    x1 = geometry[i + 2] - x
                    y1 = geometry[i + 3] - y
                    buffer.line(x0, y0, x1, y1, color)

    def _get_bounds(self):
        max_x = -0x7FFF
        min_x = 0x7FFF
        max_y = -0x7FFF
        min_y = 0x7FFF
        for geometry in self.geometry:
            geometry = list(geometry)
            max_x = max(max_x, max(geometry[::2]))
            min_x = min(min_x, min(geometry[::2]))
            max_y = max(max_y, max(geometry[1::2]))
            min_y = min(min_y, min(geometry[1::2]))

        return (min_x - 1, min_y - 1, max_x - min_x + 2, max_y - min_y + 2)


class Polygons(FillableGeometry):
    """Render multiple polygons.

    Geometry should produce vertex buffers.
    """

    def draw_raster(self, raster):
        buffer = raster.fbuf
        x = raster.x
        y = raster.y
        w = raster.w
        h = raster.h
        for polygon, color in self:
            if intersect_poly_rect(polygon, len(polygon), x, y, w, h):
                buffer.poly(-x, -y, polygon, color, self.fill)

    def _get_bounds(self):
        max_x = -0x7FFF
        min_x = 0x7FFF
        max_y = -0x7FFF
        min_y = 0x7FFF
        for geometry in self.geometry:
            geometry = list(geometry)
            max_x = max(max_x, max(geometry[::2]))
            min_x = min(min_x, min(geometry[::2]))
            max_y = max(max_y, max(geometry[1::2]))
            min_y = min(min_y, min(geometry[1::2]))

        return (min_x - 1, min_y - 1, max_x - min_x + 2, max_y - min_y + 2)


class Rectangles(FillableGeometry):
    """Render multiple rectangles.

    Geometry should produce x, y, w, h arrays.
    """

    def draw(self, buffer, x=0, y=0):
        for rect, color in self:
            px = rect[0] - x
            py = rect[1] - y
            w = rect[2]
            h = rect[3]
            if w < 0:
                px += w
                w = -w
            if h < 0:
                py += h
                h = -h
            buffer.rect(px, py, w, h, color, self.fill)

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


class RoundedRectangles(Rectangles):
    """Render multiple rounded rectangles.

    Geometry should produce x, y, w, h arrays.
    """

    def __init__(self, geometry, colors, *, radius=4, fill=True, surface=None, clip=None):
        super().__init__(geometry, colors, fill=fill, surface=surface, clip=clip)
        self.radius = radius

    def draw(self, buffer, x=0, y=0):
        fill = self.fill
        for rect, color in self:
            px = rect[0] - x
            py = rect[1] - y
            w = rect[2]
            h = rect[3]
            if w < 0:
                px += w
                w = -w
            if h < 0:
                py += h
                h = -h
            # keep pixels within original bounds
            w -= 1
            h -= 1
            r = min(self.radius, w // 2, h // 2)
            if fill:
                buffer.rect(px + r, py, w - 2*r, h + 1, color, fill)
                buffer.rect(px, py + r, r, h - 2*r, color, fill)
                buffer.rect(px + w - r, py + r, r + 1, h - 2*r, color, fill)
            else:
                buffer.hline(px + r, py, w - 2*r, color)
                buffer.hline(px + r, py + h, w - 2*r, color)
                buffer.vline(px, py + r, h - 2*r, color)
                buffer.vline(px + w, py + r, h - 2*r, color)
            if r == 0:
                # Avoid https://github.com/micropython/micropython/issues/16053
                buffer.pixel(px, py, color)
                buffer.pixel(px, py + h, color)
                buffer.pixel(px + w, py, color)
                buffer.pixel(px + w, py + h, color)
            else:
                buffer.ellipse(px + w - r, py + r, r, r, color, fill, 1)
                buffer.ellipse(px + w - r, py + h - r, r, r, color, fill, 8)
                buffer.ellipse(px + r, py + h - r, r, r, color, fill, 4)
                buffer.ellipse(px + r, py + r, r, r, color, fill, 2)

    def update(self, geometry=None, colors=None, fill=None, radius=None):
        if radius is not None:
            self.radius = radius
        super().update(geometry=geometry, colors=colors, fill=fill)


class Circles(FillableGeometry):
    """Render multiple circles.

    Geometry should produce cx, cy, r arrays.
    """

    def draw_raster(self, raster):
        buffer = raster.fbuf
        x = raster.x
        y = raster.y
        w = raster.w
        h = raster.h
        for geometry, color in self:
            px = geometry[0] - x
            py = geometry[1] - y
            r = geometry[2]
            if px + r < 0 or px - r > w or py + r < 0 or py - r> h:
                continue
            if r == 0:
                # Avoid https://github.com/micropython/micropython/issues/16053
                continue
            buffer.ellipse(px, py, r, r, color, self.fill)

    def _get_bounds(self):
        max_x = -0x7FFF
        min_x = 0x7FFF
        max_y = -0x7FFF
        min_y = 0x7FFF
        for geometry in self.geometry:
            max_x = max(max_x, geometry[0] + abs(geometry[2]))
            min_x = min(min_x, geometry[0] - abs(geometry[2]))
            max_y = max(max_y, geometry[1] + abs(geometry[2]))
            min_y = min(min_y, geometry[1] - abs(geometry[2]))

        return (min_x - 1, min_y - 1, max_x - min_x + 2, max_y - min_y + 2)


class Ellipses(FillableGeometry):
    """Render multiple ellipses.

    Geometry should produce cx, cy, rx, ry arrays.
    """

    def draw_raster(self, raster):
        buffer = raster.fbuf
        x = raster.x
        y = raster.y
        w = raster.w
        h = raster.h
        for geometry, color in self:
            px = geometry[0] - x
            py = geometry[1] - y
            rx = geometry[2]
            ry = geometry[3]
            if px + rx < 0 or px - rx > w or py + ry < 0 or py - ry > h:
                continue
            if rx == 0 and ry == 0:
                # Avoid https://github.com/micropython/micropython/issues/16053
                continue
            buffer.ellipse(px, py, rx, ry, color, self.fill)

    def _get_bounds(self):
        max_x = -0x7FFF
        min_x = 0x7FFF
        max_y = -0x7FFF
        min_y = 0x7FFF
        for geometry in self.geometry:
            max_x = max(max_x, geometry[0] + abs(geometry[2]))
            min_x = min(min_x, geometry[0] - abs(geometry[2]))
            max_y = max(max_y, geometry[1] + abs(geometry[3]))
            min_y = min(min_y, geometry[1] - abs(geometry[3]))

        return (min_x - 1, min_y - 1, max_x - min_x + 2, max_y - min_y + 2)

"""Shape classes which efficiently draw primitives."""

import asyncio

#: Transparent color when blitting bitmaps.
BLIT_KEY_RGB565 = const(0b0000000000100000)


class Shape:
    """ABC for drawable objects."""

    def __init__(self, surface=None, clip=None):
        self.surface = surface
        self.clip = clip

    def draw(self, buffer, x=0, y=0):
        # draw nothing
        pass

    def update(self):
        if self.clip is None:
            self.clip = self._bounds()
        self.surface.damage(self.clip)

    def _bounds(self):
        raise NotImplementedError()


class ColoredGeometry(Shape):
    """ABC for geometries with colors applied."""

    def __init__(self, geometry, colors, *, surface=None, clip=None):
        super().__init__(surface, clip=clip)
        self.geometry = geometry
        self.colors = colors

    def update(self, geometry=None, colors=None):
        if geometry is not None:
            self.geometry = geometry
        if colors is not None:
            self.colors = colors
        super().update()

    def __len__(self):
        return len(self.geometry)

    def __iter__(self):
        yield from zip(self.geometry, self.colors)


class FillableGeometry(ColoredGeometry):
    """ABC for geometries which can either be filled or stroked.

    Stroked outlines always have line with 1.
    """

    def __init__(self, geometry, colors, *, fill=True, surface=None, clip=None):
        super().__init__(geometry, colors, surface=surface, clip=clip)
        self.fill = fill


class Lines(ColoredGeometry):
    """Render multiple colored line segments with line-width 1.

    Geometry should produce x0, y0, x1, y1 arrays.
    """

    def draw(self, buffer, x=0, y=0):
        for geometry, color in self:
            x0 = geometry[0] - x
            y0 = geometry[1] - y
            x1 = geometry[2] - x
            y1 = geometry[3] - y
            buffer.line(x0, y0, x1, y1, color)

    def _bounds(self):
        max_x = -0x7fff
        min_x = 0x7fff
        max_y = -0x7fff
        min_y = 0x7fff
        for geometry in self.geometry:
            max_x = max(max_x, geometry[0], geometry[2])
            min_x = min(min_x, geometry[0], geometry[2])
            max_y = max(max_y, geometry[1], geometry[3])
            min_y = min(min_y, geometry[1], geometry[3])

        return (min_x, min_y, max_x - min_x, max_y - min_y)



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

    def _bounds(self):
        max_x = -0x7fff
        min_x = 0x7fff
        max_y = -0x7fff
        min_y = 0x7fff
        for geometry in self.geometry:
            max_x = max(max_x, geometry[0], geometry[0] + geometry[2])
            min_x = min(min_x, geometry[0], geometry[0] + geometry[2])
            max_y = max(max_y, geometry[1])
            min_y = min(min_y, geometry[1])

        return (min_x, min_y, max_x - min_x, max_y - min_y)


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

    def _bounds(self):
        max_x = -0x7fff
        min_x = 0x7fff
        max_y = -0x7fff
        min_y = 0x7fff
        for geometry in self.geometry:
            max_x = max(max_x, geometry[0])
            min_x = min(min_x, geometry[0])
            max_y = max(max_y, geometry[1], geometry[1] + geometry[2])
            min_y = min(min_y, geometry[1], geometry[1] + geometry[2])

        return (min_x, min_y, max_x - min_x, max_y - min_y)


class Polygons(FillableGeometry):
    """Render multiple polygons.

    Geometry should produce vertex buffers.
    """

    def draw(self, buffer, x=0, y=0):
        for polygon, color in self:
            buffer.poly(-x, -y, polygon, color, self.fill)

    def _bounds(self):
        max_x = -0x7fff
        min_x = 0x7fff
        max_y = -0x7fff
        min_y = 0x7fff
        for geometry in self.geometry:
            max_x = max(max_x, max(geometry[::2]))
            min_x = min(min_x, min(geometry[::2]))
            max_y = max(max_y, max(geometry[1::2]))
            min_y = min(min_y, min(geometry[1::2]))

        return (min_x, min_y, max_x - min_x, max_y - min_y)


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

    def _bounds(self):
        max_x = -0x7fff
        min_x = 0x7fff
        max_y = -0x7fff
        min_y = 0x7fff
        for geometry in self.geometry:
            max_x = max(max_x, geometry[0], geometry[0] + geometry[2])
            min_x = min(min_x, geometry[0], geometry[0] + geometry[2])
            max_y = max(max_y, geometry[1], geometry[1] + geometry[3])
            min_y = min(min_y, geometry[1], geometry[1] + geometry[3])

        return (min_x, min_y, max_x - min_x, max_y - min_y)


class Circles(FillableGeometry):
    """Render multiple circles.

    Geometry should produce cx, cy, r arrays.
    """

    def draw(self, buffer, x=0, y=0):
        for geometry, color in self:
            px = geometry[0] - x
            py = geometry[1] - y
            r = geometry[2]
            buffer.ellipse(px, py, r, r, color, self.fill)


class Ellipses(FillableGeometry):
    """Render multiple ellipses.

    Geometry should produce cx, cy, rx, ry arrays.
    """

    def draw(self, buffer, x=0, y=0):
        for geometry, color in self:
            px = geometry[0] - x
            py = geometry[1] - y
            rx = geometry[2]
            ry = geometry[3]
            buffer.ellipse(px, py, rx, ry, color, self.fill)

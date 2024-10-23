import asyncio
from array import array

from .raster import Raster
from .shapes import Circles, Ellipses, Polygons, Rectangles, Lines, VLines, HLines
from .util import contains


LAYERS = const(("BACKGROUND", "UNDERLAY", "IMAGE", "DRAWING", "OVERLAY"))


class Surface:
    """A space for drawing shapes."""

    def __init__(self):
        self.layers = {layer: [] for layer in LAYERS}
        self._damage = []
        self.refresh_needed = asyncio.Event()

    def draw(self, raster):
        for layer in LAYERS:
            for object in self.layers[layer]:
                if object.clip is None:
                    clip = raster
                else:
                    clip = raster.clip(*object.clip)
                    if clip is None:
                        continue
                object.draw_raster(clip)

    def refresh(self, display, working_buffer):
        for rect in self._damage:
            x, y, w, h = rect
            # handle buffer too small
            buffer_rows = (len(working_buffer) // (2*w)) - 1
            for start_row in range(0, h, buffer_rows):
                raster_rows = min(buffer_rows, h - start_row)
                raster = Raster(working_buffer, x, y + start_row, w, raster_rows)
                self.draw(raster)
                display.blit(working_buffer, x, y + start_row, w, raster_rows)
        self._damage = []
        self.refresh_needed.clear()

    def damage(self, rect):
        if not any(contains(rect, rect2) for rect2 in self._damage):
            self._damage = [rect2 for rect2 in self._damage if not contains(rect2, rect)]
            self._damage.append(rect)
            self.refresh_needed.set()

    def clear(self, layer):
        """Clear all shapes from a layer."""
        for shape in self.layers[layer]:
            shape.surface = None
        self.layers[layer] = []

    def add_shape(self, layer, shape):
        """Add a shape to a layer of the drawing."""
        if shape.surface is None:
            shape.surface = self
        elif shape.surface is not self:
            raise RuntimeError("Shape {shape} is already on a surface: {shape.surface}")
        self.layers[layer].append(shape)
        shape.update()

    def remove_shape(self, layer, shape):
        self.layers[layer].remove(shape)
        shape.update()
        shape.surface = None

    def polys(self, layer, geometry, colors, fill=True, clip=None):
        shape = Polygons(geometry, colors, fill=fill, clip=clip)
        self.add_shape(layer, shape)
        return shape

    def rects(self, layer, geometry, colors, fill=True, clip=None):
        shape = Rectangles(geometry, colors, fill=fill, clip=clip)
        self.add_shape(layer, shape)
        return shape

    def circles(self, layer, geometry, colors, fill=True, clip=None):
        shape = Circles(geometry, colors, fill=fill, clip=clip)
        self.add_shape(layer, shape)
        return shape

    def ellipses(self, layer, geometry, colors, fill=True, clip=None):
        shape = Ellipses(geometry, colors, fill=fill, clip=clip)
        self.add_shape(layer, shape)
        return shape

    def lines(self, layer, geometry, colors, clip=None):
        shape = Lines(geometry, colors, clip=clip)
        self.add_shape(layer, shape)
        return shape

    def vlines(self, layer, geometry, colors, clip=None):
        shape = VLines(geometry, colors, clip=clip)
        self.add_shape(layer, shape)
        return shape

    def hlines(self, layer, geometry, colors, clip=None):
        shape = HLines(geometry, colors, clip=clip)
        self.add_shape(layer, shape)
        return shape

    def points(self, layer, geometry, colors, markers, clip=None):
        from .markers import Points
        points = Points(geometry, colors, markers, clip=clip)
        self.add_shape(layer, points)
        return points

    def markers(self, layer, geometry, colors, markers, clip=None):
        from .markers import Markers
        points = Markers(geometry, colors, markers, clip=clip)
        self.add_shape(layer, points)
        return points

    def text(self, layer, geometry, colors, texts, bold=False, font=None, clip=None):
        from .text import Text
        text = Text(geometry, colors, texts, bold=bold, font=font, clip=clip)
        self.add_shape(layer, text)
        return text

    def bitmaps(self, layer, geometry, bitmaps, colors=None, key=-1, palette=None, clip=None):
        if colors is None:
            from .bitmaps import Bitmaps
            bitmaps = Bitmaps(geometry, bitmaps, key=key, palette=palette, clip=clip)
            self.add_shape(layer, bitmaps)
            return bitmaps
        else:
            from .bitmaps import ColoredBitmaps
            bitmaps = ColoredBitmaps(geometry, colors, bitmaps, clip=clip)
            self.add_shape(layer, bitmaps)
            return bitmaps

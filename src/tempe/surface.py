import asyncio
from array import array

from .raster import Raster
from .shapes import Polygons, Rectangles, Lines, VLines, HLines
from .markers import Markers
from .text import Text


LAYERS = ("BACKGROUND", "UNDERLAY", "IMAGE", "DRAWING", "OVERLAY")


class Surface:
    """A space for drawing shapes."""

    def __init__(self):
        self.layers = {layer: [] for layer in LAYERS}
        self.windows = {}
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
                object.draw(clip.fbuf, clip.x, clip.y)

    def refresh(self, display, working_buffer):
        for rect in self._damage:
            x, y, w, h = rect
            # handle buffer too small
            buffer_rows = (len(working_buffer) // w) - 1
            for start_row in range(0, h, buffer_rows):
                raster_rows = min(buffer_rows, h - start_row)
                raster = Raster(working_buffer, x, y + start_row, w, raster_rows)
                self.draw(raster)
                display.blit(working_buffer, x, y + start_row, w, raster_rows)
        self._damage = []
        self.refresh_needed.clear()

    def damage(self, rect):
        if rect not in self._damage:
            self._damage.append(rect)
            self.refresh_needed.set()

    def clear(self, layer):
        self.layers[layer] = []

    def add_shape(self, layer, shape):
        self.layers[layer].append(shape)

    def polys(self, layer, geometry, colors, clip=None):
        shape = Polygons(self, geometry, colors, clip=clip)
        self.add_shape(layer, shape)
        return shape

    def rects(self, layer, geometry, colors, clip=None):
        shape = Rectangles(self, geometry, colors, clip=clip)
        self.add_shape(layer, shape)
        return shape

    def lines(self, layer, geometry, colors, clip=None):
        shape = Lines(self, geometry, colors, clip=clip)
        self.add_shape(layer, shape)
        return shape

    def vlines(self, layer, geometry, colors, clip=None):
        shape = VLines(self, geometry, colors, clip=clip)
        self.add_shape(layer, shape)
        return shape

    def hlines(self, layer, geometry, colors, clip=None):
        shape = HLines(self, geometry, colors, clip=clip)
        self.add_shape(layer, shape)
        return shape

    def points(self, layer, geometry, colors, markers, clip=None):
        points = Markers(self, geometry, colors, markers, clip=clip)
        self.add_shape(layer, points)
        return points

    def text(self, layer, geometry, colors, texts, bold=False, font=None, clip=None):
        text = Text(self, geometry, colors, texts, bold=bold, font=font, clip=clip)
        self.add_shape(layer, text)
        return text

import asyncio
from array import array

from .raster import Raster



LAYERS = ('BACKGROUND', "UNDERLAY", 'IMAGE', "DRAWING", "OVERLAY")



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

    def refresh(self, display):
        for rect in self._damage:
            x, y, w, h = rect
            buffer = array('H', bytearray(2*w*h))
            raster = Raster(buffer, x, y, w, h)
            self.draw(raster)
            display.blit(buffer, x, y, w, h)
        self._damage = []
        self.refresh_needed.clear()

    def damage(self, rect):
        self._damage.append(rect)
        self.refresh_needed.set()

    def clear(self, layer):
        self.layers[layer] = []

    def add_shape(self, layer, shape):
        self.layers[layer].append(shape)

    def polys(self, layer, geometry, colors, clip=None):
        self.add_shape(layer, FilledPolygons(self, geometry, colors, clip=clip))

    def rects(self, layer, geometry, colors, clip=None):
        self.add_shape(layer, FilledRectangles(self, geometry, colors, clip=clip))

    def lines(self, layer, geometry, colors, clip=None):
        self.add_shape(layer, StrokedLines(self, geometry, colors, clip=clip))

    def vlines(self, layer, geometry, colors, clip=None):
        self.add_shape(layer, StrokedVLines(self, geometry, colors, clip=clip))

    def hlines(self, layer, geometry, colors, clip=None):
        self.add_shape(layer, StrokedHLines(self, geometry, colors, clip=clip))

    def points(self, layer, geometry, colors, markers, clip=None):
        points = Markers(self, geometry, colors, markers, clip=clip)
        self.add_shape(layer)
        return points

    def text(self, layer, geometry, colors, texts, bold=False, font=None, clip=None):
        text = Text(self, geometry, colors, texts, bold=bold, font=font, clip=clip)
        self.add_shape(layer, text)
        return text


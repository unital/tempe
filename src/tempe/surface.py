# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

import asyncio
from array import array
import framebuf

from .data_view import Repeat
from .geometry import Geometry, RowGeometry
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
        self.format = framebuf.RGB565
        self.pixel_size = 2

    def draw(self, raster):
        """Draw into a raster."""
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
        """Refresh the surface on the display."""
        for rect in self._damage:
            x, y, w, h = rect
            # handle buffer too small
            buffer_rows = (len(working_buffer) // (w * self.pixel_size) ) - 1
            for start_row in range(0, h, buffer_rows):
                raster_rows = min(buffer_rows, h - start_row)
                raster = Raster(working_buffer, x, y + start_row, w, raster_rows)
                self.draw(raster)
                display.blit(working_buffer, x, y + start_row, w, raster_rows)
        self._damage = []
        self.refresh_needed.clear()

    def damage(self, rect):
        """Mark a rectangle as needing to be refreshed."""
        if not any(contains(rect, rect2) for rect2 in self._damage):
            self._damage = [
                rect2 for rect2 in self._damage if not contains(rect2, rect)
            ]
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
        """Remove a shape from a layer of the drawing."""
        self.layers[layer].remove(shape)
        shape.update()
        shape.surface = None

    def polygons(self, layer, geometry, colors, fill=True, clip=None):
        geometry = self._check_geometry(geometry, None)
        colors = self._check_colors(colors)
        shape = Polygons(geometry, colors, fill=fill, clip=clip)
        self.add_shape(layer, shape)
        return shape

    def rectangles(self, layer, geometry, colors, fill=True, clip=None):
        geometry = self._check_geometry(geometry, 4)
        colors = self._check_colors(colors)
        shape = Rectangles(geometry, colors, fill=fill, clip=clip)
        self.add_shape(layer, shape)
        return shape

    def circles(self, layer, geometry, colors, fill=True, clip=None):
        geometry = self._check_geometry(geometry, 3)
        colors = self._check_colors(colors)
        shape = Circles(geometry, colors, fill=fill, clip=clip)
        self.add_shape(layer, shape)
        return shape

    def ellipses(self, layer, geometry, colors, fill=True, clip=None):
        geometry = self._check_geometry(geometry, 4)
        colors = self._check_colors(colors)
        shape = Ellipses(geometry, colors, fill=fill, clip=clip)
        self.add_shape(layer, shape)
        return shape

    def lines(self, layer, geometry, colors, clip=None):
        geometry = self._check_geometry(geometry, 4)
        colors = self._check_colors(colors)
        shape = Lines(geometry, colors, clip=clip)
        self.add_shape(layer, shape)
        return shape

    def vlines(self, layer, geometry, colors, clip=None):
        geometry = self._check_geometry(geometry, 3)
        colors = self._check_colors(colors)
        shape = VLines(geometry, colors, clip=clip)
        self.add_shape(layer, shape)
        return shape

    def hlines(self, layer, geometry, colors, clip=None):
        geometry = self._check_geometry(geometry, 3)
        colors = self._check_colors(colors)
        shape = HLines(geometry, colors, clip=clip)
        self.add_shape(layer, shape)
        return shape

    def points(self, layer, geometry, colors, markers, clip=None):
        from .markers import Points

        geometry = self._check_geometry(geometry, 2)
        colors = self._check_colors(colors)
        markers = self._check_markers(markers)
        points = Points(geometry, colors, markers, clip=clip)
        self.add_shape(layer, points)
        return points

    def markers(self, layer, geometry, colors, markers, clip=None):
        from .markers import Markers

        geometry = self._check_geometry(geometry, 3)
        colors = self._check_colors(colors)
        markers = self._check_markers(markers)
        points = Markers(geometry, colors, markers, clip=clip)
        self.add_shape(layer, points)
        return points

    def text(self, layer, geometry, colors, texts, font=None, clip=None):
        from .text import Text

        geometry = self._check_geometry(geometry, 2)
        colors = self._check_colors(colors)
        texts = self._check_texts(texts)
        text = Text(geometry, colors, texts, font=font, clip=clip)
        self.add_shape(layer, text)
        return text

    def bitmaps(
        self, layer, geometry, bitmaps, colors=None, key=-1, palette=None, clip=None
    ):
        geometry = self._check_geometry(geometry, 4)
        bitmaps = self._check_bitmaps(bitmaps)
        if colors is None:
            from .bitmaps import Bitmaps

            bitmaps = Bitmaps(geometry, bitmaps, key=key, palette=palette, clip=clip)
            self.add_shape(layer, bitmaps)
            return bitmaps
        else:
            from .bitmaps import ColoredBitmaps

            colors = self._check_colors(colors)
            bitmaps = ColoredBitmaps(geometry, colors, bitmaps, clip=clip)
            self.add_shape(layer, bitmaps)
            return bitmaps

    def _check_geometry(self, geometry, coords):
        if isinstance(geometry, array) or (
            isinstance(geometry, (tuple, list))
            and all(isinstance(x, int) for x in geometry)
        ):
            geometry = RowGeometry.from_lists([geometry])
        if (
            coords is not None
            and isinstance(geometry, Geometry)
            and geometry.coords is not None
        ):
            if geometry.coords < coords:
                raise ValueError(
                    f"Expected Geometry with at least {coords} coordinates, but got {geometry.coords}"
                )
        return geometry

    def _check_colors(self, colors):
        if isinstance(colors, str):
            from .colors import from_str

            return Repeat(from_str(colors))
        elif isinstance(colors, int):
            return Repeat(colors)
        else:
            return colors

    def _check_markers(self, markers):
        if isinstance(markers, (int, str, framebuf.FrameBuffer)):
            return Repeat(markers)
        else:
            return markers

    def _check_texts(self, texts):
        if isinstance(texts, str):
            return Repeat(texts)
        else:
            return texts

    def _check_bitmaps(self, bitmaps):
        if isinstance(bitmaps, framebuf.FrameBuffer):
            return Repeat(bitmaps)
        else:
            return bitmaps

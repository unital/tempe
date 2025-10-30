# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

from array import array
from math import sqrt

from .shapes import SizedGeometry
from .util import line_points, intersect_poly_rect


class WideLines(SizedGeometry):
    """Render multiple colored line segments with variable width.

    Geometry should produce x0, y0, x1, y1, width arrays.
    """

    def __init__(self, geometry, colors, sizes, *, round=True, surface=None, clip=None):
        super().__init__(geometry, colors, sizes, surface=surface, clip=clip)
        self.round = round

    def draw_raster(self, raster):
        buffer = raster.fbuf
        x = raster.x
        y = raster.y
        w = raster.w
        h = raster.h
        vertices = array("h", bytearray(16))
        should_round = self.round
        for geometry, color, lw in self:
            if intersect_poly_rect(geometry[:4], 4, x - lw, y - lw, w + 2 * lw, h + 2 * lw):
                x0 = geometry[0]
                y0 = geometry[1]
                x1 = geometry[2]
                y1 = geometry[3]
                if lw < 2:
                    buffer.line(x0 - x, y0 - y, x1 - x, y1 - y, color)
                else:
                    d = 2 * int(sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2))
                    line_points(x0, y0, x1, y1, lw, d, vertices)
                    buffer.poly(-x, -y, vertices, color, True)
                    if should_round:
                        r = lw // 2
                        buffer.ellipse(x0 - x, y0 - y, r, r, color, True)
                        buffer.ellipse(x1 - x, y1 - y, r, r, color, True)

    def _get_bounds(self):
        max_x = -0x7FFF
        min_x = 0x7FFF
        max_y = -0x7FFF
        min_y = 0x7FFF
        for geometry, w in zip(self.geometry, self.sizes):
            max_x = max(max_x, geometry[0] + w, geometry[2] + w)
            min_x = min(min_x, geometry[0] - w, geometry[2] - w)
            max_y = max(max_y, geometry[1] + w, geometry[3] + w)
            min_y = min(min_y, geometry[1] - w, geometry[3] - w)

        return (min_x, min_y, max_x - min_x, max_y - min_y)


class WidePolyLines(SizedGeometry):
    """Render multiple colored polylines with variable width.
    """

    def draw_raster(self, raster):
        buffer = raster.fbuf
        x = raster.x
        y = raster.y
        w = raster.w
        h = raster.h
        vertices = array("h", bytearray(16))
        for lines, color, lw in self:
            if intersect_poly_rect(lines, len(lines), x - lw, y - lw, w + 2 * lw, h + 2 * lw):
                for i in range(0, len(lines) - 2, 2):
                    x0 = lines[i]
                    y0 = lines[i + 1]
                    x1 = lines[i + 2]
                    y1 = lines[i + 3]
                    if lw < 2:
                        buffer.line(x0 - x, y0 - y, x1 - x, y1 - y, color)
                    else:
                        d = 2 * int(sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2))
                        line_points(x0, y0, x1, y1, lw, d, vertices)
                        buffer.poly(-x, -y, vertices, color, True)
                if lw >= 2:
                    r = lw // 2
                    for i in range(0, len(lines), 2):
                        x0 = lines[i]
                        y0 = lines[i + 1]
                        buffer.ellipse(x0 - x, y0 - y, r, r, color, True)

    def _get_bounds(self):
        max_x = -0x7FFF
        min_x = 0x7FFF
        max_y = -0x7FFF
        min_y = 0x7FFF
        for lines, w in zip(self.geometry, self.sizes):
            for i in range(0, len(lines), 2):
                max_x = max(max_x, lines[i] + w)
                min_x = min(min_x, lines[i] - w)
                max_y = max(max_y, lines[i + 1] + w)
                min_y = min(min_y, lines[i + 1] - w)

        return (min_x, min_y, max_x - min_x, max_y - min_y)

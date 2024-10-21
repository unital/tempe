from array import array
from math import sqrt
import micropython

from .shapes import ColoredGeometry


class WideLines(ColoredGeometry):
    """Render multiple colored line segments with variable width.

    Geometry should produce x0, y0, x1, y1, width arrays.
    """

    def __init__(self, geometry, colors, *, round=True, surface=None, clip=None):
        super().__init__(geometry, colors, surface=surface, clip=clip)
        self.round = round

    def draw(self, buffer, x=0, y=0):
        vertices = array('h', bytearray(16))
        should_round = self.round
        for geometry, color in self:
            x0 = geometry[0]
            y0 = geometry[1]
            x1 = geometry[2]
            y1 = geometry[3]
            w = geometry[4]
            if w < 2:
                buffer.line(x0 - x, y0 - y, x1 - x, y1 - y, color)
            else:
                d = 2 * int(sqrt((x1 - x0)**2 + (y1 - y0)**2))
                line_points(x0, y0, x1, y1, w, d, vertices)
                buffer.poly(-x, -y, vertices, color, True)
                if should_round:
                    r = w // 2
                    buffer.ellipse(x0 - x, y0 - y, r, r, color, True)
                    buffer.ellipse(x1 - x, y1 - y, r, r, color, True)

    def _bounds(self):
        max_x = -0x7fff
        min_x = 0x7fff
        max_y = -0x7fff
        min_y = 0x7fff
        for geometry in self.geometry:
            max_x = max(max_x, geometry[0] + geometry[4], geometry[2] + geometry[4])
            min_x = min(min_x, geometry[0] - geometry[4], geometry[2] - geometry[4])
            max_y = max(max_y, geometry[1] + geometry[4], geometry[3] + geometry[4])
            min_y = min(min_y, geometry[1] - geometry[4], geometry[3] - geometry[4])

        return (min_x, min_y, max_x - min_x, max_y - min_y)



class WidePolyLines(ColoredGeometry):
    """Render multiple colored polylines with variable width.

    Geometry should produce array of [x0, y0, x1, y1, ...] and width.
    """

    def draw(self, buffer, x=0, y=0):
        vertices = array('h', bytearray(16))
        for geometry, color in self:
            lines, w = geometry
            for i in range(0, len(lines) - 2, 2):
                x0 = lines[i]
                y0 = lines[i+1]
                x1 = lines[i+2]
                y1 = lines[i+3]
                if w < 2:
                    buffer.line(x0 - x, y0 - y, x1 - x, y1 - y, color)
                else:
                    d = 2 * int(sqrt((x1 - x0)**2 + (y1 - y0)**2))
                    line_points(x0, y0, x1, y1, w, d, vertices)
                    buffer.poly(-x, -y, vertices, color, True)
            if w >= 2:
                r = w // 2
                for i in range(0, len(lines), 2):
                    x0 = lines[i]
                    y0 = lines[i+1]
                    buffer.ellipse(x0 - x, y0 - y, r, r, color, True)

    def _bounds(self):
        max_x = -0x7fff
        min_x = 0x7fff
        max_y = -0x7fff
        min_y = 0x7fff
        for geometry in self.geometry:
            lines, w = geometry
            for i in range(0, len(lines), 2):
                max_x = max(max_x, lines[i] + w)
                min_x = min(min_x, lines[i] - w)
                max_y = max(max_y, lines[i+1] + w)
                min_y = min(min_y, lines[i+1] - w)

        return (min_x, min_y, max_x - min_x, max_y - min_y)


@micropython.viper
def line_points(x0: int, y0: int, x1: int, y1: int, w: int, d: int, vertices: ptr16):
    dx: int = x1 - x0
    dy: int = y1 - y0

    # stuff to handle inter division always round down, when we really
    # want away from 0
    if dx == 0:
        mx = -((w + 1) // 2)
    else:
        if dy > 0:
            mx = -w * dy // d
        else:
            mx = -(w * dy // d)
    if dy == 0:
        my = (w + 1) // 2
    else:
        if dx > 0:
            my = -(-w * dx // d)
        else:
            my = w * dx // d

    vertices[0] = x0 + mx
    vertices[1] = y0 + my
    vertices[2] = x1 + mx
    vertices[3] = y1 + my
    vertices[4] = x1 - mx
    vertices[5] = y1 - my
    vertices[6] = x0 - mx
    vertices[7] = y0 - my


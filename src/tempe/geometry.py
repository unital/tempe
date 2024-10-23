
from array import array
from math import pi, sin, cos

from .data_view import DataView

POINT = "point"
CIRCLE = "circle"
RECTANGLE = "rectangle"
POLY = "poly"


class Geometry(DataView):
    """Efficient storage of geometric information."""

    def __init__(self, geometry):
        self.geometry = geometry

    def __iter__(self):
        raise NotImplementedError()

    def __len__(self):
        raise NotImplementedError()


class RowGeometry(Geometry):
    """Geometry where coordinates are provided as ragged rows."""

    @classmethod
    def from_lists(cls, rows):
        return cls([array("h", coord) for coord in rows])

    def __iter__(self):
        yield from self.geometry

    def __len__(self):
        return len(self.geometry)


class ColumnGeometry(Geometry):
    """Geometry where coordinates are provided as ragged columns"""

    def __iter__(self):
        for coords in zip(*self.geometry):
            yield array("h", coords)

    def __len__(self):
        lengths = [len(coord) for coord in self.geometry if len(coord) is not None]
        if lengths:
            return max(lengths)
        else:
            return None


class StripGeometry(Geometry):
    """Geometry generating connected strip of n-gons from vertices.

    Iterator provides vertex point buffers of the form [x0, y0, x1, y1, ...].
    """

    def __init__(self, geometry, n_groups=2, step=1, n_coords=2):
        super().__init__(geometry)
        self.n_groups = n_groups
        self.step = step
        self.n_coords = n_coords

    def __iter__(self):
        size = self.n_groups * self.n_coords
        start = 0
        buf = array("h", bytearray(2 * size))
        for i in range(len(self)):
            buf[:] = self.geometry[start : start + size]
            start += self.step * self.n_coords
            yield buf

    def __len__(self):
        return ((len(self.geometry) // self.n_coords) - self.n_groups) // self.step + 1


class PointsToLines(Geometry):
    """Turn a generator of x, y values into a generator of (x0, y0, x1, y1)."""

    def __iter__(self):
        buf = array("h", bytearray(8))
        for i, point in enumerate(self.geometry):
            buf[:2] = buf[2:]
            buf[2:] = point
            if i != 0:
                yield buf

    def __len__(self):
        n = len(self.geometry)
        if n is None:
            return None
        else:
            return n - 1



class Extend(Geometry):

    def __iter__(self):
        for coords in zip(*self.geometry):
            buf = array('h', bytearray(2*sum(len(coord) for coord in coords)))
            i = 0
            for coord in coords:
                buf[i:i + len(coord)] = coord
                i += len(coord)
            yield buf

    def __len__(self):
        lengths = [len(coord) for coord in self.geometry if len(coord) is not None]
        if lengths:
            return max(lengths)
        else:
            return None


class ProductGeometry(Geometry):
    """Cartesian product of 2 geometries."""

    def __iter__(self):
        geom_1, geom_2 = self.geometry
        for x in geom_1:
            sx = len(x)
            for y in geom_2:
                sy = len(y)
                buf = array('h', bytearray(2*(sx + sy)))
                buf[:sx] = x
                buf[sx:] = y
                yield buf

    def __len__(self):
        if any(len(coord) is None for coord in self.geometry):
            return None
        else:
            total = 1
            for coord in self.geometry:
                total *= len(coord)
            return total


class Select(Geometry):
    """Select coordinates from another geometry."""

    def __init__(self, geometry, selection):
        super().__init__(geometry)
        self.selection = selection

    def __iter__(self):
        selection = self.selection
        buffer = array('h', len(2*len(selection)))
        for geometry in self.geometry:
            for i, j in enumerate(selection):
                buffer[i] = geometry[j]
            yield buffer

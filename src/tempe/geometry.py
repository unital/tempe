from .dataview import DataView

from array import array

POINT = 'point'
CIRCLE = 'circle'
RECTANGLE = 'rectangle'
POLY = 'poly'



class Geometry(DataView):
    """Efficient storage of geometric information."""

    def __init__(self, geometry, coords=POINT):
        self.geometry = geometry
        self.coords = coords

    def __iter__(self):
        raise NotImplementedError()

    def __len__(self):
        raise NotImplementedError()


class RowGeometry(Geometry):
    """Geometry where coordinates are provided as ragged rows."""

    @classmethod
    def from_lists(cls, rows):
        return cls([array('h', coord) for coord in rows])

    def __iter__(self):
        yield from self.geometry

    def __len__(self):
        return len(self.geometry)


class ColumnGeometry(Geometry):
    """Geometry where coordinates are provided as ragged columns"""

    def __iter__(self):
        buf = array('h', bytearray(2*len(self.geometry)))
        for coords in zip(*self.geometry):
            buf[:] = coords
            yield buf

    def __len__(self):
        return max(len(coord) for coord in self.geometry)


class GeometryStrip(Geometry):
    """Geometry generating connected strip of n-gons from vertices.

    Iterator provides vertex point buffers of the form [x0, y0, x1, y1, ...].
    """

    def __init__(self, geometry, n_vertices=2):
        super().__init__(geometry)

    def __iter__(self):
        size = self.n_vertices * self.n_coords
        start = 0
        buf = array('h', bytearray(2*size))
        for i in range(len(self)):
            start += self.step * self.n_coords
            buf[:] = self.geometry[start:start + size]
            yield buf

    def __len__(self):
        return ((len(self.geometry) // self.n_coords) - self.n_vertices) // self.step


class LineStrip(GeometryStrip):
    n_vertices = 2


class TriangleStrip(GeometryStrip):
    n_vertices = 3


class QuadStrip(GeometryStrip):
    n_vertices = 3
    step = 2


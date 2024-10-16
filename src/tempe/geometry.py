from .data_view import DataView

from array import array

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
        return max(len(coord) for coord in self.geometry)


class StripGeometry(Geometry):
    """Geometry generating connected strip of n-gons from vertices.

    Iterator provides vertex point buffers of the form [x0, y0, x1, y1, ...].
    """

    #: Grabbing pairs of coordinates for vertices.
    n_coords = 2

    def __init__(self, geometry, n_vertices=2, step=1):
        super().__init__(geometry)
        self.n_vertices = n_vertices
        self.step = step

    def __iter__(self):
        size = self.n_vertices * self.n_coords
        start = 0
        buf = array("h", bytearray(2 * size))
        for i in range(len(self)):
            start += self.step * self.n_coords
            buf[:] = self.geometry[start : start + size]
            yield buf

    def __len__(self):
        return ((len(self.geometry) // self.n_coords) - self.n_vertices) // self.step

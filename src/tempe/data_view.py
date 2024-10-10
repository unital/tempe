"""The DataView class and its subclasses."""

class DataView:
    """The base dataview class"""

    @classmethod
    def create(cls, data):
        """Create an appropriate dataclass instance from an object."""
        if isinstance(data, cls):
            return data

        try:
            iter(data)
            return cls(data)
        except TypeError:
            return Repeat(data)

    def __init__(self, data):
        self.data = data

    def __iter__(self):
        yield from self.data

    def __getitem__(self, index):
        return self.data[index]

    def __add__(self, other):
        from .data_view_math import Add
        try:
            iter(other)
            return Add(self, other)
        except TypeError:
            return Add(self, Repeat(other))

    def __radd__(self, other):
        from .data_view_math import Add
        try:
            iter(other)
            return Add(other, self)
        except TypeError:
            return Add(Repeat(other), self)

    def __sub__(self, other):
        from .data_view_math import Subtract
        try:
            iter(other)
            return Subtract(self, other)
        except TypeError:
            return Subtract(self, Repeat(other))

    def __rsub__(self, other):
        from .data_view_math import Subtract
        try:
            iter(other)
            return Subtract(other, self)
        except TypeError:
            return Subtract(Repeat(other), self)

    def __mul__(self, other):
        from .data_view_math import Multiply
        try:
            iter(other)
            return Multiply(self, other)
        except TypeError:
            return Multiply(self, Repeat(other))

    def __rmul__(self, other):
        from .data_view_math import Multiply
        try:
            iter(other)
            return Multiply(self, other)
        except TypeError:
            return Multiply(Repeat(other), self)

    def __floordiv__(self, other):
        from .data_view_math import FloorDivide
        try:
            iter(other)
            return FloorDivide(self, other)
        except TypeError:
            return FloorDivide(self, Repeat(other))

    def __rfloordiv__(self, other):
        from .data_view_math import FloorDivide
        try:
            iter(other)
            return FloorDivide(other, self)
        except TypeError:
            return FloorDivide(Repeat(other), self)

    def __truediv__(self, other):
        from .data_view_math import Divide
        try:
            iter(other)
            return Divide(self, other)
        except TypeError:
            return Divide(self, Repeat(other))

    def __rtruediv__(self, other):
        from .data_view_math import Divide
        try:
            iter(other)
            return Divide(other, self)
        except TypeError:
            return Divide(Repeat(other), self)

    def __neg__(self):
        from .data_view_math import Neg
        return Neg(self)

    def __pos__(self):
        from .data_view_math import Pos
        return Pos(self)

    def __abs__(self):
        from .data_view_math import Abs
        return Abs(self)

    def __invert__(self):
        from .data_view_math import Invert
        return Invert(self)


class Cycle(DataView):
    """A Dataview which extends an iterable by repeating cyclically."""

    def __iter__(self):
        while True:
            yield from self.data

    def __getitem__(self, index):
        if isinstance(index, slice):
            return [
                self.data[index % len(self.data)]
                for index in range(slice.start, slice.stop, slice,step)
            ]
        else:
            return self.data[index % len(self.data)]


class ReflectedCycle(DataView):
    """A Dataview which extends an iterable by repeating in reverse."""

    def __iter__(self):
        while True:
            yield from self.data
            for value in self.data[::-1]:
                yield value


class Last(DataView):
    """A Dataview which extends an iterable by repeating the last value."""

    def __iter__(self):
        for value in self.data:
            yield self.data
        while True:
            yield value


class Repeat(DataView):
    """A Dataview broadcasts a scalar as an infinitely repeating ."""

    def __iter__(self):
        while True:
            yield self.data

    def __getitem__(self, index):
        if isinstance(index, slice):
            return [self.data] * ((self.stop - self.start) // self.step)
        else:
            return self.data

    def __add__(self, other):
        if isinstance(other, Repeat):
            return Repeat(self.data + other.data)
        else:
            return super().__add__(other)

    def __sub__(self, other):
        if isinstance(other, Repeat):
            return Repeat(self.data - other.data)
        else:
            return super().__sub__(other)

    def __mul__(self, other):
        if isinstance(other, Repeat):
            return Repeat(self.data * other.data)
        else:
            return super().__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, Repeat):
            return Repeat(self.data / other.data)
        else:
            return super().__truediv__(other)

    def __floordiv__(self, other):
        if isinstance(other, Repeat):
            return Repeat(self.data // other.data)
        else:
            return super().__floordiv__(other)

    def __neg__(self):
        return Repeat(-self.data)

    def __pos__(self):
        return Repeat(+self.data)

    def __abs__(self):
        return Repeat(abs(self.data))

    def __invert__(self):
        return Repeat(~self.data)


class Count(DataView):

    def __init__(self, start=0, step=1):
        self.start = 0
        self.step = 1

    def __iter__(self):
        i = self.start
        while True:
            yield i
            i += 1

    def __getitem__(self, index):
        if isinstance(index, slice):
            return [
                self.start + self.step * index
                for index in range(slice.start, slice.stop, slice,step)
            ]
        else:
            return self.start + self.step * index


class Range(DataView):

    def __init__(self, start, stop=None, step=1):
        self.start = start
        self.stop = stop
        self.step = step

    def __iter__(self):
        yield from range(self.start, self.stop, self.step)

    def __getitem__(self, index):
        if isinstance(index, slice):
            return [
                self.start + self.step * self.index
                for index in range(slice.start, slice.stop, slice,step)
            ]
        else:
            return self.start + self.step * self.index


class Slice(DataView):

    def __init__(self, data, start, stop=None, step=1):
        super().__init__(data)
        if stop is None:
            stop = start
            start = 0
        self.start = start
        self.stop = stop
        self.step = step

    def __iter__(self):
        i = 0
        j = None
        start = self.start
        step = self.step
        stop = self.stop
        for value in self.data:
            if start <= i < stop:
                if j is None:
                    j = 0
                if j % step == 0:
                    yield value
                j += 1
            elif i > stop:
                break
            i += 1


class Interpolated(DataView):

    def __init__(self, data, n):
        super().__init__(data)
        self.n = n

    def __iter__(self):
        for index in range(n):
            yield self.data[index * (len(self.data) - 1) // (n - 1)]

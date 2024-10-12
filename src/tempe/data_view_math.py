"""The DataView class and its subclasses."""


""" Classes that implement numerical operations on DataViews.

These classes are largely an internal implementation detail.
"""

from .data_view import DataView


class UnaryOp(DataView):

    def __iter__(self):
        raise NotImplementedError()

    def __getitem__(self, index):
        raise NotImplementedError()


class BinOp(DataView):

    def __init__(self, data1, data2):
        self.data1 = data1
        self.data2 = data2

    def __iter__(self):
        raise NotImplementedError()

    def __getitem__(self, index):
        raise NotImplementedError()


class Neg(UnaryOp):

    def __iter__(self):
        for x in self.data:
            yield -x

    def __getitem__(self, index):
        return -self.data[index]


class Pos(UnaryOp):

    def __iter__(self):
        for x in self.data:
            yield +x

    def __getitem__(self, index):
        return +self.data[index]


class Abs(UnaryOp):

    def __iter__(self):
        for x in self.data:
            yield abs(x)

    def __getitem__(self, index):
        return abs(self.data[index])


class Invert(UnaryOp):

    def __iter__(self):
        for x in self.data:
            yield ~x

    def __getitem__(self, index):
        return ~self.data[index]

class Add(BinOp):

    def __iter__(self):
        for x, y in zip(self.data1, self.data2):
            yield x + y

    def __getitem__(self, index):
        return self.data1[index] + self.data2[index]


class BinOp(DataView):

    def __init__(self, data1, data2):
        self.data1 = data1
        self.data2 = data2

    def __iter__(self):
        raise NotImplementedError()


class Add(BinOp):

    def __iter__(self):
        for x, y in zip(self.data1, self.data2):
            yield x + y

    def __getitem__(self, index):
        return self.data1[index] + self.data2[index]


class Subtract(BinOp):

    def __iter__(self):
        for x, y in zip(self.data1, self.data2):
            yield x - y

    def __getitem__(self, index):
        return self.data1[index] - self.data2[index]


class Multiply(BinOp):

    def __iter__(self):
        for x, y in zip(self.data1, self.data2):
            yield x * y

    def __getitem__(self, index):
        return self.data1[index] * self.data2[index]


class Divide(BinOp):

    def __iter__(self):
        for x, y in zip(self.data1, self.data2):
            yield x / y

    def __getitem__(self, index):
        return self.data1[index] / self.data2[index]


class FloorDivide(BinOp):

    def __iter__(self):
        for x, y in zip(self.data1, self.data2):
            yield x // y

    def __getitem__(self, index):
        return self.data1[index] // self.data2[index]


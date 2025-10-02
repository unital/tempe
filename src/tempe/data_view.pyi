# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

"""The DataView class and its subclasses.

The following informal types are used in this module:

.. py:type:: DataType

   This is the underlying data-type of the data being viewed; it is the
   type that will be produced when the DataView is iterated.
"""

from collections.abc import Sequence, Iterator, Iterable
from typing import Any, Generic, TypeVar

class DataView[DataType]:
    """The base dataview class"""

    @classmethod
    def create(cls, data: Any) -> DataView:
        """Create an appropriate DataView instance from an object."""

    def __init__(self, data: Iterable[DataType]): ...
    def __len__(self) -> int | None: ...
    def __iter__(self) -> Iterator[DataType]: ...
    def __getitem__(self, index: int | slice) -> DataType | DataView[DataType]: ...
    def __add__(self, other: DataType | Iterable[DataType]) -> DataView[DataType]: ...
    def __radd__(self, other: DataType | Iterable[DataType]) -> DataView[DataType]: ...
    def __sub__(self, other: DataType | Iterable[DataType]) -> DataView[DataType]: ...
    def __rsub__(self, other: DataType | Iterable[DataType]) -> DataView[DataType]: ...
    def __mul__(self, other: DataType | Iterable[DataType]) -> DataView[DataType]: ...
    def __rmul__(self, other: DataType | Iterable[DataType]) -> DataView[DataType]: ...
    def __floordiv__(
        self, other: DataType | Iterable[DataType]
    ) -> DataView[DataType]: ...
    def __rfloordiv__(
        self, other: DataType | Iterable[DataType]
    ) -> DataView[DataType]: ...
    def __truediv__(
        self, other: DataType | Iterable[DataType]
    ) -> DataView[DataType]: ...
    def __rtruediv__(
        self, other: DataType | Iterable[DataType]
    ) -> DataView[DataType]: ...
    def __neg__(self) -> DataView[DataType]: ...
    def __pos__(self) -> DataView[DataType]: ...
    def __abs__(self) -> DataView[DataType]: ...
    def __invert__(self) -> DataView[DataType]: ...

class Cycle[DataType](DataView[DataType]):
    """A DataView which extends an iterable by repeating cyclically."""

    def __len__(self) -> None: ...

class ReflectedCycle[DataType](DataView[DataType]):
    """A DataView which extends an iterable by repeating in reverse."""

    def __len__(self) -> None: ...

class RepeatLast[DataType](DataView[DataType]):
    """A DataView which extends an iterable by repeating the last value."""

    def __len__(self) -> None: ...

class Repeat[DataType](DataView[DataType]):
    """A DataView broadcasts a scalar as an infinitely repeating value."""

    def __init__(self, data: DataType): ...
    def __len__(self) -> None: ...

class Count(DataView[int]):
    """DataView that counts indefinitely from a start by a step."""

    def __init__(self, start: int = 0, step: int = 1): ...
    def __len__(self) -> None: ...

class Range(DataView[int]):
    """DataView that efficiently represents a range."""

    def __init__(self, start: int, stop: int | None = None, step: int = 1): ...
    def __len__(self) -> int: ...

class Slice[DataType](DataView[DataType]):
    """Take a slice of another DataView"""

    def __init__(
        self,
        data: Iterable[DataType],
        start: int,
        stop: int | None = None,
        step: int = 1,
    ): ...

class Interpolated[DataType](DataView[DataType]):
    """Produce n evenly spaced elements from the data source."""

    def __init__(self, data: Sequence[DataType], n: int): ...

__all__ = [
    "DataView",
    "Cycle",
    "ReflectedCycle",
    "RepeatLast",
    "Repeat",
    "Count",
    "Range",
    "Slice",
    "Interpolated",
]

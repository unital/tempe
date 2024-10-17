# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

"""Base Display class and FileDisplay class.

This module defines the Display abstract base class as well as a concrete
implementation that renders to a binary file.

Users of specific hardware may need to define their own subclasses that
can send updates to the underlying device.
"""

from array import array
from typing import Self


class Display:
    """Abstract base class for Displays"""

    def blit(self, buffer: array, x: int, y: int, w: int, h: int):
        """Render the buffer to the given rectangle of the Display.

        The array buffer must match the width and height, and the edges
        of the bounding rectangle should lie within the Display.

        Concrete subclasses must implement this method, either to
        directly render partial updates to the underlying device, or to
        render to a complete framebuffer which is then rendered.
        """
        raise NotImplementedError

    def clear(self) -> None:
        """Clear the display, setting all pixels to 0."""
        raise NotImplementedError


class FileDisplay(Display):
    """Display that renders raw RGB565 data to a file.

    FileDisplay can be used as a context manager to open and close the
    underlying file object automatically.
    """

    def __init__(self, name: str, size: tuple[int, int] = (320, 240)): ...

    def __enter__(self) -> Self: ...

    def __exit__(self, *args) -> bool: ...


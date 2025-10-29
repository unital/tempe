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
import framebuf
from typing import Self, Protocol, runtime_checkable

@runtime_checkable
class Display(Protocol):
    """Abstract base class for Displays"""

    size: tuple[int, int]

    def blit(self, buffer: array, x: int, y: int, w: int, h: int):
        """Render the buffer to the given rectangle of the Display.

        The array buffer must match the width and height, and the edges
        of the bounding rectangle should lie within the Display.

        Concrete subclasses must implement this method, either to
        directly render partial updates to the underlying device, or to
        render to a complete framebuffer which is then rendered.

        Parameters
        ----------
        buffer : array or other buffer
            An array of pixel data in RGB565 format.
        x : int
            The x-coordinate of the rectangle to render into.
        y : int
            The y-coordinate of the rectangle to render into.
        w : int
            The width of the rectangle to render into.
        h : int
            The height of the rectangle to render into.
        """

    def clear(self) -> None:
        """Clear the display, setting all pixels to 0."""


class FrameBufferDisplay(Display):
    """Display that renders into a FrameBuffer.

    The given size should be consistent with the width and height of the
    FrameBuffer.

    If the FrameBuffer is not RGB565 format, a palette object
    compatible with `FrameBuffer.blit()` should be provided which maps all
    RGB565 pixel values to pixel values of the target array. Note that this
    may be impractically large in most cases (eg. even a 1-bit image needs an
    8 kilobyte palette).
    """

    fbuf: framebuf.FrameBuffer
    palette: framebuf.FrameBuffer | None = None

    def __init__(
            self,
            fbuf: framebuf.FrameBuffer,
            size: tuple[int, int],
            palette: framebuf.FrameBuffer | None = None,
        ) -> None: ...

    def blit(self, buffer: framebuf.FrameBuffer | array, x: int, y: int, w: int, h: int):
        """Render the buffer to the given rectangle of the Display.

        This uses the FrameBuffer.blit method, so buffer can either be a
        FrameBuffer object (in which case the width and height should
        match the w and h parameters) or a buffer which is consistent with the
        given w and h and RGB565 pixels.

        Parameters
        ----------
        buffer : array or other buffer
            An array of pixel data in RGB565 format.
        x : int
            The x-coordinate of the rectangle to render into.
        y : int
            The y-coordinate of the rectangle to render into.
        w : int
            The width of the rectangle to render into.
        h : int
            The height of the rectangle to render into.
        """


class FileDisplay(Display):
    """Display that renders raw RGB565 data to a file.

    FileDisplay can be used as a context manager to open and close the
    underlying file object automatically.
    """

    def clear(self) -> None: ...
    def __init__(self, name: str, size: tuple[int, int] = (320, 240)): ...
    def __enter__(self) -> Self: ...
    def __exit__(self, *args) -> bool: ...

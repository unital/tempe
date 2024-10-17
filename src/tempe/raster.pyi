"""This module defined the Raster class.

This is an internal class which handles the logic of providing a
framebuffer for a rectangular region of a surface, as well as clipping
operations.
"""

from array import array
import framebuf

from typing import Self

class Raster:
    """A rectangular buffer that can be drawn on by a surface.

    This class is used internally, so most end-users do not need to create
    them.

    Attributes
    ----------
    fbuf : frambuf.FrameBuffer
        The framebuffer built on the buffer.
    x : int
        The x-offset of the framebuffer relative to the Surface.
    y : int
        The y-offset of the framebuffer relative to the Surface.
    """

    def __init__(
            self,
            buf: array,
            x: int,
            y: int,
            w: int,
            h: int,
            stride: int | None = None,
            offset: int = 0,
        ): ...

    @classmethod
    def from_rect(cls, x: int, y: int, w: int, h: int) -> Self:
        """Create a Raster with a new buffer for the given rectangle."""

    def clip(self, x: int, y: int, w: int, h: int) -> Self | None:
        """Create a Raster sharing the same buffer, clipped to the rectangle.

        If there is no intersection between the raster and the rectangle, then
        None is returned.
        """

__all__ = ["Raster"]

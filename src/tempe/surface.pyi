"""Drawing surface class and related objects.

This module defines the Surface class and related constants for using
it.

Attributes
----------

Layers : tuple[str, ...]
    The default set of layers used by Surfaces, in order from back to front.
    The default value is ``("BACKGROUND", "UNDERLAY", "IMAGE", "DRAWING", "OVERLAY")``

"""
import asyncio
from array import array
from collections.abc import Iterable
from typing import Any

from .display import Display
from .font import AbstractFont
from .geometry import Geometry
from .raster import Raster
from .shapes import Shape, Polygons, Rectangles, Lines, VLines, HLines, rectangle
from .util import contains

#: The default set of layers used by Surfaces, in order from back to front.
LAYERS = ("BACKGROUND", "UNDERLAY", "IMAGE", "DRAWING", "OVERLAY")

class Surface:
    """A layered space for drawing shapes.

    This is the fundamental class where all Tempe drawing takes place.
    A Surface has a number of layers, each of which holds zero or more
    Shapes.  The Surface draws shapes on order from the first layer to
    the last, with each shape in a layer being drawn in the order it was
    added to the Surface.

    Shapes which have changed update themselves and add the areas that
    need re-drawing to the list of damaged regions.

    Actual drawing is carried out by the ``draw`` method, but most users of
    Surface objects should call ``refresh``, which handles managing damaged
    regions and clipping to minimise the actual work that's needed.

    Attributes
    ----------
    refresh_needed : asyncio.Event
        An Event that is set when the surface is damaged, and cleared
        at the end of a ``refresh`` call.
    """

    def __init__(self): ...

    def refresh(self, display: Display, working_buffer: array[int]) -> None:
        """Refresh the surface's appearance in the display.

        Calling this updates all damaged regions on the display device.
        The caller should supply a chunk of memory as an array of unsigned
        16-bit integers that is used as a scratch space for partial
        rendering.  The larger this memory is (up to the size of the
        display), the faster the display will be updated.

        Parameters
        ----------
        display : Display
            The actual physical display that the surface will be drawn on.
        working_buffer : array[int]
            An empty array of unsigned 16-bit ints (ie. ``array('H', ...)``)
            that the Surface will use as memory for temporary drawing buffers.
        """

    def add_shape(self, layer: Any, shape: Shape) -> None:
        """Add a shape to a layer of the drawing."""

    def remove_shape(self, layer: Any, shape: Shape) -> None: ...

    def clear(self, layer: Any) -> None:
        """Clear all shapes from a layer."""

    def damage(self, rect: rectangle) -> None:
        """Add a rectangle to the regions which need updating.

        This also sets the ``refresh_needed`` event.

        This should be called by Shape classes when they are changed.

        Parameters
        ----------
        rect : tempe.shapes.rectangle
            A rectangle in the form of a tuple (x, y, w, h) which contains
            a region where the shapes being displayed have changed.
        """

    def draw(self, raster: Raster) -> None:
        """Draw the contents of the surface onto the Raster.

        Most end-user code should call ``refresh`` instead.

        Parameters
        ----------
        raster : Raster
            The Raster object that the shapes will be drawn on.
        """

    def polys(
        self,
        layer: Any,
        geometry: Geometry[array],
        colors: Iterable[int],
        clip: tuple[int, int, int, int] | None = None,
    ) -> Polygons: ...

    def rects(
        self,
        layer: Any,
        geometry: Geometry[tuple[int, int, int, int]],
        colors: Iterable[int],
        clip: tuple[int, int, int, int] | None = None,
    ) -> Rectangles: ...

    def lines(
        self,
        layer: Any,
        geometry: Geometry[tuple[int, int, int, int]],
        colors: Iterable[int],
        clip: tuple[int, int, int, int] | None = None,
    ) -> Lines: ...

    def vlines(
        self,
        layer: Any,
        geometry: Geometry[tuple[int, int, int, int]],
        colors: Iterable[int],
        clip: tuple[int, int, int, int] | None = None,
    ) -> VLines: ...

    def hlines(
        self,
        layer: Any,
        geometry: Geometry[tuple[int, int, int, int]],
        colors: Iterable[int],
        clip: tuple[int, int, int, int] | None = None,
    ) -> HLines: ...

    def points(
        self,
        layer: Any,
        geometry: Geometry[tuple[int, int, int, int]],
        colors: Iterable[int],
        markers: Iterable[Any],
        clip: tuple[int, int, int, int] | None = None,
    ) -> "tempe.markers.Markers": ...

    def text(
        self,
        layer: Any,
        geometry: Geometry[tuple[int, int, int, int]],
        colors: Iterable[int],
        text: Iterable[str],
        bold: bool = False,
        font: AbstractFont | None = None,
        clip: tuple[int, int, int, int] | None = None,
    ) -> "tempe.text.Text": ...

__all__ = ["Surface"]

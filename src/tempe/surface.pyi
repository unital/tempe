# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

"""Drawing surface class and related objects.

This module defines the Surface class and related constants for using
it.

Attributes
----------

Layers : tuple[str, ...]
    The default set of layers used by Surfaces, in order from back to front.
    The default value is ``("BACKGROUND", "UNDERLAY", "IMAGE", "DRAWING", "OVERLAY")``

BACKGROUND : str
UNDERLAY : str
IMAGE : str
DRAWING : str
OVERLAY : str
    Constants holding the default values for the surface layers as strings.

"""

import asyncio
from array import array
import framebuf
from collections.abc import Iterable, Sequence
from typing import Any, Final

import tempe
from .display import Display
from .font import AbstractFont
from .geometry import Geometry
from .raster import Raster
from .shapes import (
    Shape,
    Polygons,
    PolyLines,
    Rectangles,
    Circles,
    Ellipses,
    Lines,
    VLines,
    HLines,
    rectangle,
)
from .markers import Marker, Markers, Points
from .bitmaps import Bitmaps, ColoredBitmaps
from .text import Text, HALIGN, VALIGN, LEFT, TOP
from .util import contains
from .colors import color, rgb565



#: The default set of layers used by Surfaces, in order from back to front.
BACKGROUND: Final[str] = "BACKGROUND"
UNDERLAY: Final[str] = "UNDERLAY"
IMAGE: Final[str] = "IMAGE"
DRAWING: Final[str] = "DRAWING"
OVERLAY: Final[str] = "OVERLAY"

LAYERS: Final[tuple[str, ...]] = (BACKGROUND, UNDERLAY, IMAGE, DRAWING, OVERLAY)

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
    def refresh(self, display: Display, working_buffer: bytearray) -> None:
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
        working_buffer : bytearray
            An empty bytearray that the Surface will use as memory for temporary
            drawing buffers.
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

    def polygons(
        self,
        layer: Any,
        geometry: Geometry[array] | Sequence[int],
        colors: Iterable[rgb565] | color,
        fill: bool = True,
        clip: tuple[int, int, int, int] | None = None,
    ) -> Polygons:
        """Create a new Polygons object and add it to the layer.

        Parameters
        ----------
        layer : Any
            The layer that the Polygons object is added to.
        geometry : Geometry[array] | Sequence[int]
            The geometry to use, or if a sequence of ints, a single polygon.
        colors : Iterable[rgb565] | color
            The colors of each polygon, or a color to use for all polygons.
        fill : bool
            Whether to fill the polygon or draw a one-pixel-wide outline.
        clip :  tuple[int, int, int, int] | None
            A clipping rectangle for the polygons.
        """

    def poly_lines(
        self,
        layer: Any,
        geometry: Geometry[array] | Sequence[int],
        colors: Iterable[rgb565] | color,
        clip: tuple[int, int, int, int] | None = None,
    ) -> PolyLines:
        """Create a new PolyLines object and add it to the layer.

        Parameters
        ----------
        layer : Any
            The layer that the PolyLines object is added to.
        geometry : Geometry[array] | Sequence[int]
            The geometry to use, or if a sequence of ints, a single polyline.
        colors : Iterable[rgb565] | color
            The colors of each polyline, or a color to use for all polylines.
        clip :  tuple[int, int, int, int] | None
            A clipping rectangle for the polylines.
        """

    def rectangles(
        self,
        layer: Any,
        geometry: Geometry[rectangle] | Sequence[rectangle] | rectangle,
        colors: Iterable[rgb565] | color,
        fill: bool = True,
        clip: tuple[int, int, int, int] | None = None,
    ) -> Rectangles:
        """Create a new Rectangles object and add it to the layer.

        Parameters
        ----------
        layer : Any
            The layer that the Rectangles object is added to.
        geometry : Geometry[tuple[int, int, int, int]] | Sequence[tuple[int, int, int, int]] | tuple[int, int, int, int],
            The geometry to use, or if a tuple of 4 ints, a single rectangle.
        colors : Iterable[int] | int | str
            The colors of each rectangle, or a color to use for all rectangles.
        fill : bool
            Whether to fill the polygon or draw a one-pixel-wide outline.
        clip :  tuple[int, int, int, int] | None
            A clipping rectangle for the rectangles.
        """

    def rounded_rectangles(
        self,
        layer: Any,
        geometry: Geometry[tuple[int, int, int, int]] | tuple[int, int, int, int],
        colors: Iterable[rgb565] | color,
        radius: int = 4,
        fill: bool = True,
        clip: tuple[int, int, int, int] | None = None,
    ) -> Rectangles:
        """Create a new RoundedRectangles object and add it to the layer.

        Parameters
        ----------
        layer : Any
            The layer that the RoundedRectangles object is added to.
        geometry : Geometry[tuple[int, int, int, int]] | tuple[int, int, int, int],
            The geometry to use, or if a tuple of 4 ints, a single rectangle.
        colors : Iterable[rgb565] | color
            The colors of each rectangle, or a color to use for all rectangles.
        radius : int
            The default corner radius.  The actual radius used for a particular
            rectangle is the minimum of the default radius, half the width, and
            half the height.
        fill : bool
            Whether to fill the polygon or draw a one-pixel-wide outline.
        clip :  tuple[int, int, int, int] | None
            A clipping rectangle for the rectangles.
        """

    def circles(
        self,
        layer: Any,
        geometry: Geometry[tuple[int, int, int]] | tuple[int, int, int],
        colors: Iterable[rgb565] | color,
        fill: bool = True,
        clip: tuple[int, int, int, int] | None = None,
    ) -> Circles:
        """Create a new Circles object and add it to the layer.

        Parameters
        ----------
        layer : Any
            The layer that the Circles object is added to.
        geometry : Geometry[tuple[int, int, int]] | tuple[int, int, int]
            The geometry to use, or if a tuple of 3 ints, a single circle.
        colors : Iterable[rgb565] | color
            The colors of each circle, or a color to use for all circles.
        fill : bool
            Whether to fill the polygon or draw a one-pixel-wide outline.
        clip :  tuple[int, int, int, int] | None
            A clipping rectangle for the circles.
        """

    def ellipses(
        self,
        layer: Any,
        geometry: Geometry[tuple[int, int, int, int]] | tuple[int, int, int, int],
        colors: Iterable[rgb565] | color,
        fill: bool = True,
        clip: tuple[int, int, int, int] | None = None,
    ) -> Ellipses:
        """Create a new Ellipses object and add it to the layer.

        Parameters
        ----------
        layer : Any
            The layer that the Ellipses object is added to.
        geometry : Geometry[tuple[int, int, int, int]] | tuple[int, int, int, int]
            The geometry to use, or if a tuple of 4 ints, a single ellipse.
        colors : Iterable[rgb565] | color
            The colors of each ellipse, or a color to use for all ellipses.
        fill : bool
            Whether to fill the polygon or draw a one-pixel-wide outline.
        clip :  tuple[int, int, int, int] | None
            A clipping rectangle for the ellipses.
        """

    def lines(
        self,
        layer: Any,
        geometry: Geometry[tuple[int, int, int, int]] | tuple[int, int, int, int],
        colors: Iterable[rgb565] | color,
        clip: tuple[int, int, int, int] | None = None,
    ) -> Lines:
        """Create a new Lines object and add it to the layer.

        Parameters
        ----------
        layer : Any
            The layer that the Lines object is added to.
        geometry : Geometry[tuple[int, int, int, int]] | tuple[int, int, int, int]
            The geometry to use, or if a tuple of 4 ints, a single line.
        colors : Iterable[rgb565] | color
            The colors of each line, or a color to use for all lines.
        clip :  tuple[int, int, int, int] | None
            A clipping rectangle for the lines.
        """

    def vlines(
        self,
        layer: Any,
        geometry: Geometry[tuple[int, int, int]] | tuple[int, int, int],
        colors: Iterable[rgb565] | color,
        clip: tuple[int, int, int, int] | None = None,
    ) -> VLines:
        """Create a new VLines object and add it to the layer.

        Parameters
        ----------
        layer : Any
            The layer that the VLines object is added to.
        geometry : Geometry[tuple[int, int, int]] | tuple[int, int, int, int]
            The geometry to use, or if a tuple of 3 ints, a single vertical line.
        colors : Iterable[rgb565] | color
            The colors of each line, or a color to use for all lines.
        clip :  tuple[int, int, int, int] | None
            A clipping rectangle for the lines.
        """

    def hlines(
        self,
        layer: Any,
        geometry: Geometry[tuple[int, int, int]] | tuple[int, int, int],
        colors: Iterable[rgb565] | color,
        clip: tuple[int, int, int, int] | None = None,
    ) -> HLines:
        """Create a new HLines object and add it to the layer.

        Parameters
        ----------
        layer : Any
            The layer that the HLines object is added to.
        geometry : Geometry[tuple[int, int, int]] | tuple[int, int, int]
            The geometry to use, or if a tuple of 3 ints, a single vertical line.
        colors : Iterable[rgb565] | color
            The colors of each line, or a color to use for all lines.
        clip :  tuple[int, int, int, int] | None
            A clipping rectangle for the lines.
        """

    def points(
        self,
        layer: Any,
        geometry: Geometry[tuple[int, int]] | tuple[int, int],
        colors: Iterable[rgb565] | color,
        markers: Iterable[Any] | int | str | framebuf.FrameBuffer,
        clip: tuple[int, int, int, int] | None = None,
    ) -> Points:
        """Create a new Points object and add it to the layer.

        Parameters
        ----------
        layer : Any
            The layer that the Points object is added to.
        geometry : Geometry[tuple[int, int]] | tuple[int, int]
            The geometry to use, or if a tuple of 2 ints, a single point.
        colors : Iterable[rgb565] | color
            The colors of each marker, or a color to use for all markers.
        markers : Iterable[Any] | int | str | framebuf.FrameBuffer
            The type of each marker, or a single marker to use for all points.
        clip :  tuple[int, int, int, int] | None
            A clipping rectangle for the points.
        """

    def markers(
        self,
        layer: Any,
        geometry: Geometry[tuple[int, int, int]] | tuple[int, int, int],
        colors: Iterable[rgb565] | color,
        markers: Iterable[Any] | int | str | framebuf.FrameBuffer,
        clip: tuple[int, int, int, int] | None = None,
    ) -> Markers:
        """Create a new Markers object and add it to the layer.

        Markers expect a geometry of the form (x, y, radius).

        Parameters
        ----------
        layer : Any
            The layer that the Markers object is added to.
        geometry : Geometry[tuple[int, int, int]] | tuple[int, int, int]
            The geometry to use, or if a tuple of 3 ints, a single point and radius.
        colors : Iterable[rgb565] | color
            The colors of each marker, or a color to use for all markers.
        markers : Iterable[Any] | int | str | framebuf.FrameBuffer
            The type of each marker, or a single marker to use for all points.
        clip :  tuple[int, int, int, int] | None
            A clipping rectangle for the markers.
        """

    def text(
        self,
        layer: Any,
        geometry: Geometry[tuple[int, int]] | tuple[int, int],
        colors: Iterable[rgb565] | color,
        text: Iterable[str] | str,
        alignments: Iterable[tuple[HALIGN, VALIGN]] | tuple[HALIGN, VALIGN] = (LEFT, TOP),
        font: AbstractFont | None = None,
        line_spacing: int = 0,
        clip: tuple[int, int, int, int] | None = None,
    ) -> Text:
        """Create a new Text object and add it to the layer.

        Parameters
        ----------
        layer : Any
            The layer that the Text object is added to.
        geometry : Geometry[tuple[int, int]] | tuple[int, int]
            The geometry to use, or if a tuple of 2 ints, a single point.
        colors : Iterable[rgb565] | color
            The colors of each string, or a color to use for all strings.
        text : Iterable[str] | str
            The strings to display at each point, or a single string to use at all points.
        alignments : Iterable[tuple[HALIGN, VALIGN]] | tuple[HALIGN, VALIGN]
            The the alignments of the text relative to the point specified in the
            geometry.  The default is `(LEFT, TOP)`, which places the top-left corner
            of the text at the specified points.
        font : AbstractFont | None
            The font to use for the text.  If None, the default FrameBuffer
            8x8 monospaced font will be used.
        line_spacing: int
            Add more or less space between adjacent lines.
        clip :  tuple[int, int, int, int] | None
            A clipping rectangle for the text.
        """

    def bitmaps(
        self,
        layer: Any,
        geometry: Geometry[tuple[int, int, int, int]] | tuple[int, int, int, int],
        bitmaps: Iterable[framebuf.FrameBuffer] | framebuf.Framebuffer,
        colors: Iterable[rgb565] | color | None,
        key: int = -1,
        palette: array[rgb565] | None = None,
        clip: tuple[int, int, int, int] | None = None,
    ) -> Bitmaps | ColoredBitmaps:
        """Create a new Bitmaps or ColoredBitmaps object and add it to the layer.

        Parameters
        ----------
        layer : Any
            The layer that the bitmaps object is added to.
        geometry : Geometry[tuple[int, int]] | tuple[int, int]
            The geometry to use, or if a tuple of 4 ints, a single rectangle.
        bitmaps : Iterable[framebuf.FrameBuffer] | framebuf.Framebuffer
            The colors of each string, or a color to use for all strings.
        colors : Iterable[rgb565] | color | None
            If None, the bitmaps are assumed to be either RGB565 bitmaps, or
            a palette must be provided, otherwise the bitmap is assumed to be
            a 1-bit bitmap and this parameter provides the colors of each bitmap,
            or a color to use for all bitmaps.
        key : int
            For bitmaps that are not using ``colors``, an RGB565 color that
            will be considered transparent when rendering the bitmap.  If the
            value is -1, there is no transparent color.
        palette : array[rgb565] | None
            If ``colors`` is None and the bitmaps aren't RGB565 format, this is
            an array containing RGB565 color values for each color value in the
            given format.
        clip :  tuple[int, int, int, int] | None
            A clipping rectangle for the bitmaps.
        """

    def _check_geometry[T](
        self,
        geometry: Geometry[T] | array | list[int] | tuple[int, ...],
        coords: int | None,
    ) -> Geometry[T]: ...

    def _check_colors(self, colors: Iterable[rgb565] | color) -> Iterable[rgb565]: ...

__all__ = ["Surface"]

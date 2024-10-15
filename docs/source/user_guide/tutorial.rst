========
Tutorial
========

If you have a microcontroller with a screen capable of color graphics,
you want your applications to be able to draw to it in an efficient and
consistent way.  Micropython includes the :py:mod:`framebuf` module, which
allows you to draw into a region of memory, but even for a small screen
drawing in 16-bit color is very expensive. Additionally most of the time
you only need to update small parts of the total screen area when displayed
data changes, but a framebuffer can't track what is drawn in the region
that needs updating and so you will likely end up redrawing everything.

Basic Drawing
=============

Tempe abstracts these concerns away by providing a |Surface| object that
represents a layered 2D coordinate space, and tracks the |Shape| objects
that are drawn to it::

    surface = Surface()

    # fill the background with white pixels
    background = Rectangles([(0, 0, 320, 240)], [0xffff])
    surface.add_shape('BACKGROUND', background)

    # draw some black text in the main drawing layer
    hello_tempe = Text([(112, 116)], [0x0000], ["Hello Tempe!"])
    surface.add_shape('DRAWING', hello_tempe)

To actually render the image, you need to provide a |Display| subclass
that can handle copying a buffer to a rectangle on the physical device.
Particularly for non-standard devices or interfaces, you may need to
write this code, but there are examples of how to do this for common
displays.

You also need to provide a writable array of unsigned 16-bit integers
that Tempe can use to render raster images into before copying them to
the display.  The larger this chunk of memory is the better, but it can
be allocated once and re-used repeatedly for drawing operations.

Actual drawing is performed by calling |refresh| with the display and
the buffer::

    # a buffer one quarter the size of the screen
    working_buffer = array('H', bytearray(2*320*61))

    # set up the display object
    display = ST7789()
    display.init()

    # refresh the display
    surface.refresh(display, working_buffer)

The |refresh| method only updates the region of the screen that needs
updating (in this case, since this is the first refresh, it will be the
entire screen), and automatically handles situations where the working
buffer is too small for the size of the region which needs to be rendered.
Under the covers, it is making calls to the built-in :py:mod:`framebuf`
module to set the pixels in the working buffer for the region that is
being updated, before copying the data across to screen device.

This should display something like the following:

..  image:: hello_world.png
    :width: 160


Shapes and Geometry
===================

Tempe provides a number of fundamental |Shape| subclasses, mostly based
around what the underlying :py:mod:`framebuf` library provides: lines,
rectangles, ellipses and general polygons.

However the Tempe shape objects represent multiple instances of each of
these objects, as this permits more efficient iteration and representation
of the shapes.  For example, to draw the bars of a bar graph you might want
to draw three rectangles with three different colors, so you can call::

    bars = Rectangles(
        [(4, 4, 8, 100), (4, 16, 8, 80), (4, 28, 8, 50)],
        [red, lime, blue],
    )
    surface.add_shape('DRAWING', bars)

Where these rectangles are a related part of a larger graphical entity,
it will generally be more efficient than drawing the three rectangles
separately.

These shape objects expect to be given an appropriate |Geometry| that
describes the geometric properties of each iteration of the shapes
to be rendered.  For |Rectangles| it expects to get a |Geometry| that
can be iterated over to produce sequences of length 4, holding x, y,
width, and height, but other shapes expect different geometric information.
For example, |Circles| expect an iterator that produces x, y and radius,
while |Polygons| expect the iterator to produce :py:class:`~array.array`
instances with alternating x and y values: [x0, y0, x1, y1, x2, y2, ...].

|RowGeometry|
-------------

Tempe refers to this basic object-by-object representation of geometric
information as "row-oriented" geometry, and provides the |RowGeometry|
class as a helper.  For example, if we wanted to create a collection of
|Polygons| then rather than having to write something like::

    triangles = Polygons(
        [
            array('h', [10, 10, 10, 20, 20, 20]),
            array('h', [20, 10, 20, 20, 30, 20]),
            array('h', [30, 10, 30, 20, 40, 20]),
        ],
        [red, lime, blue],
    )

you can instead call::

    triangles = Polygons(
        RowGeometry.from_lists([
            (10, 10, 10, 20, 20, 20),
            (20, 10, 20, 20, 30, 20),
            (30, 10, 30, 20, 40, 20),
        ]),
        [red, lime, blue],
    )

which will handle creating the arrays for you.  Similarly if we were to
create the rectangles using::

    bars = Rectangles(
        RowGeometry.from_lists([
            (4, 4, 8, 100), (4, 16, 8, 80), (4, 28, 8, 50)
        ]),
        [red, lime, blue],
    )

then the data will be converted to arrays of 16-bit integers, which use
less tha half as much memory.

|ColumnGeometry|
----------------

When building geometry it can sometimes be more convenient to specify
the geometrip properties in different ways than "row-oriented".  For
example, when building a horizontal bar chart, the principal information
that you are working with is a sequence of bar widths.  It's natural then
to want to build the geometry instead in a "column-oriented" fashion:
a sequence of x-values, then a sequence of y-values, then a sequence of
widths, and finally a sequence of heights.

Tempe provides a |ColumnGeometry| class for this purpose::

    xs = [4, 4, 4]
    ys = [4, 16, 28]
    widths = [100, 80, 50]
    heights = [8, 8, 8]

    bars = Rectangles(
        ColumnGeometry([xs, ys, widths, heights]),
        [red, lime, blue],
    )

When the geometry is expressed this way, we can see that there is a lot
of repetition in the columns and as we'll see when we talk about |DataView|
classes, we can take advantage of this to produce more compact and efficient
representations of the geometry.

|StripGeometry|
---------------

Another common type of data visualization is a line plot.  The |Lines|
shape expects its geometry to provide it with sets of end-point coordinates
(x1, y1, x2, y2).  So if we have data points at (10, 20), (15, 50), (20, 40),
(25, 60) and (30, 25), then to plot those with |RowGeometry| you would
need to have something like::

    line_plot = Lines(
        RowGeometry.from_lists([
            [10, 20, 15, 50],
            [15, 50, 20, 40],
            [20, 40, 25, 60],
            [25, 60, 30, 25],
        ]),
        colors=[black] * 4,
    )

It's clear that this is inefficient, as the second coordinate pair is
repeated as the first coordinate pair of the next line.  |ColumnGeometry|
is not much better unless you do clever things with :py:class:`memoryview`
objects.

In cases like this, where part of the geometry from one iteration is used
in the next, Tempe provides the |StripGeometry| class, where vertices can
simply be provided as an array of x, y values and it will generate the
appropriate sets of values for each iteration.

For example, out line plot can be written as::

    line_plot = Lines(
        StripGeometry(
            [10, 20, 15, 50, 20, 40, 25, 60, 30, 25],
            n_vertices=2,
            step=1,
        ]),
        colors=[black] * 4,
    )

Other common geometries created this way are triangle and quad strips.

|DataView| Classes
==================

Looking at the column geometry section above::

    xs = [4, 4, 4]
    ys = [4, 16, 28]
    widths = [100, 80, 50]
    heights = [8, 8, 8]

    bars = Rectangles(
        ColumnGeometry([xs, ys, widths, heights]),
        [red, lime, blue],
    )

you might notice that the ``xs`` and ``height`` values are repeated.
For three rectangles, this is not likely a problem, but if you are
plotting 100 or 1000 values, the memory use starts to add up.  In these
situations it makes sense to trade-off a lot of space for a little
computation time.

Tempe provides a number of |DataView| classes that allow data values
to be "viewed" in different ways.  For example, there is a |Repeat|
data view which creates an iterable that repeats a value over and over.

So we could instead have used::

    xs = Repeat(4)
    ys = [4, 16, 28]
    widths = [100, 80, 50]
    heights = Repeat(8)

    bars = Rectangles(
        ColumnGeometry([xs, ys, widths, heights]),
        [red, lime, blue],
    )

Similarly there are |Count| and |Range| data views that generate evenly
spaced values, and a |Cycle| data view that extends an iterable by
repeating it cyclically.  All of these data views can be used both for
|Geometry| parameters and for colors and other aesthetics::

    xs = Repeat(4)
    ys = Count(start=4, step=12)
    widths = [100, 80, 50]
    heights = Repeat(8)
    colors = Cycle([red, lime, blue])

    bars = Rectangles(
        ColumnGeometry([xs, ys, widths, heights]),
        colors,
    )

Using data views, geometries and shapes, you can quickly and efficiently
build standard data visualizations::

    def horizontal_bar_chart(
        surface,
        x, y,
        widths,
        labels,
        colors,
        bar_height=8,
    ):
        label_width = 8 * max(len(label) for label in labels)
        label_xs = Repeat(x)
        bar_xs = Repeat(x + label_width)
        ys = Count(y, bar_height)

        label_text = Text(
            ColumnGeometry([label_xs, ys], labels),
            labels,
            Repeat(black),
        )
        bars = Rectangles(
            [bar_xs, ys, widths, Repeat(bar_height)],
            colors,
        )
        suface.add_shape("OVERLAY", label_text)
        suface.add_shape("DRAWING", bars)

Complex Shapes
==============

Beyond simple geometric shape classes, Tempe provides a number of more complex
shapes

Text and Fonts
--------------

The |Text| shape handles drawing text at specified locations and colors.
By default it uses the built-in :py:mod:`framebuf` font, which is a simple
8x8 monospaced font.  It is readable and functional on a typical device,
but is not ideal for general interfaces: in particular it is available in
just one size.

For more better text rendering, Tempe currently can use bitmap fonts of the
format produced by Peter Hinch's font_to_py script, as well as a slightly
more efficient internal variant.  Tempe provides bitmap versions of Google's
Roboto font at 16 pt, which looks reasonably good on small screens.

These fonts are typically shipped as modules::

    from tempe.font import TempeFont
    from tempe.fonts import roboto16bold

    font = TempeFont(roboto16bold)

    hello_tempe = Text([(64, 107)], [0x0000], ["Hello Tempe!"], font=font)
    surface.add_shape('DRAWING', hello_tempe)

Using this in the original example from the tutorial will generate something
like the following:

..  image:: hello_font.png
    :width: 160

TODO: support alright fonts

Markers and Scatterplots
------------------------

The |Markers| shape expects a geometry consisting of an x, y point and a
marker size, the colors for each marker and the shape of each marker.
The marker shapes can be specified as:

- constants :py:attr:`Marker.CIRCLE`, :py:attr:`Marker.SQUARE`, etc. for
  standard marker shapes
- a string, which will get rendered at the location in the default framebuf font
- a :py:class:`framebuf.FrameBuffer` containing a 1-bit image

The string and :py:class:`framebuf.FrameBuffer` markers currently ignore the
size parameter.

Bitmaps
-------

The |Bitmaps| shape blits FrameBuffer instances at the given locations.
These must either be in RGB565 format, or supply a palette and optional
key-color for transparency.  The |ColoredBitmaps| shapes render 1-bit
framebuffers in the specified colors.


.. |Surface| replace:: :py:class:`~tempe.surface.Surface`
.. |refresh| replace:: :py:meth:`~tempe.surface.Surface.refresh`
.. |Shape| replace:: :py:class:`~tempe.shapes.Shape`
.. |Rectangles| replace:: :py:class:`~tempe.shapes.Rectangles`
.. |Lines| replace:: :py:class:`~tempe.shapes.Lines`
.. |Polygons| replace:: :py:class:`~tempe.shapes.Polygons`
.. |Circles| replace:: :py:class:`~tempe.shapes.Circles`
.. |Text| replace:: :py:class:`~tempe.text.Text`
.. |Markers| replace:: :py:class:`~tempe.markers.Markers`
.. |Bitmaps| replace:: :py:class:`~tempe.bitmaps.Bitmaps`
.. |ColoredBitmaps| replace:: :py:class:`~tempe.bitmaps.ColoredBitmaps`
.. |Display| replace:: :py:class:`~tempe.display.Display`
.. |Geometry| replace:: :py:class:`~tempe.geometry.Geometry`
.. |RowGeometry| replace:: :py:class:`~tempe.geometry.RowGeometry`
.. |ColumnGeometry| replace:: :py:class:`~tempe.geometry.ColumnGeometry`
.. |StripGeometry| replace:: :py:class:`~tempe.geometry.StripGeometry`
.. |DataView| replace:: :py:class:`~tempe.data_view.DataView`
.. |Repeat| replace:: :py:class:`~tempe.data_view.Repeat`
.. |Cycle| replace:: :py:class:`~tempe.data_view.Cycle`
.. |Count| replace:: :py:class:`~tempe.data_view.Count`
.. |Range| replace:: :py:class:`~tempe.data_view.Range`

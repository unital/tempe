============
Introduction
============

.. currentmodule:: tempe

Tempe is a pure-Micropython graphics system designed to be make using the
full capabilities of display devices more accessible, particularly on
memory-constrained microcontrollers.  The aim is to allow data scientists,
user interface designers and data visualization specialists to be able to
create beautiful, responsive displays without needing to worry about the
mechanics of rendering to bytes on the screen device, handling partial screen
updates, and so on.

The Problem Tempe Solves
========================

There are many high-quality, inexpensive LCD and OLED displays that are
available and capable of being driven by modern Micropython-based
microcontrollers: typical devices are as large as 320x240 (QVGA) and capable
of 16-bit or 18-bit color and use SPI or I2C to communicate meaning that
many pins are available for other uses.

Programs which want to use these displays need to render their graphics
into a framebuffer and then transmit the raw bytes to the display's internal
memory.  Micropython provides a reasonably high-level :py:mod:`framebuf` module
that allows code to draw to a framebuffer.  However a framebuffer for one of
these screens at 16-bit color depth requires over 153K, where the
microcontroller might have a total of 256K available.

A typical data visualization application is going to need additional memory
for the data being displayed, bitmap fonts, icons, and for the program
itself, and it is very easy to run out of memory.

Additionally, dynamic applications where the information being displayed is
changing need to redraw the buffer on every update, which for complex displays
can be challenging to do in a responsive way.

One way to handle this situation is to simply reduce the color-depth, for
example using an 8-bit or 4-bit color palette with a corresponding reduction
in the buffer size, but with a corresponding loss of color fidelity.

However there are also standard ways to handle these issues while still keeping
full 16-bit color, such as tracking which regions of the screen have changed
as the display updates, and rendering to subregions of the screen as needed
using smaller in-memory buffers.  However this significantly complicates the
drawing code if using the standard :py:mod:`framebuf` module: what is being
drawn needs to be translated into the relative coordinates of the smaller
buffer and, ideally, objects that are outside of the region being updated
shouldn't attempt to draw themselves at all.

At its core, Tempe solves this problem: it provides a high-level drawing API
that lets users concentrate on what they want to draw and not how those drawing
commands are translated to bytes in a framebuffer or transmitted to the screen.
It handles partial re-draws of the display with automatic clipping of shapes
which are outside of the drawing area, and where memory is constrained it can
automatically break the updates into multiple smaller updates that fit into
the available memory.

Additionally, the design of the API permits more efficient memory use when
specifying the geometry and aesthetics of the graphical objects being drawn.

It does this using Micropython only, meaning users do not need to cross-compile
C code or create a custom firmware: it can be installed using standard mechanisms
lime ``mip`` by users who are comfortable working with Micropython.

What Tempe Isn't
================

Tempe is built on top of the standard Micropython framebuffer module, so
it can't do sub-pixel rendering, alpha compositing/variable opacity or
full 24/32-bit color (or even 18-bit color), and has a number of other
limitations.  Some experimentation shows that it may be practical to
extend the framebuffer module using :py:mod:`micropython.viper` to
provide some of these capabilities, but that is not currently on the
roadmap.

Tempe doesn't provide much for devices which are not memory constrained.
If your available memory is in the 100s of megabytes, you are running on
Linux, and you are driving an HDMI display, then you are likely
better-off with regular Python and one of its drawing libraries such as
Cairo, Agg (via something like Celiagg), Qt's QPainter, PyOpenGL or even
the basic drawing capabilities of Pillow.  Most of these systems are capable
of sub-pixel rendering and full alpha compositing.

Tempe is primarily concerned with drawing graphics and text, and
is not a complete UI or data visualization system.  As experience with the
system grows, we expect that additional libraries built on top of Tempe
will grow to address more complete use cases.  However Tempe *does* include
the basic hooks to interact with an asyncio-based application to automatically
update a display when things change, and interfaces particularly nicely with
the `Ultimo <https://unital.github.io/ultimo/>`_ framework.

For user interfaces, Tempe is a rendering layer that could be used as part of
the "View" component of a Model-View-Controller-style system.  Tempe can draw
shapes and text to display a user interface, but it has no concept of things
like text fields, buttons and sliders.

For data visualization, Tempe can be thought of as providing the geometry and
aesthetics in a Grammar of Graphics-style system.  Tempe assumes that data
has already had any statistical transformations applied, and has been mapped
to screen values.

Why "Tempe"
===========

Tempe follows the naming style of `Ultimo <https://unital.github.io/ultimo/>`_
taking its name from a suburb of my home town of Sydney.  The name "Tempe"
itself comes from the Vale of Tempe at the foot of Mt. Olympus in Greece,
known for its dramatic landscape.

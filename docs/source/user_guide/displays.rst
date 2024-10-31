===============
Display Drivers
===============

There are a wide variety of displays, controllers and communication protocols
that may potentially be able to be used with Tempe. There is, however, a
limit to the hardware which the Tempe developers have access to.
This means that you may need to implement a driver for your display.
Fortunately, there is just one method that you need to implement for a
display driver.

Implementing Display Drivers
============================

To get the full advantage of Tempe, a device needs to be capable of updating
just a rectangular region of the screen.  To implement a driver for the
display, this is all you need to provide.

The |Display| protocol is simply the following::

    class Display:

        def blit(self, buffer, x, y, w, h):
            """Send a buffer of pixels to the rectangle (x, y, w, h).

            The buffer will consist of w * h 16-bit pixels exactly and so
            will have a size of 2 * w * h bytes.
            """
            ...

If you are lucky you have a device driver which already supports this sort of
windowed transfer (and doesn't need a full-screen framebuffer).  In this case
you can simply wrap the device to make the API match::

    class MyDisplay:

        def __init__(self, my_display):
            self._display = my_display

        def blit(self, buffer, x, y, w, h):
            """Send a buffer of pixels to the rectangle (x, y, w, h).

            The buffer will consist of w * h 16-bit pixels exactly and so
            will have a size of 2 * w * h bytes.
            """
            self._display.blitmethod(buffer, x, y, w, h)

Failing this, you may need to read the datasheet for your display and work
out how to initialize it and perform these operations.

Currently Supported Displays
============================

|FileDisplay|
-------------

The Tempe library comes with a simple |FileDisplay| that writes raw RGB565
bytes to a file.  This is used for testing and to produce images for
documentation.  There is a CPython script in the `ci` directory that
uses Pillow to convert these to PNG files.

|ST7789|
--------

The |tempe_displays| library has a base class for devices which use the
ST7789 controller, and a subclass |ST7789_SPI| which talks to the
controller using SPI.  These classes are not complete: you will need to
subclass and fill in missing functionality for your particular device: for
the base device you will need to supply write methods, and for the SPI
device you will need to provide appropriate initialization for the device
(which may depend on physical properties of the hardware, such as gammma
curve adjustments).  Consult your hardware documentation.

Pimoroni ST7789 SPI Displays
----------------------------

This is a family of similar displays of various sizes that use the ST7789
controller and SPI to communicate with it.  The |PimoroniDisplay| class,
if given the size of the screen should be able to work out which device it
is and configure it appropriately.  Some displays, such as the round
breakout garden display and the original Pico Display Pack are centered
in the ST7789 memory space, and should have the `centered` parameter set
to True.

Since starting the display requires some time waiting for commands to complete,
they have an asynchrononous inititiaization method.

The |PimoroniDisplay| classes know the standard pin layouts for these boards,
and so these can usually be initialized something like::

    async def init_display()
        display = PimoroniDisplay(size=(320, 240))
        await display.init(rotation=270)
        display.backlight_pin(1)
        return display

.. |Display| replace:: :py:class:`~tempe.display.Display`
.. |FileDisplay| replace:: :py:class:`~tempe.display.FileDisplay`
.. |tempe_displays| replace:: :py:class:`tempe_displays`
.. |ST7789| replace:: :py:class:`~tempe_displays.st7789.base.ST7789`
.. |ST7789_SPI| replace:: :py:class:`~tempe_displays.st7789.spi.ST7789_SPI`
.. |PimoroniDisplay| replace:: :py:class:`~tempe_displays.st7789.pimoroni.PimoroniDisplay`

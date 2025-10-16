==============
Tempe Examples
==============

The Tempe repository contains some example code that demonstrates the concepts
involved in working with Tempe as a library.  Most of the code was written to
work on Raspberry Pi Picos with Pimoroni 320x240 ST7789-based SPI displays.
Users have had success with other ST7789-based displays, and in principle any
display which allows blitting a 16-bit framebuffer into a windowed region of
memory should work.

Support Modules
===============

Extra Fonts and Data Modules
----------------------------

Some examples use additional modules to provide fonts and data that are not installed
by the usual `mip` install.  You will either need to install the directories
`example_fonts` and `data` on your device manually, or use the `ci.deploy_to_device`
command as discussed in Installation, Development Installation.

The `tempe_config` Module
-------------------------

To allow the examples to work with different displays, they expect the user to
have added a :py:mod:`tempe_config` module somewhere on the Python path (eg. at
the top-level directory of the flash storage device), containing an async
function :py:func:`init_display` that might look something like the following::

    async init_display():
        display = MyDisplay()
        await display.init()
        return display

There are some examples which show how to write such a file for:

- `Pimoroni ST7789-based SPI displays <https://github.com/unital/tempe/tree/main/examples/configs/tempe_config_pimoroni_spi.py>`_
- `Waveshare Pico ResTouch SPI displays <https://github.com/unital/tempe/tree/main/examples/configs/tempe_config_pico_res_touch.py>`_

If your device is not currently supported, you may need to write a Display subclass
in addition to the `init_display`.  The following is an example of how to wrap a
3rd party driver for use with the examples:

- `GC9A01 screens using Robert Hughes' gc9a01_mpy firmware <https://github.com/unital/tempe/tree/main/examples/configs/tempe_config_gc9a01_mpy.py>`_

Ultimo
------

One example uses the Ultimo library.  You can mip install this as described in the
Ultimo documentation.

Running the Examples
====================

Once installed, the examples can be run in a number of ways:

Running using your IDE
----------------------

Most Micropython IDEs allow you to run scripts directly from the IDE.
This should work for all examples, although this has only been tested
with Thonny.

Running using mpremote
----------------------

Once the support modules are installed, you can run example files stored on your
computer's filesystem via `mpremote`. For example::

    mpremote run examples/hello_world.py

Running from the Python REPL
----------------------------

If the example files have been installed on the Python path, you should be
able to run them by importing their `main` function and calling it.

    >>> from hello_world import main
    >>> main()

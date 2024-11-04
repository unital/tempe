==============
Tempe Releases
==============

Version 0.x
===========

Version 0.2
-----------

This is a small release which fixes a number of bugs, provides formal
support for Pimoroni SPI-based ST7789 displays, and adds information about
writing displays to the documentation.

Version 0.2 now assumes that the memory used by ``Raster`` objects is now
a simple read/write buffer of bytes, rather than an array of unsigned 16-bit
integers, which allows allocation of larger chunks of memory.

Thanks to those involved in the Micropython discussion boards for the
feedback that led to these improvements.

Version 0.1
-----------

October 28th, 2024

Initial release.
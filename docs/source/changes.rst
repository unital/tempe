==============
Tempe Releases
==============

Version 0.x
===========

Version 0.3
-----------

November 12th, 2024

This is a release which focuses on performance.  Most shape classes now check
to see whether each sub-shape intersects with the current drawing region in
the raster, and skip rendering if this is the case.  Text objects perform this
check at the level of individual character.  This gives a significant
improvement in rendering time, particularly when working with smaller buffers,
for large Text objects, and when performing updates.

Additionally, profiling indicated that character lookup in bitmap font objects
was a major bottleneck for text rendering.  Fonts now cache those lookups in a
dictionary.  This can be turned off with an initialization option, and there is
a method to clear the cache if the memory is needed.

These changes add up to an order of magnitude speed improvement in some cases.

Additional improvements include:

- Text objects can now be vertically and horizontally aligned relative to the
  geometry.
- a new Window Shape that holds a subsurface that makes scrolling groups of
  Shapes easier.
- support for Waveshare Pico-ResTouch-LCD 2.8 displays, thanks to @JoGeDuBo.
- replace Roboto fonts with Ubuntu fonts, which render better at small sizes.
- additional examples and various small fixes.

Thanks
~~~~~~

The following people contributed to this release:

    JoGeDuBo, Corran Webster

Version 0.2
-----------

November 5th, 2024

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
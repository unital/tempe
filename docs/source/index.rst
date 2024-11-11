.. Tempe documentation master file, created by
   sphinx-quickstart on Mon Oct 14 07:23:02 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Tempe
=====

Beautiful, Efficient Micropython Graphics

Tempe is a graphics library designed to support everyday display and data
visualization tasks on small, 16-bit+ color screens.

.. image:: user_guide/scatter_plot.png
   :align: right
   :scale: 75%

- Pure Micropython codebase—no C libraries, cross-compiling or custom firmware
  needed—``mip``-install and go.
- Full 16-bit color support even on memory-constrained microcontrollers.
- API designed to support common data visualization patterns, such as polar
  coordinates, efficiently.
- Transparent support for partial display updates and damage-region tracking,
  allowing memory-efficency and fast updates for small changes.
- Core API avoids floating-point operations.
- Asyncio integration to allow simple support for dynamically changing
  graphics.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   user_guide/index.rst
   changes.rst



License
-------

Most of the code is licensed using the MIT license:

  MIT License

  Copyright (c) 2024 Unital Software

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  SOFTWARE.

The bitmap fonts included with the Tempe source are derived from Ubuntu fonts
and are licensed with the Ubuntu Font License: see
`github.com/unital/tempe/blob/main/src/tempe/fonts/README.rst <https://github.com/unital/tempe/blob/main/src/tempe/fonts/README.rst>`_
for details.


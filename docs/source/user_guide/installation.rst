===============
Getting Started
===============

.. currentmodule:: tempe

At the moment installation is experimental, but should work.

Installation
------------

Tempe can be installed from github via :py:mod:`mip`.  You can
install either released versions or the unstable head of the main
branch, as needed.

You need to install the Tempe library and display drivers separately.
If you do not need the ST7789 drivers and are writing your own, you don't
need to install the display drivers.

Released Versions
~~~~~~~~~~~~~~~~~

Released versions can be installed with ``mip`` by specifying the release
branch:

..  code-block:: python-console

    >>> mip.install("github:unital/tempe/src/tempe", version="rel/0.3")
    >>> mip.install("github:unital/tempe/src/tempe_displays", version="rel/0.3")

or using :py:mod:`mpremote`:

..  code-block:: console

    mpremote mip install github:unital/tempe/src/tempe@rel/0.3
    mpremote mip install github:unital/tempe/src/tempe_displays@rel/0.3

Unstable
~~~~~~~~

Unstable versions are installed from the main branch of the Github repo:

..  code-block:: python-console

    >>> mip.install("github:unital/tempe/tree/src/tempe/package.json")
    >>> mip.install("github:unital/tempe/tree/src/tempe_displays/package.json")

or using :py:mod:`mpremote`:

..  code-block:: console

    mpremote mip install github:unital/tempe/tree/src/tempe/package.json
    mpremote mip install github:unital/tempe/tree/src/tempe_displays/package.json

Development Installation
------------------------

To simplify the development work-cycle with actual hardware, there is a
helper script in the ci directory which will download the files onto the
device.  You will need an environment with ``mpremote`` and ``click``
installed.  For example, on a Mac/Linux machine:

..  code-block:: console

    python -m venv tempe-env
    source tempe-env/bin/activate
    pip install mpremote click

should give you a working environment.

Ensure that the Pico is plugged in to your computer and no other program
(such as Thonny or an IDE) is using it.  You can then execute:

..  code-block:: console

    python -m ci.deploy_to_device

and this will install the tempe code in the ``/lib`` directory (which is
on :py:obj:`sys.path`) and the examples in the main directory, with example
data in ``/data`` and example fonts in ``/example_fonts``.

You can optionally used the ``-march`` argument to have the files (other than
the examples and example driveers) cross-compiled for the specified architecture.
Eg. for a Raspberry Pi Pico, you would do:

..  code-block:: console

    python -m ci.deploy_to_device -march armv6m

Running the Examples
--------------------

The example code works with a Raspberry Pi Pico and its internal hardware,
plus a ST7789-based display that communicates via SPI; in particular development
has been done against various Pimoroni screens (Pico Packs, Breakout Garden,
and Pico Explorer should work).

Most examples can be run from inside an IDE like Thonny.

Writing Code Using Tempe
-------------------------

Although Tempe is a Micropython library, it provides ``.pyi`` stub files for
typing support.  If you add the tempe sources to the paths where tools like
``mypy`` and ``pyright`` look for stubs, then you should be able to get
type-hints for the code you are writing in your IDE or as a check step as
part of your CI.

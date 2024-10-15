===============
Getting Started
===============

.. currentmodule:: tempe

At the moment installation is from the GitHub repo source.  In the future
we would like to add ``mip`` and better stub file support.

Installation
------------

Tempe can be installed from github via :py:mod:`mip`.

..  code-block:: python-console

    >>> mip.install("github:unital/tempe/src/tempe/package.json")

or using :py:mod:`mpremote`:

..  code-block:: console

    mpremote mip install github:unital/tempe/src/tempe/package.json

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
on :py:obj:`sys.path`) and the examples in the main directory (with
example drivers in ``/devices``).

Running the Examples
--------------------

The example code works with a Raspberry Pi Pico and it's internal hardware,
plus a ST7789-based display that communicates via SPI; in particular development
has been done against various Pimoroni screens (Pico Packs, Breakout Garden,
and Pico Explorer should work).

Most examples can be run from inside an IDE like Thonny.

Writing Code Using Tempe
-------------------------

Althought Tempe is a Micropython library, it provides ``.pyi`` stub files for
typing support.  If you add the tempe sources to the paths where tools like
``mypy`` and ``pyright`` look for stubs (in particular, ``pip install -e ...``
will likely work), then you should be able to get type-hints for the code you
are writing in your IDE or as a check step as part of your CI.

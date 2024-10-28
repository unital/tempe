# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

"""Font ABCs and support for bitmapped fonts."""

from array import array
import framebuf
from types import ModuleType
from typing import Type, TypeAlias


class AbstractFont:
    """ABC for fonts.

    Note: this API will likely evolve, particularly if support for vector
    fonts is added.

    Attributes
    ----------
    height : int
        The height of the font.
    baseline : int
        The position of the baseline of the font relative to the top
        of a character buffer.
    monospaced : bool
        Whether the font is monospaces.
    """

    def measure(self, text: str) -> tuple[int, int, int, int]:
        """Measure the size of a line of text in the given font.

        Parameters
        ----------
        text : str
            The text to measure.  This shouldn't includ newlines, tabs, or
            other control characters.

        Returns
        -------
        bounds : rect
            This returns a tuple of (leading, descent, width and height).
        """


class BitmapFont(AbstractFont):
    """ABC for bitmapped fonts."""

    def bitmap(self, char: str) -> tuple[array, int, int]:
        """Get a character bitmap and dimensions.

        Parameters
        ----------
        char : str
            A single character to get the bitmap for.

        Returns
        -------
        buffer : array
            The bits of the character in MONO_HLSB format as an array.
        width : int
            The width of the character buffer.
        height : int
            The height of the character buffer.
        """


class FontToPy(BitmapFont):
    """Bitmapped font that uses Font To Py fonts.

    Font to Py stores the font information as modules which is efficient if
    the fonts are complied to .mpy or stored in the firmware.

    Parameters
    ----------
    mod : module
        The font module containing the module data.

    Usage
    -----
    To use this, import the font module and pass it to the class::

        from my_fonts import helvetica16

        font = FontToPy(helvetica16)

    References
    ----------
    - Font to Py repo: `github.com/peterhinch/micropython-font-to-py <https://github.com/peterhinch/micropython-font-to-py>`_
    """
    def __init__(self, mod: ModuleType): ...


class MicroFont(BitmapFont):
    """Bitmapped font that uses MicroFont fonts.

    MicroFont stores font information in custom .mfnt format files.

    Parameters
    ----------
    filename : str
        The path to the .mfnt format file.
    cache_index : bool
        Whether to cache index data in memory.
    cache_chars : bool
        Whether to cache character data in memory.

    Usage
    ----
    To use this, pass the path to the file::

        font = MicroFont("my_fonts/helvetica16.mfnt")

    References
    ----------
    - MicroFont repo: `github.com/antirez/microfont <https://github.com/antirez/microfont>`_
    """
    def __init__(self, filename, cache_index=True, cache_chars=False): ...


class TempeFont(BitmapFont):
    """Internal bitmapped font format.

    This is an internal font format based on Font To Py format with some
    minor refinements.  There is no public tooling to produce these at the
    moment, and the format will likely change over time.

    Parameters
    ----------
    mod : module
        The font module containing the module data.

    Usage
    -----
    To use this, import the font module and pass it to the class::

        from tempe.fonts import roboto16

        font = TempeFont(roboto16)
    """
    def __init__(self, mod: ModuleType): ...

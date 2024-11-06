# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

"""Font ABCs and support for bitmapped fonts."""


import framebuf
from uctypes import bytearray_at, addressof

from .util import bisect16

class AbstractFont:
    def measure(self, text):
        """Measure the size of a line of text in the given font."""
        raise NotImplementedError


class BitmapFont(AbstractFont):
    def bitmap(self, char):
        """Get a character bitmap and dimensions."""
        raise NotImplementedError


class FontToPy(BitmapFont):
    def __init__(self, mod):
        self.font = mod
        self.height = mod.height()
        self.baseline = mod.baseline()
        self.monospaced = mod.monospaced()
        self._mvfont = memoryview(mod._mvfont)
        self._msvp = memoryview(mod._mvsp)
        self._cache = {}

    def measure(self, text):
        width = 0
        for char in text:
            n  = ord(char)
            if n not in self._cache:
                self._cache[n] = self._get_char(n)
            width += self._cache[n][2]
        return (0, self.height - self.baseline, width, self.height)

    def bitmap(self, char):
        n  = ord(char)
        if n not in self._cache:
            self._cache[n] = self._get_char(n)
        return self._cache[n]

    def clear_cache(self):
        self._cache = {}

    def _get_char(self, n):
        offset = bisect16(self._msvp, n, len(self._msvp) >> 2) << 3
        width = self._mvfont[offset] | (self._mvfont[offset + 1] << 8)
        next_offset = offset + 2 + (((width - 1) >> 3) + 1) << 4
        buf = self._mvfont[offset + 2:next_offset]
        buf = bytearray_at(addressof(buf), len(buf))
        return buf, self.height, width


class MicroFont(BitmapFont):
    def __init__(self, filename, cache_index=True, cache_chars=False):
        from microfont import MicroFont

        self.font = MicroFont(filename, cache_index, cache_chars)
        self.height = self.font.height
        self.baseline = self.mod.baseline
        self.monospaced = self.mod.monospaced

    def measure(self, text):
        width = 0
        for char in text:
            width += self.font.get_ch(char)[2]
        return (0, self.height - self.baseline, width, self.height)

    def bitmap(self, char):
        return self.font.get_ch(char)


class TempeFont(BitmapFont):
    def __init__(self, mod):
        self.font = mod
        self.height = mod.height
        self.baseline = mod.baseline
        self.monospaced = mod.monospaced
        self._mvfont = memoryview(mod._mvfont)
        self._msvp = memoryview(mod._mvsp)
        self._cache = {}

    def measure(self, text):
        width = 0
        for char in text:
            n  = ord(char)
            if n not in self._cache:
                self._cache[n] = self._get_char(n)
            width += self._cache[n][2]
        return (0, self.height - self.baseline, width, self.height)

    def bitmap(self, char):
        n  = ord(char)
        if n not in self._cache:
            self._cache[n] = self._get_char(n)
        return self._cache[n]

    def clear_cache(self):
        self._cache = {}

    def _get_char(self, n):
        offset = bisect16(self._msvp, n, len(self._msvp) >> 2) << 3
        width = self._mvfont[offset] | (self._mvfont[offset + 1] << 8)
        next_offset = offset + 2 + (((width - 1) >> 3) + 1) << 4
        buf = self._mvfont[offset + 2:next_offset]
        buf = bytearray_at(addressof(buf), len(buf))
        return buf, self.height, width

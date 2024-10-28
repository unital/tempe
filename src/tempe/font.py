# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

"""Font ABCs and support for bitmapped fonts."""

from array import array
import framebuf


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

    def measure(self, text):
        width = 0
        for char in text:
            width += self.font.get_ch(char)[2]
        return (0, self.height - self.baseline, width, self.height)

    def bitmap(self, char):
        return self.font.get_ch(char)


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

    def measure(self, text):
        width = 0
        for char in text:
            width += self.font.get_ch(char)[2]
        return (0, self.height - self.baseline, width, self.height)

    def bitmap(self, char):
        return self.font.get_ch(char)

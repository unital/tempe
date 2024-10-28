# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

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


class PyToFont(BitmapFont):
    def __init__(self, mod):
        self.font = mod
        self.height = mod.height()
        self.baseline = mod.baseline()
        self.monospaced = mod.monospaced()
        self.memory = len(mod._font) + len(mod._sparse)

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
        # self.memory = len(mod._font) + len(mod._sparse)

    def measure(self, text):
        width = 0
        for char in text:
            width += self.font.get_ch(char)[2]
        return (0, self.height - self.baseline, width, self.height)

    def bitmap(self, char):
        return self.font.get_ch(char)

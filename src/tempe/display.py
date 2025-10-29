# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

import framebuf


class Display:
    """Abstract base class for Displays"""

    size: tuple[int, int]

    def blit(self, buffer, x, y, w, h):
        raise NotImplementedError


class FrameBufferDisplay(Display):
    """Display that renders into a FrameBuffer."""

    fbuf: framebuf.FrameBuffer
    palette: framebuf.FrameBuffer | None = None

    def __init__(self, fbuf, size, palette=None):
        self.fbuf = fbuf
        self.size = size
        self.palette = palette

    def blit(self, buffer, x, y, w, h):
        if isinstance(buffer, framebuf.FrameBuffer):
            self.fbuf.blit(buffer, x, y, palette=self.palette)
        else:
            self.fbuf.blit((buffer, w, h, framebuf.RGB565), x, y, palette=self.palette)

    def clear(self) -> None:
        memoryview(self.fbuf)[:] = b'\x00'


class FileDisplay(Display):
    """Display that renders raw RGB565 data to a file."""

    def __init__(self, name, size=(320, 240), pixel_size=2):
        self.name = name
        self.size = size
        self.pixel_size = pixel_size
        self._io = None

    def clear(self):
        if self._io is None:
            raise RuntimeError("File is not open")
        self._io.seek(0)
        row = b"\x00" * (self.pixel_size * self.size[0])
        for i in range(self.size[1]):
            self._io.write(row)

    def blit(self, buffer, x, y, w, h):
        cols, rows = self.size
        if x + w > cols or y + h > rows:
            raise ValueError("Buffer too large")
        if self._io is None:
            raise RuntimeError("File is not open")

        # write out a row at a time
        ps = self.pixel_size
        for i in range(h):
            self._io.seek(ps * (cols * (y + i) + x))
            self._io.write(memoryview(buffer)[ps * w * i : ps * w * (i + 1)])

    def __enter__(self):
        if self._io is None:
            try:
                self._io = open(self.name, "r+b")
            except OSError:
                self._io = open(self.name, "wb")

    def __exit__(self, exc_type, exc_value, traceback):
        if self._io is not None:
            self._io.close()
            self._io = None
        if exc_type == OSError and exc_value.errno == 28:
            print("File storage full.\n")

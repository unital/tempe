# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

import framebuf


class Raster:
    """A rectangular buffer that can be drawn on by a surface."""

    def __init__(self, buf, x, y, w, h, stride=None, offset=0, format=framebuf.RGB565):
        stride = stride if stride is not None else w
        self.buf = buf
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.pixel_size = 2
        self.offset = offset
        self.stride = stride
        self.format = format
        self.fbuf = framebuf.FrameBuffer(
            memoryview(buf)[self.pixel_size * offset :], w, h, self.format, stride
        )

    @classmethod
    def from_rect(cls, x, y, w, h):
        buf = bytearray(2 * w * h)
        return cls(buf, x, y, w, h)

    def clip(self, x, y, w, h):
        x1 = max(x, self.x)
        w1 = min(x + w, self.x + self.w) - x1
        y1 = max(y, self.y)
        h1 = min(y + h, self.y + self.h) - y1
        if w1 <= 0 or h1 <= 0:
            return None
        offset = self.offset + self.stride * (y1 - self.y) + (x1 - self.x)
        return Raster(self.buf, x1, y1, w1, h1, self.stride, offset, self.format)

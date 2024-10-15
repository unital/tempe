

class Display:
    """Abstract base class for Displays"""

    def blit(self, buffer, x, y, w, h):
        raise NotImplementedError


class FileDisplay(Display):
    """Display that renders raw RGB565 data to a file."""

    def __init__(self, name, size=(320, 240)):
        self.name = name
        self.size = size
        self._io = None

    def clear(self):
        self._io.seek(0)
        row = b'\x00\x00' * (self.size[0])
        for i in range(self.size[1]):
            self._io.write(row)

    def blit(self, buffer, x, y, w, h):
        cols, rows = self.size
        print(x, w, cols, y, h, rows)
        if x + w > cols or y + h > rows:
            raise ValueError("Buffer too large")
        if self._io is None:
            raise RuntimeError("File is not open")

        # write out a row at a time
        for i in range(h):
            self._io.seek(2 * (cols * (y + i) + x))
            self._io.write(memoryview(buffer)[w * i:w * (i + 1)])

    def __enter__(self):
        if self._io is None:
            self._io = open(self.name, 'r+b')

    def __exit__(self, *args):
        self._io.close()
        self._io = None


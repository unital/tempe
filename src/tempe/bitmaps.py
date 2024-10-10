from .shapes import ColoredGeometry, Shape, BLIT_KEY_RGB565


class BitmapGeometry(Shape):
    """Draw framebuffer bitmaps at points"""

    def __init__(self, surface, geometry, buffers, *, key=None, palette=None, clip=None):
        super().__init__(surface, clip=clip)
        self.geometry = geometry
        self.buffers = buffers
        self.key = None
        self.palette = None

    def update(self, geometry=None, buffers=None):
        if geometry is not None:
            self.geometry = geometry
        if buffers is not None:
            self.buffers = buffers
        super().update()

    def __len__(self):
        return len(self.geometry)

    def __iter__(self):
        yield from zip(self.geometry, self.buffers)

    def draw(self, buffer, x=0, y=0):
        for geometry, buf in self:
            px = geometry[0] - x
            py = geometry[1] - y
            buffer.blit(buffer, px, py, self.key, self.palette)


class ColoredBitmapGeometry(ColoredGeometry):
    """Draw 1-bit framebuffers bitmaps at points in given colors."""

    def __init__(self, surface, geometry, colors, buffers, *, clip=None):
        super().__init__(surface, clip=clip)
        self.geometry = geometry
        self.buffers = buffers
        self.colors = colors

    def update(self, geometry=None, colors=None, buffers=None):
        if geometry is not None:
            self.geometry = geometry
        if buffers is not None:
            self.buffers = buffers
        if colors is not None:
            self.colors = colors
        super().update()

    def __len__(self):
        return len(self.geometry)

    def __iter__(self):
        yield from zip(self.geometry, self.colors, self.buffers)

    def draw(self, buffer, x=0, y=0):
        palette_buf = array('H', [BLIT_KEY_RGB565, 0x0000])
        palette = framebuf.FrameBuffer(palette_buf, 2, 1, framebuf.RGB565)
        for geometry, color, buf in self:
            palette_buf[1] = color
            px = geometry[0] - x
            py = geometry[1] - y
            buffer.blit(buffer, px, py, BLIT_KEY_RGB565, palette)


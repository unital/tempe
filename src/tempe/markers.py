from array import array
import framebuf

from .shapes import ColoredGeometry, BLIT_KEY_RGB565


class Marker:
    PIXEL = 0
    CIRCLE = 1
    SQUARE = 2
    HLINE = 3
    VLINE = 4
    PLUS = 5
    CROSS = 6


class Markers(ColoredGeometry):
    def __init__(self, surface, geometry, colors, markers, *, clip=None):
        super().__init__(surface, geometry, colors, clip=clip)
        self.markers = markers

    def __iter__(self):
        yield from zip(self.geometry, self.colors, self.markers)

    def draw(self, buffer, x=0, y=0):
        palette_buf = array("H", [BLIT_KEY_RGB565, 0x0000])
        palette = framebuf.FrameBuffer(palette_buf, 2, 1, framebuf.RGB565)
        for geometry, color, marker in self:
            px = geometry[0] - x
            py = geometry[1] - y
            size = geometry[2]
            if size < 2 or marker == Marker.PIXEL:
                buffer.pixel(px, py, color)
            elif marker == Marker.CIRCLE:
                buffer.ellipse(px, py, size // 2, size // 2, color, True)
            elif marker == Marker.SQUARE:
                buffer.rect(px - size // 2, py - size // 2, size, size, color, True)
            elif marker == Marker.HLINE:
                buffer.hline(px - size // 2, py, size, color)
            elif marker == Marker.VLINE:
                buffer.vline(px, py - size // 2, size, color)
            elif marker == Marker.PLUS:
                size = 2 * (size // 2) + 1  # odd numper of pixels
                buffer.hline(px - size // 2, py, size, color)
                buffer.vline(px, py - size // 2, size, color)
            elif marker == Marker.CROSS:
                d = 17 * size // 48  # very rough approximation of 1/(2*sqrt(2))
                buffer.line(px - d, py - d, px + d, py + d, color)
                buffer.line(px - d, py + d, px + d, py - d, color)
            elif isinstance(marker, str):
                buffer.text(marker, px - 4, py - 4, color)
            elif isinstance(marker, framebuf.FrameBuffer):
                # assume 1-bit framebuffer - no way to test!
                palette[1] = color
                buffer.blit(marker, px, py, BLIT_KEY_RGB565, palette)

    def update(self, geometry=None, colors=None, markers=None):
        if geometry is not None:
            self.geometry = geometry
        if colors is not None:
            self.colors = colors
        if markers is not None:
            self.markers = markers
        super().update()

from array import array
import framebuf

from .shapes import ColoredGeometry, BLIT_KEY_RGB565


class Text(ColoredGeometry):

    def __init__(self, surface, geometry, colors, texts, *, bold=False, font=None, clip=None):
        super().__init__(surface, geometry, colors, clip=clip)
        self.texts = texts
        self.bold = bold
        self.font = font

    def __iter__(self):
        yield from zip(self.geometry, self.colors, self.texts)

    def draw(self, buffer, x=0, y=0):
        if self.font is None:
            line_height = 10
            for geometry, color, text in self:
                px = geometry[0] - x
                py = geometry[1] - y
                for i, line in enumerate(text.splitlines()):
                    buffer.text(line, px, py + i * line_height, color)
                    if self.bold:
                        buffer.text(line, px + 1, py + i * line_height, color)
        else:
            if callable(self.font.height):
                line_height = self.font.height()
            else:
                line_height = self.font.height
            palette_buf = array('H', [BLIT_KEY_RGB565, 0xffff])
            palette = framebuf.FrameBuffer(palette_buf, 2, 1, framebuf.RGB565)
            for geometry, color, text in self:
                palette_buf[1] = color
                py = geometry[1] - y
                for i, line in enumerate(text.splitlines()):
                    px = geometry[0] - x
                    for char in line:
                        buf, height, width = self.font.get_ch(char)
                        buf = bytearray(buf)
                        fbuf = framebuf.FrameBuffer(buf, width, height, framebuf.MONO_HLSB)
                        buffer.blit(fbuf, px, py, BLIT_KEY_RGB565, palette)
                        if self.bold:
                            px += 1
                            buffer.blit(fbuf, px, py, BLIT_KEY_RGB565, palette)
                        px += width
                    py += line_height


    def update(self, geometry=None, colors=None, texts=None):
        if geometry is not None:
            self.geometry = geometry
        if colors is not None:
            self.colors = colors
        if texts is not None:
            self.texts = texts
        super().update()

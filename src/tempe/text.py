from array import array
import framebuf

from .font import BitmapFont
from .shapes import ColoredGeometry, BLIT_KEY_RGB565


class Text(ColoredGeometry):
    def __init__(
        self, geometry, colors, texts, *, bold=False, font=None, surface=None, clip=None
    ):
        super().__init__(geometry, colors, surface=surface, clip=clip)
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
        elif isinstance(self.font, BitmapFont):
            line_height = self.font.height
            palette_buf = array("H", [BLIT_KEY_RGB565, 0xFFFF])
            palette = framebuf.FrameBuffer(palette_buf, 2, 1, framebuf.RGB565)
            for geometry, color, text in self:
                palette_buf[1] = color
                py = geometry[1] - y
                for i, line in enumerate(text.splitlines()):
                    px = geometry[0] - x
                    for char in line:
                        buf, height, width = self.font.bitmap(char)
                        buf = bytearray(buf)
                        fbuf = framebuf.FrameBuffer(
                            buf, width, height, framebuf.MONO_HLSB
                        )
                        buffer.blit(fbuf, px, py, BLIT_KEY_RGB565, palette)
                        px += width
                    py += line_height
        # elif isinstance(self.font, AlrightFont):
        #     line_height = self.font.height
        #     for geometry, color, text in self:
        #         py = geometry[1] - y
        #         for i, line in enumerate(text.splitlines()):
        #             px = geometry[0] - x
        #             for char in line:
        #                 contours = self.font.contours(char)
        #                 for contour in contours:
        #                     print(contour)
        #                     buffer.poly(px, py, contour, color, True)
        #                 px += self.font.measure(char)[2]
        #             py += line_height

    def update(self, geometry=None, colors=None, texts=None):
        if geometry is not None:
            self.geometry = geometry
        if colors is not None:
            self.colors = colors
        if texts is not None:
            self.texts = texts
        super().update()

    def _bounds(self):
        max_x = -0x7fff
        min_x = 0x7fff
        max_y = -0x7fff
        min_y = 0x7fff
        if self.font is None:
            for geometry, text in zip(self.geometry, self.texts):
                width = 8 * max(len(line) for line in text.splitlines())
                height = 8 * len(text.splitlines())
                max_x = max(max_x, geometry[0] + width)
                min_x = min(min_x, geometry[0])
                max_y = max(max_y, geometry[1] + height)
                min_y = min(min_y, geometry[1])
        else:
            for geometry, text in zip(self.geometry, self.texts):
                width = max(
                    self.font.measure(line)[2]
                    for line in text.splitlines()
                )
                height = self.font.height * len(text.splitlines())
                max_x = max(max_x, geometry[0] + width)
                min_x = min(min_x, geometry[0])
                max_y = max(max_y, geometry[1] + height)
                min_y = min(min_y, geometry[1])

        return (min_x, min_y, max_x - min_x, max_y - min_y)

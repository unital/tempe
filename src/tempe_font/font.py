
# key color is color with only green LSB set
KEY_COLOR = 0b0000000000100000

class Font:

    def wrap(self, text, width, first_indent=0, para_indent=0):
        lines = []
        space = self.width(" ")
        for para in text.splitlines():
            line_width = 0
            indent = first_indent
            line_words = []
            # todo: handle tabs, etc.
            for word in para.split():
                word_width = self.width(word)
                if indent + line_width + word_width > width:
                    # wrap
                    if len(line_words) == 0:
                        # really long first word - do our best
                        line_width += word_width + space
                        line_words.append(word)
                    yield (indent, line_width - space, line_words)
                    line_width = 0
                    line_words = []
                    indent = para_indent
                else:
                    line_width += word_width + space
                    line_words.append(word)
            else:
                # emit incomplete line
                yield (indent, line_width - space, line_words)

    def draw(self, fbuf, text, x, y, color):
        palette = framebuf.FrameBuffer(array('H', [KEY_COLOR, color]))
        for char in text:
            buffer, width, height, left, ascent, advance = self[char]
            char_fbuf = framebuf.FrameBuffer(buffer, width, height, framebuf.MONO_HLSB)
            fbuf.blit(char_fbuf, x + left, y - ascent, key=KEY_COLOR, palette=palette)
            x += advance
        return x

    def draw_wrapped(self, fbuf, text, x, y, w, h, color, line_height, alignment='left', first_indent=0, para_indent=0, para_space=0):
        py = y
        space = self.width(" ")
        for para in text.splitlines():
            py += self.height
            for indent, line_width, words in self.wrap(para, w, first_indent, para_indent):
                px = x + indent
                if alignment == 'left':
                    for word in words:
                        px = self.draw(fbuf, word, px, py)
                        px += space
                elif alignment == 'right':
                    excess = width - indent - line_width
                    px += excess
                    for word in words:
                        px = self.draw(fbuf, word, px, py)
                        px += space
                elif alignment == 'center':
                    excess = width - indent - line_width
                    px += excess // 2
                    for word in words:
                        px = self.draw(fbuf, word, px, py)
                        px += space
                else:
                    excess = width - indent - line_width
                    n_spaces = len(words) - 1
                    for word in words:
                        px = self.draw(fbuf, word, px, py)
                        # TODO: better distribution of excess space
                        if n_spaces > 0:
                            extra = excess // n_spaces
                            px += space + extra
                            excess -= extra
                            n_spaces -= 1
                py += line_height
            py += para_space


class FontToPyFont:

    def __init__(self, mod):
        self.mod = mod
        self.height = mod.height()

    def __getitem__(self, char):
        buffer, height, width = self.mod.get_ch(char)
        return (buffer, width, height, 0, height, width)

    def width(self, text):
        width = sum(self[char][2] for char in text)

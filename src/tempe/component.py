from geometry import RowGeometry


class Style:

    def __init__(self, color, bg_color, font, alignment):
        self.color = color
        self.bg_color = color
        self.font = font
        self.alignment = alignment

    def measure_text(self, text_lines):
        if font is None:
            n_lines = len(text_lines)
            longest_line = max(len(line) for line in text_lines)
            return (0, 0, 8 * longest_line, 8 * n_lines)
        else:


    def

class Component:

    def __init__(self, surface, bounds, style):
        self.surface = surface
        self.bounds = bounds
        self.style =

    def draw(self):
        self.shapes = {}
        self.shapes['background'] = self.surface.rectangles(
            'BACKGROUND',
            RowGeometry.from_lists([self.bounds]),
            [self.style.bg_color],
        )

    def update(self):
        for shape in self.shapes.values():
            shape.update()


class Label(Component):
    """Single-line read-only text field."""

    def __init__(self, surface, bounds, bg_color, text, color, font, alignment=('top', 'left')):
        super().__init__(surface, bounds)
        self.text = text
        self.color = color
        self.font = font
        self.alignment = alignment

    def draw(self):
        self.shapes['text']

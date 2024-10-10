
from .colors import grey_1, grey_2, grey_f
from .geometry import RowGeometry, VertexStrip
from .data_view import DataView, LinearMap, Range

try:
    from .fonts import roboto16
    default_font = roboto16
except ImportError, MemoryError:
    default_font = None


class Style:

    def __init__(self, parent, **kwargs):
        self.parent = parent
        self._style = kwargs

    def __getitem__(self, key):
        if key in self._style:
            return self._style[key]
        elif self.parent is not None:
            return self.parent[key]
        else:
            raise KeyError(key)

    def __delitem__(self, key):
        del self._style[key]

    def __setitem__(self, key, value):
        self._style[key] = value

    def measure_text(self, text_lines):
        font = self["font"]
        if font is None:
            n_lines = len(text_lines)
            longest_line = max(len(line) for line in text_lines)
            return (0, 0, 8 * longest_line, 8 * n_lines)
        else:
            pass


class Component:

    style = Style(None, background_color=grey_f)

    def __init__(self, surface, bounds, **style):
        self.surface = surface
        self.bounds = bounds
        self.style = Style(type(self).style, style)

    def draw(self):
        self.shapes = {}
        if self.style['background_color'] is not None:
            self.shapes['background'] = self.surface.rectangles(
                'BACKGROUND',
                RowGeometry.from_lists([self.bounds]),
                [self.style['background_color']],
                clip=self.bounds,
            )

    def move(self, bounds):
        self.surface.damage(bounds)
        self.surface.damage(self.bounds)
        self.bounds = bounds
        self.shapes['background'].geometry = RowGeometry.from_lists([self.bounds])
        self.shapes['background'].clip = self.bounds
        self.update()

    def update(self):
        self.shapes['background'].colors = [self.style['background_color']]
        for shape in self.shapes.values():
            shape.update()


class Label(Component):
    """Single-line read-only text field."""

    style = Style(Component.style, background_color=None, font=default_font, color=grey_2, text_alignment=('top', 'left'))

    def __init__(self, surface, bounds, value, format=str, **kwargs):
        super().__init__(surface, bounds, **kwargs)
        self.value = value
        self.format = format

    def draw(self):
        super().draw()
        self.shapes['text'] = self.surface.text(
            'DRAWING',
            RowGeometry.from_lists([self.bounds[:2]]),
            [self.format(self.value)],
            [self.style['color']],
            font=self.style['font'],
            clip=self.bounds,
        )

    def move(self, bounds):
        self.shapes['text'].geometry = RowGeometry.from_lists([bounds[:2]])
        self.shapes['text'].clip = bounds
        super().move(bounds)

    def update(self):
        self.shapes['text'].texts = self.format(self.value)
        self.shapes['text'].colors[0] = self.style['color']
        self.shapes['text'].font = self.style['font']
        super().update()


class LinePlot(Component):
    """Single line plot."""

    style = Style(Component.style, background_color=grey_f)

    def __init__(self, surface, bounds, values, index=None, colors=(grey_2,), value_range=None, index_range=None, orientation='horizontal', x_origin='left', y_origin='bottom', **kwargs):
        super().__init__(surface, bounds, **kwargs)
        if not isinstance(values, DataView):
            values = DataView(values)
        self.values = values
        if value_range is None:
            value_range = (min(values), max(values))
        self.value_range = value_range
        if index is None:
            index = Range(len(values))
            index_range = (min(index), max(index))
        self.index = index
        self.index_range = index_range
        self.colors = colors

    def map_xy(self):
        normalized_values = (self.values - self.value_range[0])/(self.value_range[1] - self.value_range[0])
        normalized_index = (self.index - self.index_range[0])/(self.index_range[1] - self.index_range[0])
        x, y, w, h = self.bounds
        if self.orientation == 'horizontal':
            y_source = normalized_values
            x_source = normalized_index
        else:
            y_source = normalized_index
            x_source = normalized_values

        vertex_strip = array('h', bytearray(8 * len(self.values)))
        if y_origin = 'bottom':
            vertex_strip[1::2] = (y + h * y_source)
        else:
            vertex_strip[1::2] = (y + h - h * y_source)
        if x_origin = 'left':
            vertex_strip[::2] = (x + w * x_origin)
        else:
            vertex_strip[::2] = (x + w - w * x_origin)

        return vertex_strip

    def draw(self):
        super().draw()
        vertices = self.map_xy()
        self.shapes['lines'] = self.surface.lines(
            'DRAWING',
            LineStrip(vertices),
            self.colors,
            clip=self.bounds,
        )

    def move(self, bounds):
        self.shapes['lines'].clip = bounds
        super().move(bounds)

    def update(self):
        self.shapes['lines'].geometry.geometry = self.map_xy()
        self.shapes['lines'].colors = self.colors
        super().update()

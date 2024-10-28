# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

from array import array

from .colors import grey_1, grey_2, grey_e, grey_f
from .geometry import RowGeometry, StripGeometry, ColumnGeometry
from .data_view import DataView, Range
from .markers import Marker

try:
    from .fonts import roboto16

    default_font = roboto16
except ImportError:
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

    style = Style(None, background_color=grey_e)

    def __init__(self, surface, bounds, **style):
        self.surface = surface
        self.bounds = bounds
        self.style = Style(type(self).style, **style)
        self.shapes = {}

    def draw(self):
        if self.style["background_color"] is not None:
            self.shapes["background"] = self.surface.rects(
                "BACKGROUND",
                RowGeometry.from_lists([self.bounds]),
                [self.style["background_color"]],
                clip=self.bounds,
            )

    def move(self, bounds):
        self.surface.damage(bounds)
        self.surface.damage(self.bounds)
        self.bounds = bounds
        self.shapes["background"].geometry = RowGeometry.from_lists([self.bounds])
        self.shapes["background"].clip = self.bounds
        self.update()

    def update(self):
        if "background" in self.shapes:
            if self.style["background_color"] is not None:
                self.shapes["background"].colors = [self.style["background_color"]]
            else:
                del self.shapes["background"]
        elif self.style["background_color"] is not None:
            self.draw()
        for shape in self.shapes.values():
            shape.update()


class Label(Component):
    """Single-line read-only text field."""

    style = Style(
        Component.style,
        background_color=None,
        font=default_font,
        color=grey_2,
        text_alignment=("top", "left"),
    )

    def __init__(self, surface, bounds, value, format=str, **kwargs):
        super().__init__(surface, bounds, **kwargs)
        self.value = value
        self.format = format

    def draw(self):
        super().draw()
        self.shapes["text"] = self.surface.text(
            "DRAWING",
            RowGeometry.from_lists([self.bounds[:2]]),
            [self.style["color"]],
            [self.format(self.value)],
            font=self.style["font"],
            clip=self.bounds,
        )

    def move(self, bounds):
        self.shapes["text"].geometry = RowGeometry.from_lists([bounds[:2]])
        self.shapes["text"].clip = bounds
        super().move(bounds)

    def update(self):
        if "text" not in self.shapes:
            self.draw()
        else:
            self.shapes["text"].texts = [self.format(self.value)]
            self.shapes["text"].colors[0] = self.style["color"]
            self.shapes["text"].font = self.style["font"]
        super().update()


# TODO: Refactor these plot classes into a more refined approach


class LinePlot(Component):
    """Single line plot."""

    style = Style(Component.style, background_color=grey_f)

    def __init__(
        self,
        surface,
        bounds,
        values,
        index=None,
        colors=grey_2,
        value_range=None,
        index_range=None,
        orientation="horizontal",
        x_origin="left",
        y_origin="bottom",
        **kwargs
    ):
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
        if not isinstance(index, DataView):
            index = DataView(index)
        self.index = index
        self.index_range = index_range
        if not isinstance(colors, DataView):
            colors = DataView.create(colors)
        self.colors = colors
        self.orientation = orientation
        self.x_origin = x_origin
        self.y_origin = y_origin

    def map_xy(self):
        vertex_strip = array("h", bytearray(4 * len(self.values)))
        for i, (index, value) in enumerate(zip(self.index, self.values)):
            x = self.bounds[0] + self.bounds[2] * (index - self.index_range[0]) / (
                self.index_range[1] - self.index_range[0]
            )
            y = (
                self.bounds[1]
                + self.bounds[3]
                - self.bounds[3]
                * (value - self.value_range[0])
                / (self.value_range[1] - self.value_range[0])
            )
            vertex_strip[2 * i] = int(x)
            vertex_strip[2 * i + 1] = int(y)

        return vertex_strip

    def draw(self):
        super().draw()
        vertices = self.map_xy()
        self.shapes["lines"] = self.surface.lines(
            "DRAWING",
            LineStrip(vertices),
            self.colors,
            clip=self.bounds,
        )

    def move(self, bounds):
        self.shapes["lines"].clip = bounds
        super().move(bounds)

    def update(self):
        if "lines" not in self.shapes:
            self.draw()
        else:
            self.shapes["lines"].geometry.geometry = self.map_xy()
            self.shapes["lines"].colors = self.colors
        super().update()


class ScatterPlot(Component):
    """Single scatter plot."""

    style = Style(Component.style, background_color=grey_f)

    def __init__(
        self,
        surface,
        bounds,
        values,
        index=None,
        sizes=1,
        colors=grey_2,
        markers=Marker.VLINE,
        value_range=None,
        index_range=None,
        orientation="horizontal",
        x_origin="left",
        y_origin="bottom",
        **kwargs
    ):
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
        if not isinstance(index, DataView):
            index = DataView(index)
        self.index = index
        self.index_range = index_range
        if not isinstance(sizes, DataView):
            sizes = DataView.create(sizes)
        self.sizes = sizes
        if not isinstance(colors, DataView):
            colors = DataView.create(colors)
        self.colors = colors
        if not isinstance(markers, DataView):
            markers = DataView.create(markers)
        self.markers = markers
        self.orientation = orientation
        self.x_origin = x_origin
        self.y_origin = y_origin

    def map_xy(self):
        xs = array("h", bytearray(2 * len(self.values)))
        ys = array("h", bytearray(2 * len(self.values)))
        for i, (index, value) in enumerate(zip(self.index, self.values)):
            x = self.bounds[0] + self.bounds[2] * (index - self.index_range[0]) / (
                self.index_range[1] - self.index_range[0]
            )
            y = (
                self.bounds[1]
                + self.bounds[3]
                - self.bounds[3]
                * (value - self.value_range[0])
                / (self.value_range[1] - self.value_range[0])
            )
            xs[i] = int(x)
            ys[i] = int(y)

        return xs, ys, self.sizes

    def draw(self):
        super().draw()
        xs, ys, sizes = self.map_xy()
        self.shapes["markers"] = self.surface.points(
            "DRAWING",
            ColumnGeometry([xs, ys, sizes]),
            self.colors,
            self.markers,
            clip=self.bounds,
        )

    def move(self, bounds):
        self.shapes["markers"].clip = bounds
        super().move(bounds)

    def update(self):
        if "markers" not in self.shapes:
            self.draw()
        else:
            self.shapes["markers"].geometry.geometry = self.map_xy()
            self.shapes["markers"].colors = self.colors
            self.shapes["markers"].markers = self.markers
        super().update()


class BarPlot(Component):
    """Single bar plot."""

    style = Style(Component.style, background_color=grey_f)

    def __init__(
        self,
        surface,
        bounds,
        values,
        index=None,
        sizes=1,
        colors=grey_2,
        markers=Marker.VLINE,
        value_range=None,
        index_range=None,
        orientation="horizontal",
        x_origin="left",
        y_origin="bottom",
        **kwargs
    ):
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
        if not isinstance(index, DataView):
            index = DataView(index)
        self.index = index
        self.index_range = index_range
        if not isinstance(sizes, DataView):
            sizes = DataView.create(sizes)
        self.sizes = sizes
        if not isinstance(colors, DataView):
            colors = DataView.create(colors)
        self.colors = colors
        if not isinstance(markers, DataView):
            markers = DataView.create(markers)
        self.markers = markers
        self.orientation = orientation
        self.x_origin = x_origin
        self.y_origin = y_origin

    def map_xy(self):
        xs = array("h", bytearray(2 * len(self.values)))
        hs = array("h", bytearray(2 * len(self.values)))
        for i, (index, value) in enumerate(zip(self.index, self.values)):
            x = self.bounds[0] + self.bounds[2] * (index - self.index_range[0]) / (
                self.index_range[1] - self.index_range[0]
            )
            h = (
                -self.bounds[3]
                * (value - self.value_range[0])
                / (self.value_range[1] - self.value_range[0])
            )
            xs[i] = int(x)
            hs[i] = int(h)

        return (
            xs,
            DataView.create(self.bounds[1] + self.bounds[3]),
            DataView.create(3),
            hs,
        )

    def draw(self):
        super().draw()
        geometry = self.map_xy()
        self.shapes["rects"] = self.surface.rects(
            "DRAWING",
            ColumnGeometry(geometry),
            self.colors,
            clip=self.bounds,
        )

    def move(self, bounds):
        self.shapes["rects"].clip = bounds
        super().move(bounds)

    def update(self):
        if "rects" not in self.shapes:
            self.draw()
        else:
            self.shapes["rects"].geometry.geometry = self.map_xy()
            self.shapes["rects"].colors = self.colors
        super().update()

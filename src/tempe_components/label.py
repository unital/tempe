# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

from tempe.colors import grey_4, grey_6, grey_a, grey_d
from tempe.surface import DRAWING
from tempe.text import Text, CENTER

from .component import Component, component_style
from .observable import Field, undefined, is_undefined
from .style import StateColor, Style


label_style = Style(
    parent=component_style,
    background=StateColor(enabled=grey_d),
    text=StateColor(enabled=grey_4),
    radius=8,
)

class Label(Component):

    style = Field(label_style, cls=Style)
    text = Field("", cls=str)

    _anchor = (0, 0)
    _text_shape = None

    @property
    def text_color(self):
        if self.style.text is None:
            return None
        else:
            return self.style.text[self.state]

    @property
    def font(self):
        return self.style.font

    def _update_text(self):
        if self.style.text is not None:
            text_color = self.style.text[self.state]
        else:
            text_color = None
        if text_color is None:
            if self._text_shape is not None:
                self.surface.remove_shape(DRAWING, self._text_shape)
                self._text_shape = None
        elif self._text_shape is None:
            self._text_shape = Text(
                [self._anchor],
                [text_color],
                [self.text],
                [(CENTER, CENTER)],
                font=self.font,
            )
            self.surface.add_shape(DRAWING, self._text_shape)
        else:
            self._text_shape.update(
                geometry=[self._anchor],
                colors=[text_color],
                texts=[self.text],
                font=self.font,
            )


    def update(
        self,
        update=None,
        **kwargs
    ):
        super().update(update)
        self._anchor = (
            self.box.bounds[0] + self.box.bounds[2] // 2,
            self.box.bounds[1] + self.box.bounds[3] // 2,
        )
        self._update_text()


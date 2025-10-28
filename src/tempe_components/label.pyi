# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

from typing import Final

from tempe.colors import rgb565
from tempe.font import AbstractFont

from .component import Component, component_style
from .observable import Field, undefined
from .style import StateColor, Style


label_style: Final[Style]


class Label(Component):

    text = Field("", cls=str)

    _anchor = (0, 0)
    _text_shape = None

    @property
    def text_color(self) -> rgb565: ...

    @property
    def font(self) -> AbstractFont: ...

    def _update_text(self) -> None: ...

    def update(self, update: dict[str, object] | None = None, /, **kwargs) -> None: ...

# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

import asyncio

from tempe.colors import grey_e, grey_a
from tempe.shapes import RoundedRectangles
from tempe.surface import Surface, BACKGROUND, OVERLAY

from .observable import Observable, Field, undefined
from .style import Style, StateColor, ENABLED


component_style = Style(
    parent=None,
    background=StateColor(enabled=grey_e)
)


class Box(Observable):
    x: int = Field(cls=int)
    y: int = Field(cls=int)
    content_width: int = Field(cls=int)
    content_height: int = Field(cls=int)
    pad_top: int = Field(1, cls=int)
    pad_bottom: int = Field(1, cls=int)
    pad_left: int = Field(1, cls=int)
    pad_right: int = Field(1, cls=int)
    margin_top: int = Field(0, cls=int)
    margin_bottom: int = Field(0, cls=int)
    margin_left: int = Field(0, cls=int)
    margin_right: int = Field(0, cls=int)

    @property
    def bounds(self):
        return (
            self.x + self.margin_left,
            self.y + self.margin_top,
            self.content_width + self.pad_left + self.pad_right,
            self.content_height + self.pad_top + self.pad_bottom,
        )

    @property
    def shadow_bounds(self):
        return (
            self.x + self.margin_left - 1,
            self.y + self.margin_top + 1,
            self.content_width + self.pad_left + self.pad_right + 2,
            self.content_height + self.pad_top + self.pad_bottom,
        )

    @property
    def content_bounds(self):
        return (
            self.x + self.margin_left + self.pad_left,
            self.y + self.margin_top + self.pad_top,
            self.content_width,
            self.content_height,
        )


class Component(Observable):

    surface: "Surface"

    box: Box

    style = Field(component_style, cls=Style)

    state = Field(ENABLED, cls=str)

    _background_shape = None
    _shadow_shape = None
    _border_shape = None

    def __init__(self, surface, **kwargs):
        self.surface = surface
        super().__init__(**kwargs)

    def _update_background_shape(self):
        if self.style.background is None:
            background = None
        else:
            background = self.style.background[self.state]
        if background is None:
            if self._background_shape is not None:
                if self._shadow_shape is not None:
                    self.surface.remove_shape(BACKGROUND, self._shadow_shape)
                self.surface.remove_shape(BACKGROUND, self._background_shape)
                self._background_shape = None
        elif self._background_shape is None:
            if self.style.shadow is not None:
                self._shadow_shape = RoundedRectangles(
                    [self.box.shadow_bounds],
                    [self.style.shadow[self.state]],
                    radius=self.style.radius + 1,
                    fill=True,
                    fill_center=False,
                )
                self.surface.add_shape(BACKGROUND, self._shadow_shape)
            self._background_shape = RoundedRectangles(
                [self.box.bounds],
                [background],
                radius=self.style.radius,
                fill=True,
            )
            self.surface.add_shape(BACKGROUND, self._background_shape)
        else:
            if self.style.shadow is None:
                if self._shadow_shape is not None:
                    self.surface.remove_shape(BACKGROUND, self._shadow_shape)
                    self._shadow_shape = None
            elif self._shadow_shape is None:
                self._shadow_shape = RoundedRectangles(
                    [self.box.shadow_bounds],
                    [self.style.shadow[self.state]],
                    radius=self.style.radius + 1,
                    fill=True,
                    fill_center=False,
                )
                # Ensure proper layering
                self.surface.remove_shape(BACKGROUND, self._background_shape)
                self.surface.add_shape(BACKGROUND, self._shadow_shape)
                self.surface.add_shape(BACKGROUND, self._background_shape)
            else:
                self._shadow_shape.update(
                    geometry=[self.box.shadow_bounds],
                    colors=[self.style.shadow[self.state]],
                    radius=self.style.radius,
                )

            self._background_shape.update(
                geometry=[self.box.bounds],
                colors=[background],
                radius=self.style.radius,
            )

    def _update_border_shape(self):
        if self.style.border is None:
            border = None
        else:
            border = self.style.border[self.state]
        if border is None:
            if self._border_shape is not None:
                self.surface.remove_shape(OVERLAY, self._border_shape)
                self._border_shape = None
        elif self._border_shape is None:
            self._border_shape = RoundedRectangles(
                [self.box.bounds],
                [border],
                radius=self.style.radius,
                fill=False,
            )
            self.surface.add_shape(OVERLAY, self._border_shape)
        else:
            self._border_shape.update(
                geometry=[self.box.bounds],
                colors=[border],
                radius=self.style.radius,
            )

    def update(
        self, update=None, **kwargs
    ):
        super().update(update, **kwargs)
        self._update_background_shape()
        self._update_border_shape()

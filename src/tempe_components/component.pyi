# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

from typing import Final, dataclass_transform

from tempe.shapes import RoundedRectangles, rectangle
from tempe.surface import Surface

from .observable import Observable, Undefined, undefined
from .style import Style, State, ENABLED


component_style: Final[Style]


class Box(Observable):
    """Geometry for UI components.

    This is a simplified version of the standard HTML box model: each box has
    content which has a width and a height, internal padding, and external
    margin.
    """

    #: Horizontal position
    x: int

    #: Vertical position
    y: int

    #: Width of box content
    content_width: int

    #: Height of box content
    content_height: int

    #: Amount of top padding inside border but outside content
    pad_top: int = 0

    #: Amount of bottom padding inside border but outside content
    pad_bottom: int = 0

    #: Amount of left padding inside border but outside content
    pad_left: int = 0

    #: Amount of right padding inside border but outside content
    pad_right: int = 0

    #: Amount of top margin outside border
    margin_top: int = 0

    #: Amount of bottom margin outside border
    margin_bottom: int = 0

    #: Amount of left margin outside border
    margin_left: int = 0

    #: Amount of right margin outside border
    margin_right: int = 0

    @property
    def bounds(self) -> rectangle:
        """Bounding rectangle of border and background."""

    @property
    def shadow_bounds(self) -> rectangle:
        """Bounding rectangle of drop shadow."""

    @property
    def content_bounds(self) -> rectangle:
        """Bounding rectangle of content."""


class Component(Observable):
    """Base class for UI elements."""

    #: The surface to which the component's shapes will be added.
    surface: Surface

    #: The box geometry of the component.
    box: Box

    #: The style for the component. There is a default component style for each class.
    style: Style = component_style

    #: The current activation state of the component, used for color selection.
    state: State = ENABLED

    _background_shape: RoundedRectangles | None = None

    _border_shape: RoundedRectangles | None = None

    def _update_background_shape(self) -> None: ...

    def _update_border_shape(self) -> None: ...

    def update(self, update: dict[str, object] | None = None, /, **kwargs) -> None: ...


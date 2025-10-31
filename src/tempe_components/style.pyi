# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

from typing import Final, Literal, Callable, overload

from tempe.colors import normalize_color, grey_4, grey_c, grey_e, grey_a, color, rgb565
from tempe.font import AbstractFont

from .observable import Observable, Field, field


State = Literal["active", "enabled", "disabled"]
ACTIVE: Final[State] = "active"
ENABLED: Final[State] = "enabled"
DISABLED: Final[State] = "disabled"
STATES: Final[tuple[State, ...]] = (ENABLED, DISABLED, ACTIVE)


class StateColorField(Field[color, rgb565, StateColor]):
    """A Field subclass for storing color information."""

    @overload
    def __init__(
            self,
            default: rgb565,
            *,
            adapter: Callable[[color], rgb565] = normalize_color,
        ) -> None: ...

    @overload
    def __init__(
            self,
            *,
            default_factory: Callable[[], rgb565] | None = None,
            adapter: Callable[[color], rgb565] = normalize_color,
        ) -> None: ...

    def default_factory(self, obj: StateColor) -> rgb565: ...


class StateColor(Observable):
    """Color information for different states of a UI component.

    This object holds information about how a particular aspect of a component
    changes color as the component's state changes.
    """

    enabled = StateColorField()
    disabled = StateColorField()
    active = StateColorField()

    def __init__(self, **kwargs: color): ...

    def __getitem__(self, state: State) -> rgb565: ...

    def __setitem__(self, state: State, value: color) -> None: ...


class Style(Observable):
    """Styling information for Ui components.

    This object holds styling information, such as color selections for
    different parts of the component, font information, and box shape
    parameters.

    Styles can have a parent style, and inherit non-specified values from
    that and will react to changes in their parent, signalling classes which
    use them that they may have had values updated.
    """

    parent: Style | None = None

    background: StateColor | None = None
    border: StateColor | None = None
    shadow: StateColor | None = None
    radius: int = 0
    text: StateColor | None = None
    font: AbstractFont | None = None

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

    enabled = StateColorField()
    disabled = StateColorField()
    active = StateColorField()

    def __init__(self, **kwargs: color): ...

    def __getitem__(self, state: State) -> rgb565: ...

    def __setitem__(self, state: State, value: color) -> None: ...


class Style(Observable):

    parent: Style | None = None

    background: StateColor | None = None
    border: StateColor | None = None
    radius: int = 0
    text: StateColor | None = None
    font: AbstractFont | None = None

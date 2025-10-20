# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

from tempe.colors import normalize_color, grey_4, grey_c, grey_e, grey_a
from tempe.font import AbstractFont

from .observable import Observable, Field, field, undefined


ACTIVE = const("active")
ENABLED = const("enabled")
DISABLED = const("disabled")
STATES = const((ENABLED, DISABLED, ACTIVE))


class StateColorField(Field):

    def __init__(
            self,
            default=undefined,
            default_factory=None,
            adapter=normalize_color,
        ):
        if default_factory is None:
            super().__init__(
                default=default,
                adapter=adapter,
                cls=int,
            )
        else:
            super().__init__(
                default_factory=default_factory,
                adapter=adapter,
                cls=int,
            )

    def default_factory(self, obj):
        if self.name is not 'enabled':
            return obj.enabled
        return super().default_factory(obj)


class StateColor(Observable):

    enabled = StateColorField()
    disabled = StateColorField()
    active = StateColorField()

    def __init__(self, enabled, **kwargs):
        kwargs[ENABLED] = enabled
        super().__init__(**kwargs)

    def __getitem__(self, state):
        return getattr(self, state)

    def __setitem__(self, state, value):
        self.update({state: value})


class Style(Observable):

    parent = Field(None)

    background = Field(cls=StateColor)
    border = Field(cls=StateColor)
    radius = Field(adapter=abs, cls=int)
    text = Field(cls=StateColor)
    font = Field(None, cls=AbstractFont)

# fix need for recursive definition
Style.parent.cls = Style

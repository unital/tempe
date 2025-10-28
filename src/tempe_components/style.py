# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

from tempe.colors import normalize_color, grey_4, grey_c, grey_e, grey_a
from tempe.font import AbstractFont

from .observable import Observable, Field, field, undefined, is_undefined


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


class StyleField(Field):

    def __get__(self, obj, cls=None):
        if not hasattr(obj, self.stored_name):
            try:
                return getattr(obj.parent, self.name)
            except AttributeError:
                default = self.default_factory(obj)
                if not is_undefined(default):
                    setattr(obj, self.stored_name, default)
        try:
            return getattr(obj, self.stored_name)
        except AttributeError:
            raise AttributeError(self.name)


class Style(Observable):

    parent = Field(None)

    background = StyleField(None, cls=StateColor)
    border = StyleField(None, cls=StateColor)
    shadow = StyleField(None, cls=StateColor)
    radius = StyleField(0, adapter=abs, cls=int)
    text = StyleField(None, cls=StateColor)
    font = StyleField(None, cls=AbstractFont)

# fix need for recursive definition
Style.parent.cls = Style

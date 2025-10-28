# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

import asyncio
from typing import Callable, Any, ClassVar, ParamSpec, dataclass_transform, overload

class Undefined:
    pass

undefined = Undefined()

def is_undefined(obj: Any) -> bool: ...

params = ParamSpec("params")


@dataclass_transform(eq_default=False, field_specifiers=(Field, field,))
class Updatable:
    """A dataclass-like class that allows atomic updates of attributes."""

    _obs_fields: ClassVar[dict[str, Field]] = {}

    def update(
        self,
        update: dict[str, object] | None = None,
        /,
        **kwargs: object,
    ) -> None: ...


class Observable(Updatable):
    """A dataclass-like class that fires an asyncio.Event when updated."""

    _obs_fields: ClassVar[dict[str, Field]] = {}

    @property
    def updated(self) -> asyncio.Event: ...

    def close(self) -> None: ...


async def aobserve(observable: Observable, callback: Callable[[Observable], None]) -> None: ...

def observe(observable: Observable, callback: Callable[[Observable], None]) -> asyncio.Task: ...


class Field[Accepts, Stores, Target: Updatable]:
    """A dataclass-like field that can validate and adapt values on setting."""

    name: str

    stored_name: str

    adapter: Callable[[Accepts], Stores] | None

    cls: type[Stores] | None

    @overload
    def __init__(
            self,
            default: Stores,
            *,
            adapter: Callable[[Accepts], Stores] | None = None,
            cls: type[Stores] | None = None,
        ) -> None: ...

    @overload
    def __init__(
            self,
            *,
            default_factory: Callable[[], Stores] | None = None,
            adapter: Callable[[Accepts], Stores] | None = None,
            cls: type[Stores] | None = None,
        ) -> None: ...

    def __set_name__(self, cls: type[Target], name: str) -> None: ...

    @overload
    def __get__(self, obj: Target, cls: type[Target] | None = None) -> Stores: ...

    @overload
    def __get__(self, obj: None, cls: type[Target]) -> Stores: ...

    def __set__(self, obj: Target, value: Accepts) -> None: ...

    def default_factory(self, obj: Target) -> Stores | Undefined: ...

    def default(self) -> Stores | Undefined: ...

    def validator(self, obj: Target, value: Accepts) -> Stores: ...


@overload
def field[Accepts, Stores](
        default: Stores,
        adapter: Callable[[Accepts], Stores] | None = None,
        cls: type[Stores] | None = None,
    ) -> Stores: ...

@overload
def field[Accepts, Stores](
        default_factory: Callable[[], Stores] | None = None,
        adapter: Callable[[Accepts], Stores] | None = None,
        cls: type[Stores] | None = None,
    ) -> Stores: ...


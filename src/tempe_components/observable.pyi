import asyncio
from typing import Callable, Any, ClassVar, ParamSpec, dataclass_transform, overload

class Undefined:
    pass

undefined = Undefined()

def is_undefined(obj: Any) -> bool: ...

params = ParamSpec("params")


@dataclass_transform(eq_default=False, field_specifiers=(Field, field,))
class Updatable:

    _obs_fields: ClassVar[dict[str, Field]] = {}
    strict: ClassVar[bool] = False

    def update(
        self,
        update: dict[str, object] | None = None,
        **kwargs: object,
    ) -> None: ...


class Observable(Updatable):

    _obs_fields: ClassVar[dict[str, Field]] = {}

    @property
    def updated(self) -> asyncio.Event: ...

    def close(self) -> None: ...


async def aobserve(observable: Observable, callback: Callable[[], None]) -> None: ...


class Field[Accepts, Stores]:

    name: str

    stored_name: str

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

    def __set_name__(self, cls: type[Updatable], name: str) -> None: ...

    @overload
    def __get__(self, obj: Updatable, cls: type[Updatable] | None = None) -> Stores: ...

    @overload
    def __get__(self, obj: None, cls: type[Updatable]) -> Stores: ...

    def __set__(self, obj: Updatable, value: Accepts) -> None: ...

    def default_factory(self, obj: Updatable) -> Stores | Undefined: ...

    def default(self, obj: Updatable) -> Stores | Undefined: ...

    def validator(self, obj: Updatable, value: Accepts) -> Stores: ...


@overload
def field[Accepts, Stores](
        default: Stores,
        adapter: Callable[[Accepts], Stores] | None = None,
        cls: type[Stores] | None = None,
    ) -> Field[Accepts, Stores]: ...

@overload
def field[Accepts, Stores](
        default_factory: Callable[[], Stores] | None = None,
        adapter: Callable[[Accepts], Stores] | None = None,
        cls: type[Stores] | None = None,
    ) -> Field[Accepts, Stores]: ...


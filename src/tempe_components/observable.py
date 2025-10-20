# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

import asyncio

class Undefined:
    pass

undefined = Undefined()

def is_undefined(obj):
    return isinstance(obj, Undefined)


class Updatable:

    _obs_fields = {}

    def __init__(self, **kwargs):
        # Hack to work around lack of PEP 487 support.
        if not '_obs_fields' in self.__class__.__dict__:
            self.__class__.__init_subclass__()
        self.update(kwargs)

    @classmethod
    def __init_subclass__(cls):
        fields = {}
        for base in cls.__bases__:
            fields.update(getattr(base, '_obs_fields', {}))
        cls._obs_fields = fields

    def update(self, update=None, **kwargs):
        if update is None:
            update = {}
        update.update(kwargs)
        for name, value in update.items():
            field = self.__class__._obs_fields.get(name, None)
            if field is not None:
                if is_undefined(value):
                    delattr(self, field.stored_name)
                else:
                    setattr(self, field.stored_name, value)
            else:
                if is_undefined(value):
                    delattr(self, name)
                else:
                    setattr(self, name, value)

        self.validate(update)

    def validate(self, update):
        pass


class Observable(Updatable):

    _obs_fields = {}

    def __init__(self, **kwargs):
        self.updated = asyncio.Event()
        self._update_tasks = {}
        super().__init__(**kwargs)

    def close(self):
        for task in self._update_tasks.values():
            task.cancel()

    def _attr_updated(self, observable):
        self.updated.set()
        self.updated.clear()

    def update(self, update=None, **kwargs):
        if update is None:
            update = {}
        update.update(kwargs)
        for name, value in update.items():
            if name in self._update_tasks:
                self._update_tasks[name].cancel()
                del self._update_tasks[name]

        super().update(update)

        for name in update:
            value = self.__dict__[name]
            if isinstance(value, Observable):
                self._update_tasks[name] = observe(value, self._attr_updated)

        self.updated.set()
        self.updated.clear()


async def aobserve(observable, callback):
    while True:
        try:
            await observable.updated.wait()
        except asyncio.CancelledError:
            break
        callback(observable)


def observe(observable, callback):
    return asyncio.create_task(aobserve(observable, callback))


class Field:

    prefix = '_'

    def __init__(self, default=undefined, default_factory=None, adapter=None, cls=None):
        self._default = default
        self._default_factory = default_factory
        self.adapter = adapter
        self.cls = cls

    def __set_name__(self, cls, name):
        # Hack to work around lack of PEP 487 support.
        if not '_obs_fields' in cls.__dict__:
            cls.__init_subclass__()
        cls._obs_fields[name] = self
        self.name = name
        self.stored_name = self.prefix + name

    def __get__(self, obj, cls=None):
        if not hasattr(obj, self.stored_name):
            default = self.default_factory(obj)
            if not is_undefined(default):
                setattr(obj, self.stored_name, default)
        try:
            return getattr(obj, self.stored_name)
        except AttributeError:
            raise AttributeError(self.name)

    def __set__(self, obj, value):
        value = self.validator(obj, value)
        obj.update({self.name: value})

    def default_factory(self, obj):
        if is_undefined(self._default) and self._default_factory is not None:
            return self._default_factory()
        else:
            return self.default()

    def default(self):
        return self._default

    def validator(self, obj, value):
        if self.adapter is not None:
            try:
                value = self.adapter(value)
            except Exception:
                raise ValueError(f"Error adapting value {value}.")
        if self.cls is not None and not isinstance(value, self.cls):
            raise ValueError(f"Invalid value {value}, should be of type {self.cls}")
        return value


def field(default=undefined, default_factory=None, adapter=None, cls=None):
    return Field(default=default, default_factory=default_factory, adapter=adapter, cls=cls)

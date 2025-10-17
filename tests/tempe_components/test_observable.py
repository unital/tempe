# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

import asyncio
import unittest

from tempe_components.observable import Field, Observable, Updatable, field, undefined


class TestUpdatable(unittest.TestCase):

    def test_base(self):
        data = Updatable()
        data.update(test=1)

        self.assertEqual(data.test, 1)

    def test_base_update_args(self):
        data = Updatable()
        data.update({'test_1': 1}, test_2=2)

        self.assertEqual(data.test_1, 1)
        self.assertEqual(data.test_2, 2)

    def test_base_init(self):
        data = Updatable(test=1)

        self.assertEqual(data.test, 1)

    def test_simple_subclass(self):

        class UpdatableSimpleSub(Updatable):
            test = 0

        data = UpdatableSimpleSub()
        data.update(test=1)

        self.assertEqual(data.test, 1)

    def test_simple_subclass_init(self):

        class UpdatableSimpleSub(Updatable):
            test = 0

        data = UpdatableSimpleSub(test=1)

        self.assertEqual(data.test, 1)

    def test_simple_subclass_init_args(self):

        class UpdatableFieldSub(Updatable):
            test = 0

        with self.assertRaises(TypeError):
            UpdatableFieldSub(1)

    def test_field_subclass(self):

        class UpdatableFieldSub(Updatable):
            test = Field()

        self.assertIn("_obs_fields", UpdatableFieldSub.__dict__)
        self.assertEqual(
            UpdatableFieldSub._obs_fields,
            {"test": UpdatableFieldSub.test}
        )


        data = UpdatableFieldSub()
        data.update(test=1)

        self.assertEqual(data.test, 1)

        data.test = 2

        self.assertEqual(data.test, 2)

    def test_field_subclass_init(self):

        class UpdatableFieldSub(Updatable):
            test = Field()

        data = UpdatableFieldSub(test=1)

        self.assertEqual(data.test, 1)

    def test_field_subclass_init_args(self):

        class UpdatableFieldSub(Updatable):
            test = Field()

        with self.assertRaises(TypeError):
            UpdatableFieldSub(1)

    def test_validate(self):

        class ValidatingUpdatable(Updatable):
            a = Field(0)
            b = Field(0)

            def validate(self, update):
                if self.b < self.a:
                    self.update(a=self.b, b=self.a)

        data = ValidatingUpdatable()
        data.update(a=10, b=1)

        self.assertEqual(data.a, 1)
        self.assertEqual(data.b, 10)


class TestObservable(unittest.TestCase):

    async def update_waiter(self, data, callback):
        await data.updated.wait()
        callback(data)

    async def update_later(self, data, update):
        await asyncio.sleep(0.01)
        data.update(update)

    def test_base(self):
        data = Observable()

        try:
            data.update(test=1)
        finally:
            data.close()

        self.assertEqual(data.test, 1)

    def test_base_event(self):
        data = Observable()

        result = []

        def test_changed(data):
            result.append(data.test)

        async def test():
            await asyncio.gather(
                asyncio.wait_for(self.update_waiter(data, test_changed), 10),
                self.update_later(data, {'test': 1})
            )

        try:
            asyncio.run(test())
        finally:
            data.close()

        self.assertEqual(result, [1])

    def test_observable(self):
        data = Observable()

        data.update(test=1)

        self.assertEqual(data.test, 1)

    def test_observable_event(self):
        data = Observable(sub_data=Observable())

        result = []

        def data_changed(data):
            result.append(data.sub_data.test)

        async def test():
            await asyncio.gather(
                asyncio.wait_for(self.update_waiter(data, data_changed), 10),
                self.update_later(data.sub_data, {'test': 1})
            )

        try:
            asyncio.run(test())

            self.assertEqual(result, [1])
            self.assertFalse(data.sub_data.updated.is_set())
            self.assertFalse(data.updated.is_set())
        finally:
            data.close()


    def test_remove_observable(self):
        sub_data = Observable(test=0)
        data = Observable(sub_data=sub_data)

        result = []

        def data_changed(data):
            result.append(data.sub_data)

        async def test():
            await asyncio.gather(
                asyncio.wait_for(self.update_waiter(data, data_changed), 10),
                self.update_later(data, {'sub_data': None})
            )
        try:

            asyncio.run(test())

            self.assertEqual(result, [None])

            result.clear()

            sub_data.test = 1

            self.assertEqual(result, [])
        finally:
            sub_data.close()
            data.close()


class TestField(unittest.TestCase):

    def test_basic(self):

        class SimpleExample(Updatable):
            test = Field()

        data = SimpleExample()

        with self.assertRaises(AttributeError):
            data.test

        data.test = 1

        self.assertEqual(data.test, 1)
        self.assertEqual(data.__dict__["_test"], 1)

        data.test = undefined

        with self.assertRaises(AttributeError):
            data.test

    def test_default(self):

        class SimpleExample(Updatable):
            test = Field(0)

        data = SimpleExample()

        self.assertEqual(data.test, 0)
        self.assertEqual(data.__dict__["_test"], 0)

        data.test = 1

        self.assertEqual(data.test, 1)
        self.assertEqual(data.__dict__["_test"], 1)

        data.test = undefined

        self.assertEqual(data.test, 0)
        self.assertEqual(data.__dict__["_test"], 0)

    def test_default_factory(self):

        class SimpleExample(Updatable):
            test = Field(default_factory=int)

        data = SimpleExample()

        self.assertEqual(data.test, 0)
        self.assertEqual(data.__dict__["_test"], 0)

        data.test = 1

        self.assertEqual(data.test, 1)
        self.assertEqual(data.__dict__["_test"], 1)

        data.test = undefined

        self.assertEqual(data.test, 0)
        self.assertEqual(data.__dict__["_test"], 0)

    def test_adapter(self):

        class SimpleExample(Updatable):
            test = Field(adapter=int)

        data = SimpleExample()

        data.test = "1"

        self.assertEqual(data.test, 1)
        self.assertEqual(data.__dict__["_test"], 1)

        with self.assertRaises(ValueError):
            data.test = "a"

    def test_cls(self):

        class SimpleExample(Updatable):
            test = Field(cls=int)

        data = SimpleExample()

        with self.assertRaises(ValueError):
            data.test = "1"

        data.test = 1

        self.assertEqual(data.test, 1)
        self.assertEqual(data.__dict__["_test"], 1)

    def test_cls_and_adapter(self):

        class SimpleExample(Updatable):
            test = Field(adapter=int, cls=int)

        data = SimpleExample()

        with self.assertRaises(ValueError):
            data.test = None

        data.test = "1"

        self.assertEqual(data.test, 1)
        self.assertEqual(data.__dict__["_test"], 1)


class TestFieldFunction(unittest.TestCase):

    def test_basic(self):

        class SimpleExample(Updatable):
            test = field()

        data = SimpleExample()

        with self.assertRaises(AttributeError):
            data.test

        data.test = 1

        self.assertEqual(data.test, 1)
        self.assertEqual(data.__dict__["_test"], 1)

        data.test = undefined

        with self.assertRaises(AttributeError):
            data.test

    def test_default(self):

        class SimpleExample(Updatable):
            test = field(0)

        data = SimpleExample()

        self.assertEqual(data.test, 0)
        self.assertEqual(data.__dict__["_test"], 0)

        data.test = 1

        self.assertEqual(data.test, 1)
        self.assertEqual(data.__dict__["_test"], 1)

        data.test = undefined

        self.assertEqual(data.test, 0)
        self.assertEqual(data.__dict__["_test"], 0)

    def test_default_factory(self):

        class SimpleExample(Updatable):
            test = field(default_factory=int)

        data = SimpleExample()

        self.assertEqual(data.test, 0)
        self.assertEqual(data.__dict__["_test"], 0)

        data.test = 1

        self.assertEqual(data.test, 1)
        self.assertEqual(data.__dict__["_test"], 1)

        data.test = undefined

        self.assertEqual(data.test, 0)
        self.assertEqual(data.__dict__["_test"], 0)

    def test_adapter(self):

        class SimpleExample(Updatable):
            test = field(adapter=int)

        data = SimpleExample()

        data.test = "1"

        self.assertEqual(data.test, 1)
        self.assertEqual(data.__dict__["_test"], 1)

        with self.assertRaises(ValueError):
            data.test = "a"

    def test_cls(self):

        class SimpleExample(Updatable):
            test = field(cls=int)

        data = SimpleExample()

        with self.assertRaises(ValueError):
            data.test = "1"

        data.test = 1

        self.assertEqual(data.test, 1)
        self.assertEqual(data.__dict__["_test"], 1)

    def test_cls_and_adapter(self):

        class SimpleExample(Updatable):
            test = field(adapter=int, cls=int)

        data = SimpleExample()

        with self.assertRaises(ValueError):
            data.test = None

        data.test = "1"

        self.assertEqual(data.test, 1)
        self.assertEqual(data.__dict__["_test"], 1)


if __name__ == "__main__":
    result = unittest.main()
    if not result.wasSuccessful():
        import sys

        sys.exit(1)

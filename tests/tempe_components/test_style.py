# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

import asyncio
import unittest

from tempe.colors import black, grey, white
from tempe_components.style import StateColor, StateColorField, Style, ENABLED, DISABLED, ACTIVE


class TestStateColor(unittest.TestCase):

    def test_basic(self):

        color = StateColor(enabled=black)

        self.assertEqual(color.enabled, black)
        self.assertEqual(color.disabled, black)
        self.assertEqual(color.active, black)

        self.assertEqual(color[ENABLED], black)
        self.assertEqual(color[DISABLED], black)
        self.assertEqual(color[ACTIVE], black)

        color.enabled = white

        self.assertEqual(color.enabled, white)
        self.assertEqual(color.disabled, white)
        self.assertEqual(color.active, white)

        self.assertEqual(color[ENABLED], white)
        self.assertEqual(color[DISABLED], white)
        self.assertEqual(color[ACTIVE], white)

        color[ENABLED] = grey

        self.assertEqual(color.enabled, grey)
        self.assertEqual(color.disabled, grey)
        self.assertEqual(color.active, grey)

        self.assertEqual(color[ENABLED], grey)
        self.assertEqual(color[DISABLED], grey)
        self.assertEqual(color[ACTIVE], grey)

    def test_basic_adapted(self):

        color = StateColor(enabled="black")

        self.assertEqual(color.enabled, black)
        self.assertEqual(color.disabled, black)
        self.assertEqual(color.active, black)

        self.assertEqual(color[ENABLED], black)
        self.assertEqual(color[DISABLED], black)
        self.assertEqual(color[ACTIVE], black)

        color.enabled = "white"

        self.assertEqual(color.enabled, white)
        self.assertEqual(color.disabled, white)
        self.assertEqual(color.active, white)

        self.assertEqual(color[ENABLED], white)
        self.assertEqual(color[DISABLED], white)
        self.assertEqual(color[ACTIVE], white)

        color[ENABLED] = "grey"

        self.assertEqual(color.enabled, grey)
        self.assertEqual(color.disabled, grey)
        self.assertEqual(color.active, grey)

        self.assertEqual(color[ENABLED], grey)
        self.assertEqual(color[DISABLED], grey)
        self.assertEqual(color[ACTIVE], grey)

    def test_full(self):

        color = StateColor(enabled=black, disabled="white")

        self.assertEqual(color.enabled, black)
        self.assertEqual(color.disabled, white)
        self.assertEqual(color.active, black)

        self.assertEqual(color[ENABLED], black)
        self.assertEqual(color[DISABLED], white)
        self.assertEqual(color[ACTIVE], black)

        color.enabled = grey
        color.disabled = "black"
        color[ACTIVE] = white

        self.assertEqual(color.enabled, grey)
        self.assertEqual(color.disabled, black)
        self.assertEqual(color.active, white)

        self.assertEqual(color[ENABLED], grey)
        self.assertEqual(color[DISABLED], black)
        self.assertEqual(color[ACTIVE], white)

    def test_empty(self):

        color = StateColor()

        with self.assertRaises(AttributeError):
            color.enabled

        with self.assertRaises(AttributeError):
            color.disabled

        with self.assertRaises(AttributeError):
            color.active

        color.enabled = black

        self.assertEqual(color.enabled, black)
        self.assertEqual(color.disabled, black)
        self.assertEqual(color.active, black)

        self.assertEqual(color[ENABLED], black)
        self.assertEqual(color[DISABLED], black)
        self.assertEqual(color[ACTIVE], black)


    def test_bad(self):

        color = StateColor()

        with self.assertRaises(ValueError):
            color.enabled = (1,)


class TestStyle(unittest.TestCase):

    async def update_waiter(self, data, callback):
        await data.updated.wait()
        callback(data)

    async def update_later(self, data, update, delay=0.01):
        await asyncio.sleep(delay)
        data.update(update)

    async def cancel_task_later(self, task, delay=1.0):
        await asyncio.sleep(delay)
        task.cancel()

    def test_basic(self):
        style = Style(
            background=StateColor(),
            border=StateColor(),
            radius=0,
            text=StateColor(),
            font=None,
        )

        try:
            self.assertEqual(style.radius, 0)
        finally:
            style.close()

    def test_inherited(self):
        bg_color = StateColor()
        parent = Style(
            background=bg_color,
            border=StateColor(),
            radius=0,
            text=StateColor(),
            font=None,
        )
        style = Style(
            parent=parent,
            radius=2,
        )
        try:
            self.assertEqual(style.radius, 2)
            self.assertEqual(style.background, bg_color)

            new_color = StateColor()
            style.background = new_color

            self.assertEqual(style.background, new_color)
            self.assertEqual(parent.background, bg_color)
        finally:
            parent.close()
            style.close()

    def test_updates(self):
        bg_color = StateColor()
        parent = Style(
            background=bg_color,
            border=StateColor(),
            radius=0,
            text=StateColor(),
            font=None,
        )
        style = Style(
            parent=parent,
            radius=2,
        )

        result = []

        def test_changed(data):
            result.append(data.test)

        obs = asyncio.create_task(aobserve(data, test_changed))

        async def test():
            await asyncio.gather(
                asyncio.wait_for(obs, 10),
                self.update_later(data, {'test': 1}, 0.01),
                self.update_later(data, {'test': 2}, 0.05),
                self.cancel_task_later(obs, 0.1)
            )

        try:
            asyncio.run(test())
        finally:
            data.close()

        self.assertEqual(result, [1, 2])

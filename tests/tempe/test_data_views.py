# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

import unittest

from tempe.data_view import Count


class TestCount(unittest.TestCase):

    def test_count(self):
        """Test count starts and steps as expected."""

        count = Count(10, 5)
        count_iter = iter(count)

        self.assertEqual(next(count_iter), 10)
        self.assertEqual(next(count_iter), 15)
        self.assertEqual(next(count_iter), 20)

    def test_count_getiten(self):
        """Test count getitem works as expected."""

        count = Count(10, 5)

        self.assertEqual(count[0], 10)
        self.assertEqual(count[1], 15)
        self.assertEqual(count[2], 20)

    def test_count_default(self):
        """Test count default starts and steps as expected."""

        count = Count()
        count_iter = iter(count)

        self.assertEqual(next(count_iter), 0)
        self.assertEqual(next(count_iter), 1)
        self.assertEqual(next(count_iter), 2)

    def test_count_default_getiten(self):
        """Test count getitem works as expected."""

        count = Count()

        self.assertEqual(count[0], 0)
        self.assertEqual(count[1], 1)
        self.assertEqual(count[2], 2)


if __name__ == "__main__":
    result = unittest.main()
    if not result.wasSuccessful():
        import sys

        sys.exit(1)

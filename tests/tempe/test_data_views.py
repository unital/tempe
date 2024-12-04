# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

import unittest

from tempe.data_view import Count, Range


class TestCount(unittest.TestCase):

    def test_count(self):
        """Test count starts and steps as expected."""

        count = Count(10, 5)
        count_iter = iter(count)

        self.assertEqual(next(count_iter), 10)
        self.assertEqual(next(count_iter), 15)
        self.assertEqual(next(count_iter), 20)

    def test_count_getitem(self):
        """Test count getitem works as expected."""

        count = Count(10, 5)

        self.assertEqual(count[0], 10)
        self.assertEqual(count[1], 15)
        self.assertEqual(count[2], 20)
        # consistent, so leave it as behaviour
        self.assertEqual(count[-1], 5)

    def test_count_getitem_slice(self):
        """Test count getitem works with slices."""

        count = Count(10, 5)

        self.assertEqual(count[2:5:2], [20, 30])

    def test_count_default(self):
        """Test count default starts and steps as expected."""

        count = Count()
        count_iter = iter(count)

        self.assertEqual(next(count_iter), 0)
        self.assertEqual(next(count_iter), 1)
        self.assertEqual(next(count_iter), 2)

    def test_count_default_getitem(self):
        """Test count default getitem works as expected."""

        count = Count()

        self.assertEqual(count[0], 0)
        self.assertEqual(count[1], 1)
        self.assertEqual(count[2], 2)


class TestRange(unittest.TestCase):

    def test_range(self):
        """Test range starts and steps as expected."""

        r = Range(10, 25, 5)

        self.assertEqual(list(r), [10, 15, 20])

    def test_range_len(self):
        """Test range length is correct."""

        r = Range(10, 25, 5)

        self.assertEqual(len(r), 3)

    def test_range_getitem(self):
        """Test range getitem works as expected."""

        r = Range(10, 25, 5)

        self.assertEqual(r[0], 10)
        self.assertEqual(r[1], 15)
        self.assertEqual(r[2], 20)
        self.assertEqual(r[-1], 20)

    def test_range_getitem_slice(self):
        """Test range getitem works with slices."""

        r = Range(10, 50, 5)

        self.assertEqual(r[2:5:2], [20, 30])

    def test_range_defaults(self):
        """Test range default starts and steps as expected."""

        r1 = Range(10)
        r2 = Range(10, 15)

        self.assertEqual(list(r1), list(range(10)))
        self.assertEqual(list(r2), list(range(10, 15)))


if __name__ == "__main__":
    result = unittest.main()
    if not result.wasSuccessful():
        import sys

        sys.exit(1)

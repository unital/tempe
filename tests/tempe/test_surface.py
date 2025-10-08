# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

import unittest

from tempe.surface import Surface, DRAWING
from tempe.shapes import Shape
from tempe.raster import Raster

class DummyShape(Shape):

    def _get_bounds(self):
        return (10, 10, 20, 20)


class TestSurface(unittest.TestCase):

    def setUp(self):
        self.surface = Surface()
        self.shape = DummyShape()
        self.buffer = bytearray(2 * 50 * 50)

    def tearDown(self):
        del self.surface
        del self.shape
        del self.buffer

    def refresh_surface(self):
        self.surface._damage = []
        self.surface.refresh_needed.clear()

    def test_add_shape(self):
        self.surface.add_shape(DRAWING, self.shape)

        self.assertEqual(self.surface.layers[DRAWING], [self.shape])
        self.assertEqual(self.shape.surface, self.surface)
        self.assertEqual(self.surface._damage, [self.shape._bounds])
        self.assertTrue(self.surface.refresh_needed.is_set())

    def test_remove_shape(self):
        self.surface.add_shape(DRAWING, self.shape)
        self.refresh_surface()

        self.surface.remove_shape(DRAWING, self.shape)

        self.assertEqual(self.surface.layers[DRAWING], [])
        self.assertEqual(self.shape.surface, None)
        self.assertEqual(self.surface._damage, [self.shape._bounds])
        self.assertTrue(self.surface.refresh_needed.is_set())

    def test_clear(self):
        self.surface.add_shape(DRAWING, self.shape)
        self.refresh_surface()

        self.surface.clear(DRAWING)

        self.assertEqual(self.surface.layers[DRAWING], [])
        self.assertEqual(self.shape.surface, None)
        self.assertEqual(self.surface._damage, [self.shape._bounds])
        self.assertTrue(self.surface.refresh_needed.is_set())


if __name__ == "__main__":
    result = unittest.main()
    if not result.wasSuccessful():
        import sys

        sys.exit(1)

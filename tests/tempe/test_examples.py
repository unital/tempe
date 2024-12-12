# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

import gc
import unittest

from tempe.display import FileDisplay

working_buffer = bytearray(320 * 61 * 2)


class TestExamples(unittest.TestCase):
    def test_examples(self):
        """Bytewise comparison that output of examples is what is expected."""

        examples = [
            ("examples/polar_example.py", "tests/tempe/polar.rgb565"),
            ("examples/lines_example.py", "tests/tempe/lines.rgb565"),
            ("examples/rounded_rect_example.py", "tests/tempe/rounded_rect.rgb565"),
            ("examples/shapes_example.py", "tests/tempe/shapes.rgb565"),
            ("examples/line_plot_example.py", "tests/tempe/line_plot.rgb565"),
            ("examples/scatter_plot_example.py", "tests/tempe/scatter_plot.rgb565"),
            ("examples/polar_plot_example.py", "tests/tempe/polar_plot.rgb565"),
            ("examples/hello_world.py", "tests/tempe/hello_world.rgb565"),
        ]
        for file, result in examples:
            print(file, result)
            with self.subTest(example=file):
                gc.collect()
                code = open(file, "r").read()
                locals = {"__name__": "__test__"}
                exec(code, locals)

                output = self.display_output(locals["surface"])

                self.assert_files_equal(output, result)

    def display_output(self, surface, name="example.rgb565"):
        display = FileDisplay(name, (320, 240))

        with display:
            display.clear()
            surface.refresh(display, working_buffer)

        return name

    def assert_files_equal(self, file1, file2):
        with open(file1, "rb") as f1:
            with open(file2, "rb") as f2:
                i = 0
                while True:
                    b1 = f1.read(1)
                    b2 = f2.read(1)
                    if b1 != b2:
                        print(f"Byte {i}")
                    self.assertEqual(b1, b2)
                    if not b1:
                        break
                    i += 1


if __name__ == "__main__":
    result = unittest.main()
    if not result.wasSuccessful():
        import sys

        sys.exit(1)

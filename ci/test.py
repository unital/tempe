# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

from pathlib import Path
import os
import subprocess
import sys

import click


@click.command()
def test():
    """Run unit tests in micropython"""
    print("Running Tests")
    failures = []
    test_dir = Path("tests/tempe")
    os.environ["MICROPYPATH"] = "src:" + os.environ.get(
        "MICROPYPATH", ":examples:.frozen:~/.micropython/lib:/usr/lib/micropython"
    )
    for path in sorted(test_dir.glob("*.py")):
        print(path.name, "... ", end="", flush=True)
        result = run_test(path)
        if result:
            failures.append(result)
            print("FAILED")
        else:
            print("OK")
    print()

    for path, stdout, stderr in failures:
        print("FAILURE: ", path.name)
        print("STDOUT ", "=" * 70)
        print(stdout.decode("utf-8"))
        print()
        print("STDERR ", "=" * 70)
        print(stderr.decode("utf-8"))
        print()

    if failures:
        sys.exit(1)
    else:
        print("PASSED")


def run_test(path):
    try:
        result = subprocess.run(["micropython", path], capture_output=True, check=True)
    except subprocess.CalledProcessError as exc:
        return (path, exc.stdout, exc.stderr)


if __name__ == "__main__":
    test()

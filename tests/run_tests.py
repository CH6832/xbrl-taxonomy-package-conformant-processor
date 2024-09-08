#!/usr/bin/env python3

"""run tests.py

The script can be used to run all tests.
"""

from typing import Any, Literal, NoReturn
import pytest
import sys
import os


def main() -> NoReturn:
    """Drving code."""
    # Get the directory of the script.
    script_directory = os.path.dirname(os.path.abspath(__file__))
    # Run the tests.
    sys.exit(run_tests_in_directory(script_directory))


def run_tests_in_directory(directory: str) -> (Any | Literal[1]):
    """Runs pytest on all Python files starting with 'test_' in the specified directory."""
    test_files = []

    # Iterate over files in the directory.
    for file in os.listdir(directory):
        if file.endswith(".py") and file.startswith("test_"):
            test_files.append(os.path.join(directory, file))

    # Check if there are any test files.
    if not test_files:
        print("No test files found.")
        return 1

    # Run pytest on the collected test files.
    print("Running tests:")
    for test_file in test_files:
        print(f" - {test_file}")

    exit_code = pytest.main(test_files)

    return exit_code


if __name__ == "__main__":
    main()

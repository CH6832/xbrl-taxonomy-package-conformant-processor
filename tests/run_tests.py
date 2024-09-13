#!/usr/bin/env python3

"""run tests.py

The script can be used to run all tests.
"""

from typing import Any, Literal, NoReturn
import pytest
import sys
import os
# line below ensures that python searhces through all directories for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.helpers.logger import set_logging_directory, setup_logger

log_file_path = set_logging_directory(r'..\logs', log_filename="app_tests.log")
logger = setup_logger(__name__, log_file=log_file_path)


def main() -> NoReturn:
    """Drving code."""
    # Get the directory of the script.
    script_directory = os.path.dirname(os.path.abspath(__file__))
    logger.info("Starting test execution.")
    
    # Run tests.
    try:
        sys.exit(run_tests_in_directory(script_directory))
    except Exception as e:
        logger.error(f"Error running tests: {e}", exc_info=True)
        sys.exit(1)


def run_tests_in_directory(directory: str) -> (Any | Literal[1]):
    """Runs pytest on all Python files starting with 'test_' in the specified directory."""
    test_files = []

    for file in os.listdir(directory):
        # if file.endswith(".py") and file.startswith("test_"):
        logger.debug(f"Discovered file: {file}")
        test_files.append(os.path.join(directory, file))

    # Check if there are any test files.
    if not test_files:
        logger.warning("No test files found.")
        print("No test files found.")
        return 1

    # Run pytest on the collected test files.
    print("Running tests:")
    for test_file in test_files:
        print(f" - {test_file}")
        logger.info(f"Running test file: {test_file}")

    exit_code = pytest.main(test_files)
    if exit_code == 0:
        logger.info("All tests passed.")
    else:
        logger.error(f"Tests failed with exit code {exit_code}.")

    return exit_code


if __name__ == "__main__":
    main()

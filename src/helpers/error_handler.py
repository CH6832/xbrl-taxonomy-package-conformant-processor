#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""error_handler.py

The module provides error handling functions.

Example usage
@handle_error
def divide(a, b):
    if b == 0:
        raise ValidationError("b", "Division by zero is not allowed")
    return a / b


if __name__ == "__main__":
    try:
        result = divide(10, 0)
    except Exception as e:
        logger.error("An error occurred: %s", e)
"""

import os
import sys
from typing import Any
from logging import Logger
# line below ensures that python searhces through all directories for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.helpers.logger import setup_logger

logger: Logger = setup_logger(__name__)


class BaseCustomException(Exception):
    """
    Base class for all custom exceptions in the project.
    """

    def __init__(self, message: str = "An error occurred"):
        super().__init__(message)
        logger.error("Error: %s", message)


class FileNotFoundError(BaseCustomException):
    """
    Exception raised when a required file is not found.
    """

    def __init__(self, filepath: str, message: str = "File not found") -> None:
        self.filepath = filepath
        super().__init__(f"{message}: {filepath}")
        logger.error("FileNotFoundError: %s at %s", message, filepath)

        return None


class ValidationError(BaseCustomException):
    """
    Exception raised for validation errors.
    """

    def __init__(self, field: str, message: str = "Invalid input") -> None:
        self.field = field
        super().__init__(f"{message}: {field}")
        logger.error("ValidationError: %s in field %s", message, field)

        return None


class InvalidFileFormatError(BaseCustomException):
    """
    Exception raised when a file has an invalid format.
    """
    
    def __init__(self, file_format: str, message: str = "Invalid file format") -> None:
        self.file_format = file_format
        super().__init__(f"{message}: {file_format}")
        logger.error("InvalidFileFormatError: %s for format %s", message, file_format)

        return None


def handle_error(func):
    """Decorator function to wrap other functions for error handling."""

    def wrapper(*args, **kwargs) -> Any:
        """Wrapper function that applies error handling to the decorated function."""
        try:
            return func(*args, **kwargs)
        except BaseCustomException as e:
            logger.error("Custom error caught: %s", e)
            raise e
        except Exception as e:
            logger.error("Unhandled exception: %s", e)
            raise e

    return wrapper

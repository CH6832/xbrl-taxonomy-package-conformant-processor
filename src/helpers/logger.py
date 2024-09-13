#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""logger.py

The module provides logging functionality.

Example usage:
if __name__ == "__main__":
    log_file_path = set_logging_directory('logs')
    logger = setup_logger(__name__, log_file=log_file_path)
    logger.info("This is an info message.")
    logger.error("This is an error message.")
"""

import os
import sys
import logging
from logging.handlers import RotatingFileHandler
# line below ensures that python searhces through all directories for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def setup_logger(name: str, log_file: str, level: int = logging.INFO, max_bytes: int = 1_000_000, backup_count: int = 5) -> logging.Logger:
    """Set up a logger with a specified name, log file, and log level."""

    # Create a logger with the given name
    logger: logging.Logger = logging.getLogger(name)
    logger.setLevel(level)

    # Check if a handler already exists to avoid duplicates.
    if not logger.hasHandlers():
        # Create a rotating file handler.
        file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
        file_handler.setLevel(level)

        # Create a console handler for output to terminal.
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.ERROR) # Console only shows errors

        # Define a log format.
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add the handlers to the logger.
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


def set_logging_directory(log_dir: str, log_filename: str) -> str:
    """Ensure the logging directory exists, and return the log file path."""
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_file = os.path.join(log_dir, log_filename)
    
    return log_file

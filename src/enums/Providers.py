#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Providers.py

Defines the Provider enum for taxonomy packages.
"""

from enum import Enum


class Provider(Enum):
    """
    Taxonomy packages providers.
    """
    EBA = "EBA"
    EDINET = "EDINET"
    CMFCLCI = "CMFCLCI"
    CIPC = "CIPC"

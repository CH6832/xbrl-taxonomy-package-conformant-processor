#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Fixer.py

The module contains classes with relevant methods to fix
xbrl taxonomy packages based by certain providers.
"""

import os
import sys
# line below ensures that python searhces through all directories for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from abc import ABC, abstractmethod
from xml.dom.minidom import parseString
import xml.etree.ElementTree as ET
import zipfile
from io import TextIOWrapper
import shutil
from colorama import Fore
from src.checker.TPChecker import TPChecker
from .TPFixerInterface import TaxonomyPackageFixerInterface
from ..helpers.utils import *

class EBATaxonomyPackage(TaxonomyPackageFixerInterface):
    """
    Use this class to fix an EBA XBRL Taxonomy Package.
    
    The package in input/* folder as well as newer and older versions
    can be found here: https://www.eba.europa.eu/risk-analysis-and-data/reporting-frameworks/reporting-framework-3.3
    """ 

    def convert_to_zip_archive(self) -> None:
        return None


    def fix_meta_inf_folder(self) -> None:
        return None


    def fix_top_level_single_dir(self) -> None:
        return None


    def restructure_folder(self) -> None:
        return None


    def fix_taxonomy_package_xml(self) -> None:
        return None

    
    def fix_catalog_xml(self) -> None:
        return None

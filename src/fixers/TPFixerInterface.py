#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Checker.py

Provides all sorts of classes and functions to
analyze an XBRL Taxonomy Package.
"""

import os
import sys
# line below ensures that python searhces through all directories for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from abc import ABC, abstractmethod
from xml.dom.minidom import parseString
import xml.etree.ElementTree as ET
from io import TextIOWrapper
import shutil
import zipfile
from colorama import Fore
from ..checker.TPChecker import TPChecker
from ..helpers.utils import print_color_msg


class TaxonomyPackageFixerInterface(ABC):
    """
    The Interface provides methods to fix an XBRL Taxonomy Package by a certain provider.
    """

    def __init__(self, full_path_to_zip: str, destination_folder: str) -> None:
        """Initialize XBRL Taxonomy Package class. By initializing the class
        the input package is copied over to the ouptut folder and extracted there
        to comfortably work with the data."""
        # set initial variables
        self.full_path_to_zip = full_path_to_zip
        self.destination_folder = destination_folder
        # create destination folder
        os.makedirs(self.destination_folder, exist_ok=True)
        # move taxonomy package to destination folder
        shutil.move(f"{self.full_path_to_zip}", self.destination_folder)
        # extract at destination
        print(os.path.join(self.destination_folder, os.path.basename(full_path_to_zip)))
        try:
            with zipfile.ZipFile(os.path.join(self.destination_folder, os.path.basename(full_path_to_zip)), 'r') as zip_ref:
                zip_ref.extractall(self.destination_folder)
            print(f"Extracted {self.full_path_to_zip} to {self.destination_folder}")
        except zipfile.BadZipFile:
            print(f"Error: The file {self.full_path_to_zip} is not a valid ZIP archive.")
        except PermissionError:
            print(f"Error: Permission denied. Cannot extract to {self.destination_folder}.")
        except Exception as e:
            print(f"An error occurred: {e}")
        
        return None


    @abstractmethod
    def convert_to_zip_archive(self):
        """Returns an xbrl taxonomy package in zip format."""


    @abstractmethod
    def fix_top_level_single_dir(self):
        """Generates a single toplevel directory for
        the provided xbrl taxonomy package."""


    @abstractmethod
    def fix_meta_inf_folder(self):
        """Generates a META-INF folder for the
        provided xbrl taxonomy package."""


    @abstractmethod
    def restructure_folder(self):
        """Perform restructuring of folders in the
        XBRL Taxonomy Package."""


    @abstractmethod
    def fix_taxonomy_package_xml(self):
        """The top-level directory MUST contain a taxonomyPackage.xml file"""
    
    
    @abstractmethod
    def fix_catalog_xml(self):
        """'A Taxonomy Package MUST NOT include a catalog file which includes more than one rewriteURI element
        with the same value (after performing URI Normalization, as prescribed by the XML Catalog Specification)
        for the @uriStartString attribute (tpe:multipleRewriteURIsForStartString).'"""

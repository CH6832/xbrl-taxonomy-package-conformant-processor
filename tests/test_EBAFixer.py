#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""test_EBAFixer.py"""

import os
import sys
import zipfile
import pytest
# line below ensures that python searhces through all directories for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.fixers.EBAFixer import EBATaxonomyPackage


@pytest.fixture
def setup_example_0_zip():
    """Fixture to set up example_0.zip for testing."""
    full_path_to_zip = "data/EBAFixerTest/test_convert_to_zip_archive/data/example_0/example_0.zip"
    zipfile.ZipFile(full_path_to_zip, 'w').close()
    destination_folder = "data/EBAFixerTest/test_convert_to_zip_archive/data/example_1"
    return full_path_to_zip, destination_folder


def test_convert_to_zip_archive(setup_example_0_zip):
    """Test the convert_to_zip_archive method.

    This test creates an instance of EBATaxonomyPackage and calls its convert_to_zip_archive
    method. It ensures that the method can be called without raising an error.
    """
    full_path_to_zip, destination_folder = setup_example_0_zip
    eba_package = EBATaxonomyPackage(full_path_to_zip, destination_folder)
    eba_package.convert_to_zip_archive()


def test_fix_meta_inf_folder():
    """Test the fix_meta_inf_folder method.

    This test creates an instance of EBATaxonomyPackage and calls its fix_meta_inf_folder
    method. It ensures that the method can be called without raising an error.
    """
    full_path_to_zip = "data/EBAFixerTest/test_fix_meta_inf_folder/example_0/example_0.zip"
    destination_folder = "data/EBAFixerTest/test_fix_meta_inf_folder/example_1"
    eba_package = EBATaxonomyPackage(full_path_to_zip, destination_folder)
    eba_package.fix_meta_inf_folder()


def test_fix_top_level_single_dir():
    """Test the fix_top_level_single_dir method.

    This test creates an instance of EBATaxonomyPackage and calls its fix_top_level_single_dir
    method. It ensures that the method can be called without raising an error.
    """
    full_path_to_zip = "data/EBAFixerTest/test_fix_top_level_single_dir/example_0.zip"
    destination_folder = "data/EBAFixerTest/test_fix_top_level_single_dir/example_0"
    eba_package = EBATaxonomyPackage(full_path_to_zip, destination_folder)
    eba_package.fix_top_level_single_dir()


def test_restructure_folder():
    """Test the restructure_folder method.

    This test creates an instance of EBATaxonomyPackage and calls its restructure_folder
    method. It ensures that the method can be called without raising an error.
    """
    full_path_to_zip = "data/EBAFixerTest/test_fix_top_level_single_dir/example_0.zip"
    destination_folder = "data/EBAFixerTest/test_fix_top_level_single_dir/example_0"
    eba_package = EBATaxonomyPackage(full_path_to_zip, destination_folder)
    eba_package.restructure_folder()


def test_fix_taxonomy_package_xml():
    """Test the fix_taxonomy_package_xml method.

    This test creates an instance of EBATaxonomyPackage and calls its fix_taxonomy_package_xml
    method. It ensures that the method can be called without raising an error.
    """
    full_path_to_zip = "data/EBAFixerTest/test_fix_top_level_single_dir/example_0.zip"
    destination_folder = "data/EBAFixerTest/test_fix_top_level_single_dir/example_0"
    eba_package = EBATaxonomyPackage(full_path_to_zip, destination_folder)
    eba_package.fix_taxonomy_package_xml()


def test_fix_catalog_xml():
    """Test the fix_catalog_xml method.

    This test creates an instance of EBATaxonomyPackage and calls its fix_catalog_xml
    method. It ensures that the method can be called without raising an error.
    """
    full_path_to_zip = "data/example_0.zip"
    destination_folder = "data/example_0"
    eba_package = EBATaxonomyPackage(full_path_to_zip, destination_folder)
    eba_package.fix_catalog_xml()

if __name__ == '__main__':
    pytest.main()

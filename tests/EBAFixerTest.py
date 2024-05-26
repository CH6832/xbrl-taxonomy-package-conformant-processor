#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import unittest
import zipfile
# line below ensures that python searhces through all directories for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.classes.EBAFixer import EBATaxonomyPackage

class TestEBATaxonomyPackage(unittest.TestCase):
    """
    A test class for the EBATaxonomyPackage class.

    This class tests the methods of the EBATaxonomyPackage class to ensure that they exist
    and can be called without errors.
    """

    def test_convert_to_zip_archive(self: unittest.TestCase) -> None:
        """Test the convert_to_zip_archive method.

        This method creates an instance of EBATaxonomyPackage and calls its convert_to_zip_archive
        method. It does not validate the functionality of the method but ensures that it can be called
        without raising an error.
        """

        full_path_to_zip = "data/EBAFixerTest/test_convert_to_zip_archive/data/example_0/example_0.zip"
        zipfile.ZipFile(full_path_to_zip, 'w').close()
        destination_folder = "data/EBAFixerTest/test_convert_to_zip_archive/data/example_1"
        eba_package: EBATaxonomyPackage = EBATaxonomyPackage(full_path_to_zip, destination_folder)
        eba_package.convert_to_zip_archive()

        return None

    def test_fix_meta_inf_folder(self: unittest.TestCase) -> None:
        """Test the fix_meta_inf_folder method.

        This method creates an instance of EBATaxonomyPackage and calls its fix_meta_inf_folder
        method. It does not validate the functionality of the method but ensures that it can be called
        without raising an error.
        """
        full_path_to_zip = "data/EBAFixerTest/test_fix_meta_inf_folder/example_0/example_0.zip"
        destination_folder = "data/EBAFixerTest/test_fix_meta_inf_folder/example_1"
        eba_package: EBATaxonomyPackage = EBATaxonomyPackage(full_path_to_zip, destination_folder)
        eba_package.fix_meta_inf_folder()

        return None

    def test_fix_top_level_single_dir(self: unittest.TestCase) -> None:
        """Test the fix_top_level_single_dir method.

        This method creates an instance of EBATaxonomyPackage and calls its fix_top_level_single_dir
        method. It does not validate the functionality of the method but ensures that it can be called
        without raising an error.
        """
        full_path_to_zip = "data/EBAFixerTest/test_fix_top_level_single_dir/example_0.zip"
        destination_folder = "data/EBAFixerTest/test_fix_top_level_single_dir/example_0"
        eba_package: EBATaxonomyPackage = EBATaxonomyPackage(full_path_to_zip, destination_folder)
        eba_package.fix_top_level_single_dir()

        return None

    def test_restructure_folder(self: unittest.TestCase) -> None:
        """Test the restructure_folder method.

        This method creates an instance of EBATaxonomyPackage and calls its restructure_folder
        method. It does not validate the functionality of the method but ensures that it can be called
        without raising an error.
        """
        full_path_to_zip = "data/EBAFixerTest/test_fix_top_level_single_dir/example_0.zip"
        destination_folder = "data/EBAFixerTest/test_fix_top_level_single_dir/example_0"
        eba_package: EBATaxonomyPackage = EBATaxonomyPackage(full_path_to_zip, destination_folder)
        eba_package.restructure_folder()

        return None

    def test_fix_taxonomy_package_xml(self: unittest.TestCase) -> None:
        """Test the fix_taxonomy_package_xml method.

        This method creates an instance of EBATaxonomyPackage and calls its fix_taxonomy_package_xml
        method. It does not validate the functionality of the method but ensures that it can be called
        without raising an error.
        """
        full_path_to_zip = "data/EBAFixerTest/test_fix_top_level_single_dir/example_0.zip"
        destination_folder = "data/EBAFixerTest/test_fix_top_level_single_dir/example_0"
        eba_package: EBATaxonomyPackage = EBATaxonomyPackage(full_path_to_zip, destination_folder)
        eba_package.fix_taxonomy_package_xml()

        return None

    def test_fix_catalog_xml(self: unittest.TestCase) -> None:
        """Test the fix_catalog_xml method.

        This method creates an instance of EBATaxonomyPackage and calls its fix_catalog_xml
        method. It does not validate the functionality of the method but ensures that it can be called
        without raising an error.
        """
        full_path_to_zip = "data/example_0.zip"
        destination_folder = "data/example_0"        
        eba_package: EBATaxonomyPackage = EBATaxonomyPackage(full_path_to_zip, destination_folder)
        eba_package.fix_catalog_xml()

        return None

if __name__ == '__main__':
    unittest.main()

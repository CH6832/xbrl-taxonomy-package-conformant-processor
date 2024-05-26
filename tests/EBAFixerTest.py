#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
from Fixer import EBATaxonomyPackage

class TestEBATaxonomyPackage(unittest.TestCase):
    """
    A test class for the EBATaxonomyPackage class.

    This class tests the methods of the EBATaxonomyPackage class to ensure that they exist
    and can be called without errors.
    """

    def test_convert_to_zip_archive(self):
        """
        Test the convert_to_zip_archive method.

        This method creates an instance of EBATaxonomyPackage and calls its convert_to_zip_archive
        method. It does not validate the functionality of the method but ensures that it can be called
        without raising an error.
        """
        eba_package = EBATaxonomyPackage()
        eba_package.convert_to_zip_archive()

    def test_fix_meta_inf_folder(self):
        """
        Test the fix_meta_inf_folder method.

        This method creates an instance of EBATaxonomyPackage and calls its fix_meta_inf_folder
        method. It does not validate the functionality of the method but ensures that it can be called
        without raising an error.
        """
        eba_package = EBATaxonomyPackage()
        eba_package.fix_meta_inf_folder()

    def test_fix_top_level_single_dir(self):
        """
        Test the fix_top_level_single_dir method.

        This method creates an instance of EBATaxonomyPackage and calls its fix_top_level_single_dir
        method. It does not validate the functionality of the method but ensures that it can be called
        without raising an error.
        """
        eba_package = EBATaxonomyPackage()
        eba_package.fix_top_level_single_dir()

    def test_restructure_folder(self):
        """
        Test the restructure_folder method.

        This method creates an instance of EBATaxonomyPackage and calls its restructure_folder
        method. It does not validate the functionality of the method but ensures that it can be called
        without raising an error.
        """
        eba_package = EBATaxonomyPackage()
        eba_package.restructure_folder()

    def test_fix_taxonomy_package_xml(self):
        """
        Test the fix_taxonomy_package_xml method.

        This method creates an instance of EBATaxonomyPackage and calls its fix_taxonomy_package_xml
        method. It does not validate the functionality of the method but ensures that it can be called
        without raising an error.
        """
        eba_package = EBATaxonomyPackage()
        eba_package.fix_taxonomy_package_xml()

    def test_fix_catalog_xml(self):
        """
        Test the fix_catalog_xml method.

        This method creates an instance of EBATaxonomyPackage and calls its fix_catalog_xml
        method. It does not validate the functionality of the method but ensures that it can be called
        without raising an error.
        """
        eba_package = EBATaxonomyPackage()
        eba_package.fix_catalog_xml()

if __name__ == '__main__':
    unittest.main()

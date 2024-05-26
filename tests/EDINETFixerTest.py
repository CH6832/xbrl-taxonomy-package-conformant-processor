#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
from unittest.mock import patch
from Fixer import EDINETTaxonomyPackage
import os

class TestEDINETTaxonomyPackage(unittest.TestCase):
    """
    A test class for the EDINETTaxonomyPackage class.

    This class tests the methods of the EDINETTaxonomyPackage class to ensure their functionality.
    """

    def setUp(self):
        """
        Set up the test environment.

        This method is called before each test method is run to set up any necessary
        resources or configurations.
        """
        self.package_fixer = EDINETTaxonomyPackage()

    def test_convert_to_zip_archive(self):
        """
        Test the convert_to_zip_archive method.

        This method tests whether the convert_to_zip_archive method creates a ZIP archive
        from the specified source folder.
        """
        with patch('shutil.make_archive') as mock_make_archive:
            self.package_fixer.convert_to_zip_archive()
            mock_make_archive.assert_called_once()

    def test_fix_top_level_single_dir(self):
        """
        Test the fix_top_level_single_dir method.

        This method tests whether the fix_top_level_single_dir method creates a top-level
        directory in the destination folder.
        """
        with patch('os.makedirs') as mock_makedirs:
            self.package_fixer.fix_top_level_single_dir()
            mock_makedirs.assert_called_once()

    def test_fix_meta_inf_folder(self):
        """
        Test the fix_meta_inf_folder method.

        This method tests whether the fix_meta_inf_folder method creates a META-INF directory
        in the destination folder.
        """
        with patch('os.makedirs') as mock_makedirs:
            self.package_fixer.fix_meta_inf_folder()
            mock_makedirs.assert_called_once()

    def test_restructure_folder(self):
        """
        Test the restructure_folder method.

        This method tests whether the restructure_folder method moves files to the root directory
        in the destination folder.
        """
        with patch('os.listdir') as mock_listdir:
            with patch('os.path.join') as mock_join:
                self.package_fixer.restructure_folder()
                mock_listdir.assert_called_once_with(self.package_fixer.destination_folder)
                mock_join.assert_called()

    def test_fix_taxonomy_package_xml(self):
        """
        Test the fix_taxonomy_package_xml method.

        This method tests whether the fix_taxonomy_package_xml method generates a taxonomyPackage.xml file
        in the specified source folder.
        """
        with patch('xml.etree.ElementTree.SubElement') as mock_subelement:
            with patch('os.listdir') as mock_listdir:
                self.package_fixer.fix_taxonomy_package_xml('source_folder')
                mock_subelement.assert_called()
                mock_listdir.assert_called()

    def test_fix_catalog_xml(self):
        """
        Test the fix_catalog_xml method.

        This method tests whether the fix_catalog_xml method generates a catalog.xml file
        in the specified source folder.
        """
        with patch('xml.etree.ElementTree.SubElement') as mock_subelement:
            with patch('os.listdir') as mock_listdir:
                self.package_fixer.fix_catalog_xml('source_folder')
                mock_subelement.assert_called()
                mock_listdir.assert_called()

if __name__ == '__main__':
    unittest.main()

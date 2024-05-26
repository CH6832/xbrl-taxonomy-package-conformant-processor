#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
from unittest.mock import patch
import os
import sys
# line below ensures that python searhces through all directories for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.classes.EDINETFixer import EDINETTaxonomyPackage

class TestEDINETTaxonomyPackage(unittest.TestCase):
    """
    A test class for the EDINETTaxonomyPackage class.

    This class tests the methods of the EDINETTaxonomyPackage class to ensure their functionality.
    """

    def setUp(self) -> None:
        """Set up the test environment.

        This method is called before each test method is run to set up any necessary
        resources or configurations.
        """
        path_to_zip = "data/archive_single_dir.zip"
        dest_folder = "data"
        self.package_fixer = EDINETTaxonomyPackage(path_to_zip, dest_folder)

        return None

    def test_convert_to_zip_archive(self) -> None:
        """Test the convert_to_zip_archive method.

        This method tests whether the convert_to_zip_archive method creates a ZIP archive
        from the specified source folder.
        """
        with patch('shutil.make_archive') as mock_make_archive:
            self.package_fixer.convert_to_zip_archive()
            mock_make_archive.assert_called_once()

        return None

    def test_fix_top_level_single_dir(self) -> None:
        """Test the fix_top_level_single_dir method.

        This method tests whether the fix_top_level_single_dir method creates a top-level
        directory in the destination folder.
        """
        with patch('os.makedirs') as mock_makedirs:
            self.package_fixer.fix_top_level_single_dir()
            mock_makedirs.assert_called_once()
        
        return None

    def test_fix_meta_inf_folder(self) -> None:
        """Test the fix_meta_inf_folder method.

        This method tests whether the fix_meta_inf_folder method creates a META-INF directory
        in the destination folder.
        """
        with patch('os.makedirs') as mock_makedirs:
            self.package_fixer.fix_meta_inf_folder()
            mock_makedirs.assert_called_once()

        return None

    def test_restructure_folder(self) -> None:
        """Test the restructure_folder method.

        This method tests whether the restructure_folder method moves files to the root directory
        in the destination folder.
        """
        with patch('os.listdir') as mock_listdir:
            with patch('os.path.join') as mock_join:
                self.package_fixer.restructure_folder()
                mock_listdir.assert_called_once_with(self.package_fixer.destination_folder)
                mock_join.assert_called()

        return None

    def test_fix_taxonomy_package_xml(self) -> None:
        """Test the fix_taxonomy_package_xml method.

        This method tests whether the fix_taxonomy_package_xml method generates a taxonomyPackage.xml file
        in the specified source folder.
        """
        with patch('xml.etree.ElementTree.SubElement') as mock_subelement:
            with patch('os.listdir') as mock_listdir:
                self.package_fixer.fix_taxonomy_package_xml('source_folder')
                mock_subelement.assert_called()
                mock_listdir.assert_called()

        return None

    def test_fix_catalog_xml(self) -> None:
        """Test the fix_catalog_xml method.

        This method tests whether the fix_catalog_xml method generates a catalog.xml file
        in the specified source folder.
        """
        with patch('xml.etree.ElementTree.SubElement') as mock_subelement:
            with patch('os.listdir') as mock_listdir:
                self.package_fixer.fix_catalog_xml('source_folder')
                mock_subelement.assert_called()
                mock_listdir.assert_called()

        return None

if __name__ == '__main__':
    unittest.main()

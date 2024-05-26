#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import unittest
# line below ensures that python searhces through all directories for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.classes.TPChecker import TPChecker

class CheckerTest(unittest.TestCase):
    """
    A test class for the TPChecker.
    
    This class contains test methods to validate the functionality of the Checker class
    and ensure its methods work as expected. Each test method is designed to test a specific
    aspect of the Checker's functionality, such as method behavior, error handling, and 
    edge cases.
    """
    
    def test_has_zip_format(self) -> None:
        """Test has_zip_format() function."""
        self.assertTrue(TPChecker().has_zip_format("data/data/example_0.zip"))
        self.assertFalse(TPChecker().has_zip_format("data/data/no_zip_0.txt"))
        self.assertFalse(TPChecker().has_zip_format("data/data/no_zip_1.tar.gz"))
        self.assertFalse(TPChecker().has_zip_format("data/data/no_extension"))
        
        return None

    def test_has_top_level_single_dir(self) -> None:
        """Test has_top_level_single_dir function."""
        # Positive test case with a single top-level directory.
        self.assertTrue(TPChecker().has_top_level_single_dir("data/data/example_0.zip"))
        # Negative test case with multiple top-level directories.
        self.assertFalse(TPChecker().has_top_level_single_dir("data/data/example_0.zip"))
        
        return None

    def test_validate_xml(self) -> None:
        """Test validate_xml function."""
        invalid_xml_path = os.path.join("data", "catalog.xml")
        invalid_xsd_path = "http://www.xbrl.org/2017/taxonomy-package-catalog.xsd"
        # Positive test case with a valid XML document.
        self.assertTrue(TPChecker().validate_xml("http://www.xbrl.org/2016/taxonomy-package-catalog.xsd", invalid_xml_path))
        # Negative test case with an invalid XML document.
        self.assertFalse(TPChecker().validate_xml("http://www.xbrl.org/2016/taxonomy-package-catalog.xsd", invalid_xml_path))
        # Negative test case with an invalid XML schema.
        self.assertFalse(TPChecker().validate_xml(invalid_xsd_path, "https://github.com/FIWARE/test.Functional/blob/master/API.test/security.PDP/8.0.1/catalog.xml"))
        
        return None

    def test_has_taxonomy_package_xml(self) -> None:
        """Test has_taxonomy_package_xml function."""
        archive_with_tp = "data/data/example_0.zip"
        archive_without_tp = "data"
        # Positive test case with a taxonomyPackage.xml file.
        self.assertTrue(TPChecker().has_taxonomy_package_xml(archive_with_tp))
        # Negative test case without a taxonomyPackage.xml file.
        self.assertFalse(TPChecker().has_taxonomy_package_xml(archive_without_tp))
        
        return None


    def test_has_catalog_xml(self) -> None:
        """Test has_catalog_xml function."""
        # Create a temporary directory and sample ZIP archives for testing
        archive_with_catalog = "data/data/example_0.zip"
        archive_without_catalog = "data"
        # Test has_catalog_xml function:
        # Positive test case with a catalog.xml file.
        self.assertTrue(TPChecker().has_catalog_xml(archive_with_catalog))
        # Negative test case without a catalog.xml file.
        self.assertFalse(TPChecker().has_catalog_xml(archive_without_catalog))
        
        return None

if __name__ == '__main__':
    unittest.main()

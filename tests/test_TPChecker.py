#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""test_TPChecker.py"""

import os
import sys
import pytest
# line below ensures that python searhces through all directories for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.checker.TPChecker import TPChecker


def test_has_zip_format():
    """Test the has_zip_format function."""
    checker = TPChecker()
    assert checker.has_zip_format("data/data/example_0.zip")
    assert not checker.has_zip_format("data/data/no_zip_0.txt")
    assert not checker.has_zip_format("data/data/no_zip_1.tar.gz")
    assert not checker.has_zip_format("data/data/no_extension")


def test_has_top_level_single_dir():
    """Test the has_top_level_single_dir function."""
    checker = TPChecker()
    # Positive test case with a single top-level directory.
    assert checker.has_top_level_single_dir("data/data/example_0.zip")
    # Negative test case with multiple top-level directories.
    assert not checker.has_top_level_single_dir("data/data/example_0.zip")


def test_validate_xml():
    """Test the validate_xml function."""
    checker = TPChecker()
    invalid_xml_path = os.path.join("data", "catalog.xml")
    invalid_xsd_path = "http://www.xbrl.org/2017/taxonomy-package-catalog.xsd"
    
    # Positive test case with a valid XML document.
    assert checker.validate_xml("http://www.xbrl.org/2016/taxonomy-package-catalog.xsd", invalid_xml_path)
    # Negative test case with an invalid XML document.
    assert not checker.validate_xml("http://www.xbrl.org/2016/taxonomy-package-catalog.xsd", invalid_xml_path)
    # Negative test case with an invalid XML schema.
    assert not checker.validate_xml(invalid_xsd_path, "https://github.com/FIWARE/test.Functional/blob/master/API.test/security.PDP/8.0.1/catalog.xml")


def test_has_taxonomy_package_xml():
    """Test the has_taxonomy_package_xml function."""
    checker = TPChecker()
    archive_with_tp = "data/data/example_0.zip"
    archive_without_tp = "data"
    
    # Positive test case with a taxonomyPackage.xml file.
    assert checker.has_taxonomy_package_xml(archive_with_tp)
    # Negative test case without a taxonomyPackage.xml file.
    assert not checker.has_taxonomy_package_xml(archive_without_tp)


def test_has_catalog_xml():
    """Test the has_catalog_xml function."""
    checker = TPChecker()
    archive_with_catalog = "data/data/example_0.zip"
    archive_without_catalog = "data"
    
    # Positive test case with a catalog.xml file.
    assert checker.has_catalog_xml(archive_with_catalog)
    # Negative test case without a catalog.xml file.
    assert not checker.has_catalog_xml(archive_without_catalog)


if __name__ == '__main__':
    pytest.main()

#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""test_EDINETFixer.py"""

import os
import sys
import pytest
from unittest.mock import patch
# line below ensures that python searhces through all directories for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.fixers.EDINETFixer import EDINETTaxonomyPackage


@pytest.fixture
def setup_package_fixer():
    """Fixture to set up an instance of EDINETTaxonomyPackage."""
    path_to_zip = "data/archive_single_dir.zip"
    dest_folder = "data"
    return EDINETTaxonomyPackage(path_to_zip, dest_folder)


def test_convert_to_zip_archive(monkeypatch, setup_package_fixer):
    """Test the convert_to_zip_archive method.

    This test ensures that the convert_to_zip_archive method calls `shutil.make_archive`.
    """
    with patch('shutil.make_archive') as mock_make_archive:
        setup_package_fixer.convert_to_zip_archive()
        mock_make_archive.assert_called_once()


def test_fix_top_level_single_dir(monkeypatch, setup_package_fixer):
    """Test the fix_top_level_single_dir method.

    This test ensures that the fix_top_level_single_dir method creates the top-level directory.
    """
    with patch('os.makedirs') as mock_makedirs:
        setup_package_fixer.fix_top_level_single_dir()
        mock_makedirs.assert_called_once()


def test_fix_meta_inf_folder(monkeypatch, setup_package_fixer):
    """Test the fix_meta_inf_folder method.

    This test ensures that the fix_meta_inf_folder method creates the META-INF folder.
    """
    with patch('os.makedirs') as mock_makedirs:
        setup_package_fixer.fix_meta_inf_folder()
        mock_makedirs.assert_called_once()


def test_restructure_folder(monkeypatch, setup_package_fixer):
    """Test the restructure_folder method.

    This test ensures that the restructure_folder method moves files to the root directory.
    """
    with patch('os.listdir') as mock_listdir:
        with patch('os.path.join') as mock_join:
            setup_package_fixer.restructure_folder()
            mock_listdir.assert_called_once_with(setup_package_fixer.destination_folder)
            mock_join.assert_called()


def test_fix_taxonomy_package_xml(monkeypatch, setup_package_fixer):
    """Test the fix_taxonomy_package_xml method.

    This test ensures that the fix_taxonomy_package_xml method generates a taxonomyPackage.xml file.
    """
    with patch('xml.etree.ElementTree.SubElement') as mock_subelement:
        with patch('os.listdir') as mock_listdir:
            setup_package_fixer.fix_taxonomy_package_xml('source_folder')
            mock_subelement.assert_called()
            mock_listdir.assert_called()


def test_fix_catalog_xml(monkeypatch, setup_package_fixer):
    """Test the fix_catalog_xml method.

    This test ensures that the fix_catalog_xml method generates a catalog.xml file.
    """
    with patch('xml.etree.ElementTree.SubElement') as mock_subelement:
        with patch('os.listdir') as mock_listdir:
            setup_package_fixer.fix_catalog_xml('source_folder')
            mock_subelement.assert_called()
            mock_listdir.assert_called()

if __name__ == '__main__':
    pytest.main()

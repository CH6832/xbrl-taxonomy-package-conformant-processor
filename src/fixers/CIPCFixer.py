#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""CIPCFixer.py

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
import re
from io import TextIOWrapper
import shutil
from colorama import Fore
from src.checker.TPChecker import TPChecker
from .TPFixerInterface import TaxonomyPackageFixerInterface
from ..helpers.utils import *

class CIPCTaxonomyPackage(TaxonomyPackageFixerInterface):
    """
    Use this class to fix Attribute 'xlink:href' on locator <link:loc> in all linkbases:
    - iterate over all the linkbase files and replace relative paths
    to IFRS taxonomy schemas with absolute paths.
    - delete the IFRS taxonomy package from the CIPC package. The
    IFRS Taxonomy will be incorporated as a dependency.

    WARNING:
    - Please make sure that no other file or folder is located in the folder where the source
    archive is located.
    - The version in the 'taxonomyPackage.xml' file remains the original,
      but must be changed to <y>.<m> manually.
    """

    def convert_to_zip_archive(self):
        ...

    def fix_top_level_single_dir(self):
        ...

    def fix_meta_inf_folder(self):
        ...

    def fix_taxonomy_package_xml(self):
        ...
    
    def fix_catalog_xml(self):
        ...

    def restructure_folder(self):

        def _get_package_version() -> str:
            """Get the package version"""
            return ""

        def __get_full_path_of_all_xsd_files() -> list:
            """Locate and get full path to all xsd schema files
            relevant for substring replacement and return a list.
            """
            full_path_to_schema_files: list = []
            root_folder: str = self.destination_folder
            for subdir, dirs, files in os.walk(root_folder):
                for file in files:
                    if file.endswith(".xsd") and not 'catalog' in file and not 'taxonomyPackage' in file:
                        xsd_file = os.path.join(subdir, file)
                        full_path_to_schema_files.append(xsd_file)
            return full_path_to_schema_files

        def __get_full_path_to_allxml_files():
            """Locate and get full path to all xml files relevant
            for substring replacement.
            """
            list_full_path_xml_files = []
            root_folder = self.destination_folder
            subdir: str
            files: list[ str ]
            for subdir, dirs, files in os.walk(root_folder):
                file: str
                for file in files:
                    if file.endswith(".xml") and not 'catalog' in file and not 'taxonomyPackage' in file:
                        xml_file: str = os.path.join(subdir, file)
                        list_full_path_xml_files.append(xml_file)
            return list_full_path_xml_files

        def __replace_substring_in_property_value(
            affected_xml_file, int_prop_1 = 0, int_prop_2 = 0,  substring1 = "", substring2 = "", obj_iterator = "", str_elem_href = "", repl_str_1 = "", repl_str_2 = "", tree= 0,  xml_f= "") -> None:
            """Replace substring in affected linkbase if relevant conditions are true
            and write it back to the xml file.

            Keyword arguments:
            affected_xml_file -- name of affected xml file by changes
            int_prop_1 -- initial value of substring
            int_prop_2 -- end value of substring
            substring1 -- condition for finding the xml file
            substring2 -- condition for finding the xml file
            obj_iterator -- iterator object
            str_elem_href -- value of href element in xml file
            repl_str_1 -- substring to be replaced
            repl_str_2 -- substitution for substring1
            tree -- tree of elements in xml file
            xml_f -- name of xml file to be manipulated

            Example with inserted parameters:
            if affected_xml_file[ 0:8] == "../../.." and "/def/ifrs/ifrs_for_smes" in affected_xml_file:
                hrefValueFixed1 = loc.get("{http://www.w3.org/1999/xlink}href").replace("../../../def/ifrs", "http://xbrl.ifrs.org/taxonomy/2021-03-24")
                loc.set("{http://www.w3.org/1999/xlink}href",hrefValueFixed1)
                print("Filename: " + xml_f+ ", Fixed value: " +hrefValueFixed1)
                tree.write(xml_f)
            """
            if affected_xml_file[ int_prop_1 : int_prop_2 ] == substring1 and substring2 in affected_xml_file:
                fixed_value_var_name = obj_iterator.get(str_elem_href).replace(repl_str_1 , repl_str_2)
                obj_iterator.set(str_elem_href,fixed_value_var_name)
                tree.write(xml_f)
                return

        def __replace_substring_in_schema_file(
            substring_1 = "", loc = "", elem_name_1 = "", replace_substr_1 = "", replace_substr_2 = "", xsd_f = "", tree = "") -> None:
            """Replace substring in affected schema file if relevant conditions are true
            and write it back to the xml file.
            
            Keyword arguments:
            substring_1 -- condition for finding the xml file
            loc -- iterator
            elem_name -- element name
            replace_substr_1 -- substring to be replaced
            replace_substr_2 -- replace_substr_1
            xsd_f -- name of xml file to be manipulated
            tree -- tree of elements in xml file

            Example with inserted parameters:
            if "../../../../def/ifrs/full_ifrs/" in loc.get("schemaLocation"):
                schema_value_fixed_1 = loc.get("schemaLocation").replace("../../../../def/ifrs", "http://xbrl.ifrs.org/taxonomy/2021-03-24")
                loc.set("schemaLocation", schema_value_fixed_1)
                print("Filename: " + xsd_f+ ", Fixed value: " +schema_value_fixed_1)
                tree.write(xsd_f)
            """
            if substring_1 in loc.get(elem_name_1):
                schema_value_fixed_1: str = loc.get(elem_name_1).replace(replace_substr_1, replace_substr_2)
                loc.set("schemaLocation", schema_value_fixed_1)
                tree.write(xsd_f)

        # print(f"Fixing '{ self.full_path_to_zip.name }' ... Log file can be found in 'C:/Projects/xmldata/scripts/{ self.full_path_to_zip.name.replace('.zip', '') }_std.log'")

        str_elem_href: str = "{http://www.w3.org/1999/xlink}href"
        str_elem_loc: str = "{http://www.xbrl.org/2003/linkbase}loc"
        str_elem_schema_loc: str = '{http://www.w3.org/2001/XMLSchema}import'
        str_attribute_schema_import: str = 'schemaLocation'

        ns: dict[ str, str ] = {
            "gen":"http://xbrl.org/2008/generic",
            "label":"http://xbrl.org/2008/label",
            "link":"http://www.xbrl.org/2003/linkbase",
            "validation":"http://xbrl.org/2008/validation",
            "xlink":"http://www.w3.org/1999/xlink",
            "xsi":"http://www.w3.org/2001/XMLSchema-instance"
            }
        prefix: str
        uri: str
        for prefix, uri in ns.items():
            ET.register_namespace(prefix, uri)
    
        # remove integrated IFRS taxonomy
        dir_with_ifrs_contained: str = ""
        for directory, subdirs, files in os.walk(self.destination_folder) :
            if r'def\ifrs' in directory:
                dir_with_ifrs_contained = directory
                shutil.rmtree(dir_with_ifrs_contained)
                break

        # retrieve entry point and linkbase date
        # affected_xml_file: str = ""
        # xml_file: str
        # full_path_of_all_xml_files = __get_full_path_to_allxml_files()
        # for xml_file in full_path_of_all_xml_files:
        #     tree = ET.parse(xml_file)
        #     root = tree.getroot()
        #     loc: str
        #     for loc in root.iter(str_elem_loc):
        #         print(loc.get(str_elem_href))
        #         if "/def/ifrs/full_ifrs" in loc.get(str_elem_href) or "/def/ifrs/ifrs_for_smes" in loc.get(str_elem_href) or "/def/ifrs/deprecated" in loc.get(str_elem_href):
        #             affected_xml_file = loc.get(str_elem_href)
        #             break

        # First round is to change URLs from relative to absolute paths
        # -------------------------------------------------------------
        xml_f: str
        full_path_of_all_xml_files = __get_full_path_to_allxml_files()
        for xml_f in full_path_of_all_xml_files:
            print(xml_f)
            tree: ET.ElementTree = ET.parse(xml_f)
            root = tree.getroot()
            loc: str
            for loc in root.iter(str_elem_loc):
                print(loc.attrib.get(str_elem_href))
                if "/def/ifrs/full_ifrs" in loc.get(str_elem_href) or "/def/ifrs/ifrs_for_smes" in loc.get(str_elem_href) or "/def/ifrs/deprecated" in loc.get(str_elem_href):
                    affected_xml_file = loc.get(str_elem_href)
                    affected_xml_file_date_pattern: re.compile = re.search(r'\d{4}-\d{2}-\d{2}', affected_xml_file)
                    affected_xml_file_date: str = str(affected_xml_file_date_pattern.group())
                    __replace_substring_in_property_value(affected_xml_file, 0, 8, "../../..", "/def/ifrs/ifrs_for_smes", loc, "{http://www.w3.org/1999/xlink}href", "../../../def/ifrs", "https://xbrl.ifrs.org/taxonomy/" + affected_xml_file_date, tree, xml_f)
                    __replace_substring_in_property_value(affected_xml_file, 0, 11, "../../../..", "/def/ifrs/ifrs_for_smes", loc, "{http://www.w3.org/1999/xlink}href", "../../../../def/ifrs", "https://xbrl.ifrs.org/taxonomy/" + affected_xml_file_date, tree, xml_f)
                    __replace_substring_in_property_value(affected_xml_file, 0, 8, "../../..", "/def/ifrs/full_ifrs", loc, "{http://www.w3.org/1999/xlink}href", "../../../def/ifrs", "https://xbrl.ifrs.org/taxonomy/" + affected_xml_file_date, tree, xml_f)
                    __replace_substring_in_property_value(affected_xml_file, 0, 14, "../../../../..", "/def/ifrs/full_ifrs", loc, "{http://www.w3.org/1999/xlink}href", "../../../../def/ifrs", "https://xbrl.ifrs.org/taxonomy/" + affected_xml_file_date, tree, xml_f)
                    __replace_substring_in_property_value(affected_xml_file, 0, 8, "../../..", "/def/ifrs/deprecated/", loc, "{http://www.w3.org/1999/xlink}href", "../../../def/ifrs", "https://xbrl.ifrs.org/taxonomy/" + affected_xml_file_date, tree, xml_f)
                    __replace_substring_in_property_value(affected_xml_file, 0, 11, "../../../..", "/def/ifrs/deprecated/", loc, "{http://www.w3.org/1999/xlink}href", "../../../../def/ifrs", "https://xbrl.ifrs.org/taxonomy/" + affected_xml_file_date, tree, xml_f)

            # Second round is deleting the strings from the rest of the URLs
            # --------------------------------------------------------------
            loc: str
            for loc in root.iter('{http://www.xbrl.org/2003/linkbase}loc'):
                if "/full_ifrs/" in loc.get("{http://www.w3.org/1999/xlink}href") or "/ifrs_for_smes/" in loc.get("{http://www.w3.org/1999/xlink}href") or "/deprecated/" in loc.get("{http://www.w3.org/1999/xlink}href"):
                    affected_xml_file = loc.get("{http://www.w3.org/1999/xlink}href")
                    __replace_substring_in_property_value(affected_xml_file, 0, 3, "../", "../h", loc, "{http://www.w3.org/1999/xlink}href", "../", "",tree, xml_f)

        # Third round is the fixing of the entries in the XSD schema files
        # ----------------------------------------------------------------
        xsd_f: str
        for xsd_f in __get_full_path_of_all_xsd_files():
            affected_xsd_file_date_pattern: re.compile = re.search(r'\d{4}-\d{2}-\d{2}', affected_xml_file)
            affected_xsd_file_date: str = str(affected_xsd_file_date_pattern.group())
            xsd_tree: ET.ElementTree = ET.parse(xsd_f)
            xsd_root = xsd_tree.getroot()
            xsd_loc: str
            for xsd_loc in xsd_root.iter(str_elem_schema_loc):
                if "../../../../def/ifrs/full_ifrs" in xsd_loc.get(str_attribute_schema_import):
                    __replace_substring_in_schema_file("../../../../def/ifrs/full_ifrs", xsd_loc, str_attribute_schema_import, "../../../../def/ifrs/full_ifrs", "https://xbrl.ifrs.org/taxonomy/" + affected_xsd_file_date+ "/full_ifrs", xsd_f, xsd_tree)
                elif "../../def/ifrs/full_ifrs" in xsd_loc.get(str_attribute_schema_import):
                    __replace_substring_in_schema_file("../../def/ifrs/full_ifrs", xsd_loc, str_attribute_schema_import, "../../def/ifrs/full_ifrs", "https://xbrl.ifrs.org/taxonomy/" + affected_xsd_file_date+ "/full_ifrs", xsd_f, xsd_tree)
                elif "../../../../def/ifrs/ifrs_for_smes" in xsd_loc.get(str_attribute_schema_import):
                    __replace_substring_in_schema_file("../../../../def/ifrs/ifrs_for_smes", xsd_loc, str_attribute_schema_import, "../../../../def/ifrs/ifrs_for_smes", "https://xbrl.ifrs.org/taxonomy/" + affected_xsd_file_date+ "/ifrs_for_smes", xsd_f, xsd_tree)
                elif "../../def/ifrs/ifrs_for_smes" in xsd_loc.get(str_attribute_schema_import):
                    __replace_substring_in_schema_file("../../def/ifrs/ifrs_for_smes", xsd_loc, str_attribute_schema_import, "../../def/ifrs/ifrs_for_smes", "https://xbrl.ifrs.org/taxonomy/" + affected_xsd_file_date+ "/ifrs_for_smes", xsd_f, xsd_tree)

        # os.remove(self.path_to_package)
        # shutil.make_archive(self.path_to_package.replace(".zip", ""), "zip", self.source_folder, self.zip_archive.replace(".zip", ""))
        # shutil.rmtree(self.path_to_package.replace(".zip", ""))

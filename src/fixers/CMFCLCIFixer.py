#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""CMFCLCIFixer.py

The module contains classes with relevant methods to fix
xbrl taxonomy packages based by certain providers.
"""

import os
import sys
# line below ensures that python searhces through all directories for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from xml.dom.minidom import parseString
import xml.etree.ElementTree as ET
import zipfile
from io import TextIOWrapper
from datetime import datetime
import shutil
import glob
import re
from colorama import Fore
from src.checker.TPChecker import TPChecker
from .TPFixerInterface import TaxonomyPackageFixerInterface
from ..helpers.utils import *

class CMFCLCITaxonomyPackage(TaxonomyPackageFixerInterface):
    """
    Use this class to fix the CMF CL-CI raw building block. Example download can be found here:
    https://www.cmfchile.cl/portal/principal/613/w3-propertyvalue-43598.html#especial_taxonomias
    NOTE: Make sure, that no other file, etc is located in source folder!
    """

    def restructure_folder(self) -> None:
        # remove source file
        os.remove(os.path.join(self.destination_folder, os.path.basename(str(self.full_path_to_zip).replace("input","output"))))
        # create a folder called files in source folder
        os.makedirs(os.path.join(self.destination_folder, "files"))
        # iterate over all files and folders and put all of the into
        # the "files" folder apart from the "META-INF" folder
        for item in os.listdir(self.destination_folder):
            item_path = os.path.join(self.destination_folder, item)
            if item == 'META-INF' or item == 'files':
                continue
            shutil.move(item_path, os.path.join(self.destination_folder, "files"))
        
        return None


    def fix_meta_inf_folder(self) -> None:
        os.makedirs(os.path.join(self.destination_folder, "META-INF"))
        print_color_msg(f"    META-INF directory generated",Fore.YELLOW)
        
        return None


    def convert_to_zip_archive(self) -> None:
        
        return None

    def fix_top_level_single_dir(self) -> None:
        os.makedirs(os.path.join(self.destination_folder, os.path.basename(self.full_path_to_zip).replace(".zip","")), exist_ok = True)
        print_color_msg(f"    Top level directory generated",Fore.YELLOW)
        
        return None


    def fix_taxonomy_package_xml(self, source_folder: str) -> None:
        """2. Design and generate the 'taxonomyPackage.xml' file.
        """

        def __extract_entry_points():
            """1. Extract necessary entry points from the specified folder.
            """
            self.entry_points = []  # Ensure entry_points is defined
            ns = {
                'link': 'http://www.xbrl.org/2003/linkbase',
                'xs': 'http://www.w3.org/2001/XMLSchema'
            }

            for taxonomy_schema in glob.glob(os.path.join(source_folder, '**/*.xsd'), recursive=True):
                if taxonomy_schema:
                    tree = ET.parse(taxonomy_schema)
                    root = tree.getroot()

                    if root.findall(".//xs:appinfo/link:linkbase[@id='lnk']", ns) or root.findall(".//xs:appinfo/link:linkbaseRef", ns):
                        if taxonomy_schema not in self.entry_points:
                            rel_entrypoint_path = taxonomy_schema.replace(self.destination_folder,"")
                            self.entry_points.append(rel_entrypoint_path)
                else:
                    print("No catalog entry found for entry point")

            return self.entry_points


        # Version Pattern for year and/or months and/or day
        yearMonthDaySearchPattern = re.search(r'\d{4}-\d{2}-\d{2}', source_folder)
        yearMonthSearchPattern = re.search(r'\d{4}-\d{2}', source_folder)
        yearSearchPattern = re.search(r'\d{4}', source_folder)
        # tp:version
        tpVersion: str = ""
        if yearMonthDaySearchPattern is not None:
            tpVersion = str(yearMonthDaySearchPattern.group())
        elif yearMonthSearchPattern is not None:
            tpVersion = str(yearMonthSearchPattern.group())
        elif yearSearchPattern is not None:
            tpVersion = str(yearSearchPattern.group())
        else:
            # print(colored(f"Search Pattern not defined for : { self.__get_new_zip_archive_name() }", "red"))
            print_color_msg(f"    taxonomyPackage.xml file generated",Fore.YELLOW)

        xml_pkg: ET.Element = ET.Element("tp:taxonomyPackage")
        xml_pkg.set('xml:lang', 'en')
        xml_pkg.set('xmlns:tp', 'http://xbrl.org/2016/taxonomy-package')
        xml_pkg.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        xml_pkg.set('xsi:schemaLocation', 'http://xbrl.org/2016/taxonomy-package http://xbrl.org/2016/taxonomy-package.xsd')
        xml_pkg.append(ET.Comment('This file and its content has been generated and is not part of the original ZIP.')) 

        elem: ET.Element
        elem = ET.SubElement(xml_pkg, 'tp:identifier')
        elem.text = source_folder

        elem = ET.SubElement(xml_pkg, 'tp:name')
        elem.text = source_folder.replace(".zip", "").replace("-" +tpVersion, "") + " XBRL Taxonomy"

        elem = ET.SubElement(xml_pkg, 'tp:description')
        if "CMF" in str(source_folder):
            elem.text = "Expanded IFRS " + "2020" + " taxonomy with additional Chilean regulations added"

        elem = ET.SubElement(xml_pkg, 'tp:version')
        elem.text = tpVersion

        elem = ET.SubElement(xml_pkg, 'tp:publisher')
        if "CMF" in str(source_folder):
            elem.text = "Comision para el Mercado Financiero"

        elem = ET.SubElement(xml_pkg, 'tp:publisherURL')
        if "CMF" in str(source_folder):
            elem.text = "https://www.cmfchile.cl/portal/principal/613/w3-channel.html"

        elem = ET.SubElement(xml_pkg, 'tp:publicationDate')
        elem.text = tpVersion

        xmlEPs: ET.Element
        xmlEPs = ET.SubElement(xml_pkg, 'tp:entryPoints')
        all_entrypoints = __extract_entry_points()
        for schemaName in all_entrypoints:
            xmlEP = ET.SubElement(xmlEPs, 'tp:entryPoint')

            elemName = ET.SubElement(xmlEP, 'tp:name')
            elemName.text = os.path.basename(schemaName).replace("_", "-").replace(".xsd", "")

            epFileName: str = os.path.basename(schemaName)
            fullEPDate = re.search(r'\d{4}-\d{2}-\d{2}', epFileName)
            if fullEPDate is not None:
                epVersion = str(fullEPDate.group())

                elemVersion: ET.Element = ET.SubElement(xmlEP, 'tp:version')
                elemVersion.text = epVersion

            # if "CMF" in self.__get_new_path_to_package():
            x = "http://www.cmfchile.cl/cl/fr/ci/" + tpVersion + schemaName.replace("CL_CI_2020", "").replace("CMF-CL-CI-" +tpVersion, "").replace("\\","/")
            ET.SubElement(xmlEP, 'tp:entryPointDocument', { 'href': x})

        str_xml_pkg = parseString(ET.tostring(xml_pkg, 'utf-8')) .toprettyxml(indent='    ')

        if os.path.isfile(source_folder + '/' + 'META-INF' + '/' + 'taxonomyPackage.xml') is False:
            tp_xml_file: TextIOWrapper
            with open(os.path.join(source_folder + '/' + 'META-INF', 'taxonomyPackage.xml').replace("\\", "/"), "w", encoding='utf-8') as tp_xml_file:
                tp_xml_file.write(str_xml_pkg)
            tp_xml_file.close()
        else:
            pass

        return None


    def fix_catalog_xml(self, source_folder: str) -> None:
        """5. Design and generate the 'catalog.xml'."""

        def __get_package_version() -> str:
            """Generates the package version number. Assumption that in
            cl-ci_cor_* schema, the version is always contained, but any other
            file can be used for it.
            """
            source_schema_file_name = ""
            for filename in os.listdir(source_folder):
                file = os.path.join(source_folder, filename)
                if file.endswith(".xsd") and "_cor_" in file:
                    source_schema_file_name = file
                    break
                else:
                    continue

        # Design the file:
        xml_catalog_elements: ET.Element = ET.Element("catalog")
        xml_catalog_elements.set('xmlns', 'urn:oasis:names:tc:entity:xmlns:xml:catalog')
        xml_catalog_elements.set('xmlns:spy', 'http://www.altova.com/catalog_ext')
        xml_catalog_elements.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        xml_catalog_elements.set('xsi:schemaLocation', 'urn:oasis:names:tc:entity:xmlns:xml:catalog Catalog.xsd')

        archive_name_year = re.search(r'\d{4}', "2020-01-02")
        if archive_name_year is not None:
            cat_entry_version = str(archive_name_year.group())
        else:
            print("ERROR: Pattern for year not found!")

        ET.SubElement(xml_catalog_elements, 'rewriteURI', { 'uriStartString': 'http://www.cmfchile.cl/cl/fr/ci/' + "2020-01-02" + '/', 'rewritePrefix': '../CL-CI-' + cat_entry_version + '/' })

        str_xml_c = parseString(ET.tostring(xml_catalog_elements, 'utf-8' )).toprettyxml(indent='    ')

        # Generate the file.
        if os.path.isfile(source_folder + '/' + 'META-INF' + '/' + 'catalog.xml') is False:
            with open(os.path.join(source_folder + '/' + 'META-INF', "catalog.xml").replace("\\", "/"), "w", encoding='utf-8') as catalog_xml_file:
                catalog_xml_file.write(str_xml_c)
            catalog_xml_file.close()
        else:
            # print(colored("WARNING: 'catalog.xml' file already exists!", "yellow"))
            print_color_msg(f"WARNING: 'catalog.xml' file already exists!",Fore.YELLOW)

        return None

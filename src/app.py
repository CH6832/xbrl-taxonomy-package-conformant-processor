#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""app.py

Main program and entry point.
"""

import os
import sys
from typing import Any, Literal
# line below ensures that python searhces through all directories for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.helpers.logger import set_logging_directory, setup_logger
import argparse
import shutil
from pathlib import Path
from colorama import Fore, init
from src.checker.TPChecker import TPChecker
from src.fixers.EBAFixer import EBATaxonomyPackage
from src.fixers.EDINETFixer import EDINETTaxonomyPackage
from src.fixers.CMFCLCIFixer import CMFCLCITaxonomyPackage
from src.fixers.CIPCFixer import CIPCTaxonomyPackage
from src.helpers.utils import *
from src.enums.Providers import Provider


log_file_path = set_logging_directory(r'..\logs', log_filename="app.log")
logger = setup_logger(__name__, log_file=log_file_path)

def main() -> None:
    """Driving code."""
    # intialize the colorama module
    init(autoreset=True)
    
    # catch exception if there are errors in parsed arguments
    try:
        provider, package = parse_arguments()
    except:
        error_message = f"""Please provide both: Abbreveation of provider and full path to taxonomy package (zip):
{os.path.basename(__file__)} EBA '..\\input\\ALL_20221101\\ALL_20221101.zip'"""
        raise SystemExit(print_color_msg(f"Error: {error_message}",Fore.RED))
    logger.error("Please provide both: Abbreveation of provider (str.upper()) and full path to taxonomy package (zip).")

    # print out provider and path to package to make
    # user aware of what was passed to the tool
    print_color_msg(f"Input information:",Fore.BLUE)
    print_color_msg(f"-"*18,Fore.BLUE)
    print_color_msg(f"    Provider -> {provider}",Fore.BLUE)
    print_color_msg(f"    Package  -> {package}\n",Fore.BLUE)

    tp_checker = TPChecker()

    # Prepare source and destination paths
    source_zip_path = Path(os.path.abspath(package))
    destination_folder = Path(str(source_zip_path).replace("input", "output").replace(f"\\{os.path.basename(package)}", ""))

    # Check the package.
    checks = check_package(tp_checker, package)

    # Prepare source and destination path
    provider_map = {
        Provider.EBA: EBATaxonomyPackage,
        Provider.EDINET: EDINETTaxonomyPackage,
        Provider.CMFCLCI: CMFCLCITaxonomyPackage,
        Provider.CIPC: CIPCTaxonomyPackage
    }

    try:
        provider_enum = Provider(provider)
    except ValueError:
        print_color_msg(f"\nERROR: Wrong provider!", Fore.RED)
        logger.error("ERROR: Wrong provider!")
        return

    print_color_msg(f"\nFixing package...", Fore.YELLOW)
    fix_package(provider_enum.value, provider_map[provider_enum], source_zip_path, destination_folder, checks)

    return None


def parse_arguments():
    """Parse command-line arguments."""
    # initialize argument parser and set arguments for the cmdl
    parser = argparse.ArgumentParser(description="A simple cmdl tool to fix XBRL Taxonomy Packages.")
    parser.add_argument("provider", help="Provide abbreviation of official provider (e.g. EBA, EDINET, etc.).")
    parser.add_argument("package", help="Full path to the taxonomy_package_name.zip.")
    
    args = parser.parse_args()

    return args.provider.upper(), args.package


def check_package(tp_checker, package) -> tuple[Any, Any | Literal[False], Any]:
    """Perform all package checks."""
    ZIP_FORMAT = tp_checker.has_zip_format(package)
    SINGLE_DIR = tp_checker.has_top_level_single_dir(package) if ZIP_FORMAT else False
    METAINF_DIR = tp_checker.has_meta_inf_folder(package) and \
                  tp_checker.has_catalog_xml(package) and \
                  tp_checker.has_taxonomy_package_xml(package)

    # Print the results of the checks
    print_color_msg(f"    {'DONE' if ZIP_FORMAT else 'ERROR'}: Package is {'ZIP' if ZIP_FORMAT else 'not ZIP'}", Fore.GREEN if ZIP_FORMAT else Fore.RED)
    print_color_msg(f"    {'DONE' if SINGLE_DIR else 'ERROR'}: Package has {'toplevel dir' if SINGLE_DIR else 'no single toplevel dir'}", Fore.GREEN if SINGLE_DIR else Fore.RED)
    print_color_msg(f"    {'DONE' if METAINF_DIR else 'ERROR'}: Package has {'META-INF folder' if METAINF_DIR else 'no META-INF folder or required files'}", Fore.GREEN if METAINF_DIR else Fore.RED)

    return ZIP_FORMAT, SINGLE_DIR, METAINF_DIR


def fix_package(provider_name, package_class, source_zip_path, destination_folder, checks) -> None:
    """Fix the package by applying necessary corrections based on the provider."""
    ZIP_FORMAT, SINGLE_DIR, METAINF_DIR = checks
    fixer = package_class(source_zip_path, destination_folder)

    # Apply fixes based on the results of the checks.
    if not ZIP_FORMAT:
        fixer.convert_to_zip_archive()
    if not METAINF_DIR:
        fixer.fix_meta_inf_folder()
    if not SINGLE_DIR:
        fixer.fix_top_level_single_dir()

    # Restructure the package folder
    fixer.restructure_folder()
    # Regenerate necessary XML files.
    fixer.fix_catalog_xml()
    fixer.fix_taxonomy_package_xml()

    # Generate the final ZIP archive in the destination folder.
    full_path_to_zip = str(source_zip_path).replace("input", "output")
    gen_zip_archive(destination_folder, full_path_to_zip)

    # Clean up by removing the temporary working directories after the ZIP is created.
    shutil.rmtree(destination_folder)

    # Output the result to the user
    print_color_msg(f"\nOutput result:", Fore.BLUE)
    print_color_msg(f"    {os.path.basename(full_path_to_zip)} is fixed", Fore.BLUE)
    logger.info("Output result: %s", os.path.basename(full_path_to_zip))

    return None


if __name__ == "__main__":
    main()

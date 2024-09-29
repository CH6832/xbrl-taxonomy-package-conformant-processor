#pragma once

#ifndef EDINETTAXONOMYPACKAGEFIXER_HPP
#define EDINETTAXONOMYPACKAGEFIXER_HPP

#include <string>
#include <vector>
#include <filesystem>
#include <iostream>
#include <fstream>
#include <memory>
#include <libxml/xmlmemory.h>
#include <libxml/parser.h>
#include <libxml/tree.h>
#include <libxml/xmlschemas.h>
#include "TPFixerInterface.hpp"

/**
 * @brief Interface for taxonomy package fixer classes.
 */
class TaxonomyPackageFixerInterface {
public:
    virtual void convert_to_zip_archive() = 0;
    virtual void fix_meta_inf_folder() = 0;
    virtual void fix_top_level_single_dir() = 0;
    virtual void restructure_folder() = 0;
    virtual void fix_taxonomy_package_xml(const std::string& source_folder) = 0;
    virtual void fix_catalog_xml(const std::string& source_folder) = 0;
};

/**
 * @brief Class to fix an EDINET XBRL Taxonomy Package.
 *
 * The package can be found in the input/* folder as well as
 * newer and older versions at:
 * https://disclosure2.edinet-fsa.go.jp/weee0020.aspx
 */
class EDINETTaxonomyPackage : public TPFixerInterface {
public:
    /**
     * @brief Constructor for EDINETTaxonomyPackage.
     */
    EDINETTaxonomyPackage(const std::string& destinationFolder, const std::string& fullPathToZip);

    void convert_to_zip_archive() override;
    void fix_meta_inf_folder();
    void fix_top_level_single_dir();
    void restructure_folder();
    void fix_taxonomy_package_xml(const std::string& source_folder);
    void fix_catalog_xml(const std::string& source_folder);

private:
    std::string destination_folder; /**< Destination folder for the package */
    std::string full_path_to_zip;   /**< Full path to the zip file */

    /**
     * @brief Prints a color message to the console.
     *
     * @param message The message to print.
     * @param color The color of the message.
     */
    void print_color_msg(const std::string& message, const std::string& color);
};

#endif // EDINETTAXONOMYPACKAGEFIXER_HPP

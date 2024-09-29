#pragma once

#ifndef CMFCLCITAXONOMYPACKAGEFIXER_HPP
#define CMFCLCITAXONOMYPACKAGEFIXER_HPP

#include <string>
#include <vector>
#include <filesystem>
#include <libxml/parser.h>
#include <libxml/tree.h>
#include <iostream>
#include <fstream>
#include <regex>
#include <zip.h>
#include "TPFixerInterface.hpp"

class CMFCLCITaxonomyPackage {
public:
    /**
     * Constructor for CMFCLCITaxonomyPackage
     *
     * @param full_path_to_zip Full path to the zip file
     * @param destination_folder Destination folder for output
     */
    CMFCLCITaxonomyPackage(const std::string& full_path_to_zip, const std::string& destination_folder)
        : full_path_to_zip(full_path_to_zip), destination_folder(destination_folder) {}

    void restructure_folder();
    void fix_meta_inf_folder();
    void convert_to_zip_archive();
    void fix_top_level_single_dir();
    void fix_taxonomy_package_xml(const std::string& source_folder);
    void fix_catalog_xml(const std::string& source_folder);

private:
    std::vector<std::string> entry_points;
    std::string full_path_to_zip;
    std::string destination_folder;

    /**
     * Extracts necessary entry points from the specified folder.
     *
     * @param source_folder The folder to extract entry points from
     * @return A vector of entry point paths
     */
    std::vector<std::string> extract_entry_points(const std::string& source_folder);

    /**
     * Prints colored messages to the console.
     *
     * @param message The message to print
     * @param color The color for the message
     */
    void print_color_msg(const std::string& message, const std::string& color);
};

#endif // CMFCLCITAXONOMYPACKAGEFIXER_HPP

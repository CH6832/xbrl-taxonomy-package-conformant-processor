#include "../../includes/CMFCLCIFixer.hpp"
#include <iostream>
#include <fstream>
#include <filesystem>
#include <libxml/xmlmemory.h>
#include <libxml/parser.h>
#include <libxml/tree.h>
#include <regex>
#include <sstream>

namespace fs = std::filesystem;

void CMFCLCITaxonomyPackage::restructure_folder() {
    fs::path destination_path = fs::path(destination_folder);
    fs::path output_file = destination_path / fs::path(fs::path(full_path_to_zip).filename().string().replace("input", "output"));

    if (fs::exists(output_file)) {
        fs::remove(output_file);
    }

    fs::create_directory(destination_path / "files");

    for (const auto& item : fs::directory_iterator(destination_path)) {
        if (item.path().filename() == "META-INF" || item.path().filename() == "files") {
            continue;
        }
        fs::rename(item.path(), destination_path / "files" / item.path().filename());
    }
}

void CMFCLCITaxonomyPackage::fix_meta_inf_folder() {
    fs::create_directory(fs::path(destination_folder) / "META-INF");
    print_color_msg("META-INF directory generated", "\033[33m"); // Yellow
}

void CMFCLCITaxonomyPackage::convert_to_zip_archive() {
    // Placeholder for zip conversion implementation
}

void CMFCLCITaxonomyPackage::fix_top_level_single_dir() {
    fs::create_directory(fs::path(destination_folder) / fs::path(full_path_to_zip).filename().replace_extension(""));
    print_color_msg("Top level directory generated", "\033[33m"); // Yellow
}

std::vector<std::string> CMFCLCITaxonomyPackage::extract_entry_points(const std::string& source_folder) {
    entry_points.clear();
    std::regex ns_regex("http://www\\.w3\\.org/2001/XMLSchema");
    for (const auto& taxonomy_schema : fs::recursive_directory_iterator(source_folder)) {
        if (taxonomy_schema.path().extension() == ".xsd") {
            // Load XML and check for entry points
            xmlDocPtr doc = xmlReadFile(taxonomy_schema.path().string().c_str(), NULL, 0);
            if (doc == NULL) {
                continue;
            }
            xmlNodePtr root = xmlDocGetRootElement(doc);
            // Check for entry points here (using XPath or manual traversal)
            // Simplified: Assume we find the entry points based on some logic
            std::string rel_entrypoint_path = taxonomy_schema.path().string();
            entry_points.push_back(rel_entrypoint_path);
            xmlFreeDoc(doc);
        }
    }
    return entry_points;
}

void CMFCLCITaxonomyPackage::fix_taxonomy_package_xml(const std::string& source_folder) {
    std::string tpVersion;

    std::smatch match;
    if (std::regex_search(source_folder, match, std::regex("\\d{4}-\\d{2}-\\d{2}"))) {
        tpVersion = match.str();
    }
    else if (std::regex_search(source_folder, match, std::regex("\\d{4}-\\d{2}"))) {
        tpVersion = match.str();
    }
    else if (std::regex_search(source_folder, match, std::regex("\\d{4}"))) {
        tpVersion = match.str();
    }

    // Construct XML document
    xmlDocPtr doc = xmlNewDoc(BAD_CAST "1.0");
    xmlNodePtr root = xmlNewNode(NULL, BAD_CAST "tp:taxonomyPackage");
    xmlDocSetRootElement(doc, root);
    xmlNewProp(root, BAD_CAST "xml:lang", BAD_CAST "en");
    xmlNewProp(root, BAD_CAST "xmlns:tp", BAD_CAST "http://xbrl.org/2016/taxonomy-package");
    xmlNewProp(root, BAD_CAST "xmlns:xsi", BAD_CAST "http://www.w3.org/2001/XMLSchema-instance");
    xmlNewProp(root, BAD_CAST "xsi:schemaLocation", BAD_CAST "http://xbrl.org/2016/taxonomy-package http://xbrl.org/2016/taxonomy-package.xsd");
    xmlNodeAddContent(root, BAD_CAST "This file and its content has been generated and is not part of the original ZIP.");

    // More XML element creation omitted for brevity...

    // Output XML to file
    fs::path output_file = fs::path(source_folder) / "META-INF" / "taxonomyPackage.xml";
    if (!fs::exists(output_file)) {
        xmlSaveFormatFileEnc(output_file.string().c_str(), doc, "UTF-8", 1);
    }
    xmlFreeDoc(doc);
}

void CMFCLCITaxonomyPackage::fix_catalog_xml(const std::string& source_folder) {
    // Placeholder for catalog XML fixing logic
}

void CMFCLCITaxonomyPackage::print_color_msg(const std::string& message, const std::string& color) {
    std::cout << color << message << "\033[0m" << std::endl; // Reset color
}

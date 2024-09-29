#include "../../includes/EDINETFixer.hpp"
#include <filesystem>
#include <iostream>
#include <sstream>
#include <zlib.h>
#include <libxml/xmlmemory.h>
#include <libxml/parser.h>
#include <libxml/tree.h>
#include <libxml/xmlschemas.h>

/**
 * @brief Constructor for EDINETTaxonomyPackage.
 *
 * @param destinationFolder The folder where the package will be processed.
 * @param fullPathToZip The full path to the zip file.
 */
EDINETTaxonomyPackage::EDINETTaxonomyPackage(const std::string& destinationFolder, const std::string& fullPathToZip)
    : destination_folder(destinationFolder), full_path_to_zip(fullPathToZip) {}

/**
 * @brief Converts the taxonomy package to a zip archive.
 */
void EDINETTaxonomyPackage::convert_to_zip_archive() {
    // Use zlib to create a zip archive
    // Note: This is a simplified example. You'll need a proper ZIP library
    // for creating ZIP files. This function should use a library that
    // implements the ZIP file format, like miniz or libarchive.

    std::ostringstream zipStream; // Placeholder for ZIP archive content
    // Code to create ZIP file using zlib goes here...
    // Example: write compressed data to zipStream

    std::ofstream zipFile(full_path_to_zip, std::ios::binary);
    if (zipFile) {
        // Write compressed data to zip file
        zipFile << zipStream.str();
        zipFile.close();
    }

    print_color_msg("    Zip archive created", "yellow");
}

/**
 * @brief Fixes the top-level single directory.
 */
void EDINETTaxonomyPackage::fix_top_level_single_dir() {
    std::string newDir = destination_folder + "/" + std::filesystem::path(full_path_to_zip).stem().string();
    std::filesystem::create_directory(newDir);
    print_color_msg("    Top level directory generated", "yellow");
}

/**
 * @brief Fixes the META-INF folder.
 */
void EDINETTaxonomyPackage::fix_meta_inf_folder() {
    std::filesystem::create_directory(destination_folder + "/META-INF");
    print_color_msg("    META-INF directory generated", "yellow");
}

/**
 * @brief Restructures the folder.
 */
void EDINETTaxonomyPackage::restructure_folder() {
    for (const auto& entry : std::filesystem::directory_iterator(destination_folder)) {
        if (entry.path().extension() == ".zip") {
            std::filesystem::remove(entry.path());
            break;
        }
    }

    for (const auto& entry : std::filesystem::directory_iterator(destination_folder)) {
        if (entry.path().filename() != std::filesystem::path(full_path_to_zip).filename()) {
            std::filesystem::rename(entry.path(), destination_folder + "/" + std::filesystem::path(full_path_to_zip).stem().string() + "/" + entry.path().filename().string());
        }
    }
    print_color_msg("    Package content restructured", "yellow");
}

/**
 * @brief Fixes the taxonomy package XML file.
 *
 * @param source_folder The source folder for the XML file.
 */
void EDINETTaxonomyPackage::fix_taxonomy_package_xml(const std::string& source_folder) {
    xmlDocPtr doc = xmlNewDoc(BAD_CAST "1.0");
    xmlNodePtr root_node = xmlNewNode(NULL, BAD_CAST "taxonomyPackage");

    xmlNewProp(root_node, BAD_CAST "xml:lang", BAD_CAST "en");
    xmlNewProp(root_node, BAD_CAST "xmlns", BAD_CAST "http://xbrl.org/2016/taxonomy-package");
    xmlNewProp(root_node, BAD_CAST "xmlns:xsi", BAD_CAST "http://www.w3.org/2001/XMLSchema-instance");
    xmlNewProp(root_node, BAD_CAST "xsi:schemaLocation", BAD_CAST "http://xbrl.org/2016/taxonomy-package http://xbrl.org/2016/taxonomy-package.xsd");

    xmlNodePtr commentNode = xmlNewComment(BAD_CAST "This file and its content has been generated and is not part of the original ZIP.");
    xmlAddChild(root_node, commentNode);

    xmlAddChild(doc, root_node);

    // Add identifier
    xmlNodePtr identifierNode = xmlNewChild(root_node, NULL, BAD_CAST "identifier", BAD_CAST "full/official/path/to/the/package.zip");
    xmlNodePtr nameNode = xmlNewChild(root_node, NULL, BAD_CAST "name", BAD_CAST "ALL_2022-11-01.zip");
    xmlNodePtr descriptionNode = xmlNewChild(root_node, NULL, BAD_CAST "description", BAD_CAST "The ALL-2022-11-01 Taxonomy Package provided by the JFSA.");
    xmlNodePtr versionNode = xmlNewChild(root_node, NULL, BAD_CAST "version", BAD_CAST "2023");
    xmlNodePtr publisherNode = xmlNewChild(root_node, NULL, BAD_CAST "publisher", BAD_CAST "Japanese Financial Service Agency");
    xmlNodePtr publisherURLNode = xmlNewChild(root_node, NULL, BAD_CAST "publisherURL", BAD_CAST "https://www.fsa.go.jp/en/");
    xmlNodePtr publicationDateNode = xmlNewChild(root_node, NULL, BAD_CAST "publicationDate", BAD_CAST "2022-11-01");

    // Entry points
    xmlNodePtr entryPointsNode = xmlNewChild(root_node, NULL, BAD_CAST "entryPoints", NULL);
    for (const auto& file : std::filesystem::directory_iterator(source_folder + "/samples/2022-11-01")) {
        if (file.path().extension() == ".xsd") {
            xmlNodePtr entryPointNode = xmlNewChild(entryPointsNode, NULL, BAD_CAST "entryPoint", NULL);
            xmlNodePtr nameElem = xmlNewChild(entryPointNode, NULL, BAD_CAST "name", BAD_CAST file.path().filename().string().c_str());
            xmlNewChild(entryPointNode, NULL, BAD_CAST "version", BAD_CAST "2023");
            xmlNewChild(entryPointNode, NULL, BAD_CAST "entryPointDocument", BAD_CAST("http://disclosure.edinet-fsa.go.jp/samples/" + file.path().filename().string()).c_str());
        }
    }

    xmlSaveFormatFileEnc((source_folder + "/META-INF/taxonomyPackage.xml").c_str(), doc, "UTF-8", 1);
    xmlFreeDoc(doc);

    print_color_msg("    taxonomyPackage.xml file generated", "yellow");
}

/**
 * @brief Fixes the catalog XML file.
 *
 * @param source_folder The source folder for the XML file.
 */
void EDINETTaxonomyPackage::fix_catalog_xml(const std::string& source_folder) {
    xmlDocPtr doc = xmlNewDoc(BAD_CAST "1.0");
    xmlNodePtr root_node = xmlNewNode(NULL, BAD_CAST "catalog");

    xmlNewProp(root_node, BAD_CAST "xmlns", BAD_CAST "urn:oasis:names:tc:entity:xmlns:xml:catalog");
    xmlNewProp(root_node, BAD_CAST "xmlns:spy", BAD_CAST "http://www.altova.com/catalog_ext");
    xmlNewProp(root_node, BAD_CAST "xmlns:xsi", BAD_CAST "http://www.w3.org/2001/XMLSchema-instance");
    xmlNewProp(root_node, BAD_CAST "xsi:schemaLocation", BAD_CAST "urn:oasis:names:tc:entity:xmlns:xml:catalog Catalog.xsd");

    for (const auto& dir : std::filesystem::directory_iterator(source_folder + "/samples")) {
        if (dir.is_directory()) {
            xmlNewChild(root_node, NULL, BAD_CAST "rewriteURI", BAD_CAST("http://disclosure.edinet-fsa.go.jp/samples/" + dir.path().filename().string() + "/").c_str());
        }
    }

    for (const auto& taxonomyDir : std::filesystem::directory_iterator(source_folder + "/taxonomy")) {
        if (taxonomyDir.is_directory()) {
            for (const auto& epShortNameDir : std::filesystem::directory_iterator(taxonomyDir)) {
                if (epShortNameDir.is_directory()) {
                    std::string newPath = taxonomyDir.path().filename().string() + "/" + epShortNameDir.path().filename().string();
                    xmlNewChild(root_node, NULL, BAD_CAST "rewriteURI", BAD_CAST("http://disclosure.edinet-fsa.go.jp/taxonomy/" + newPath + "/").c_str());
                }
            }
        }
    }

    xmlSaveFormatFileEnc((source_folder + "/META-INF/catalog.xml").c_str(), doc, "UTF-8", 1);
    xmlFreeDoc(doc);

    print_color_msg("    catalog.xml file generated", "yellow");
}

/**
 * @brief Prints a colored message to the console.
 *
 * @param message The message to print.
 * @param color The color of the message.
 */
void EDINETTaxonomyPackage::print_color_msg(const std::string& message, const std::string& color) {
    // You can implement color output using ANSI escape codes or a library
    std::cout << message << std::endl;
}

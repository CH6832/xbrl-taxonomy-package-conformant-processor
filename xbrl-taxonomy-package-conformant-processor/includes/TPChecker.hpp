#pragma once

#ifndef TPCHECKER_H
#define TPCHECKER_H

#include <string>
#include <set>
#include <libxml/parser.h>
#include <libxml/tree.h>

/**
 * @class TPChecker
 * @brief This class provides methods to check an XBRL taxonomy package according to the XBRL specification.
 * 
 * The class includes methods for validating ZIP file formats, checking directory structures, 
 * validating XML schemas, and resolving XML base URIs as required by the XBRL Taxonomy Package Specification.
 */
class TPChecker {
public:
    /**
     * @brief Constructor for TPChecker.
     * 
     * Initializes the TPChecker class instance.
     */
    TPChecker();

    /**
     * @brief Check if the archive is in .zip format.
     * 
     * @param archive The path to the file to check.
     * @return True if the file has a .zip extension, otherwise False.
     */
    bool has_zip_format(const std::string &archive);

    /**
     * @brief Check if the archive contains a single top-level directory.
     * 
     * @param archive The path to the .zip archive.
     * @return True if there is only one top-level directory, otherwise False.
     */
    bool has_top_level_single_dir(const std::string &archive);

    /**
     * @brief Validate an XML file against an XML schema.
     * 
     * @param schemafile The path to the XML schema file (.xsd).
     * @param example The path to the XML document to validate.
     * @return True if the XML document is valid according to the schema, otherwise False.
     */
    bool validate_xml(const std::string &schemafile, const std::string &example);

    /**
     * @brief Check if the archive contains a folder named "META-INF".
     * 
     * @param archive The path to the .zip archive.
     * @param folder_name The name of the folder to check for (default: "META-INF").
     * @return True if the folder is present, otherwise False.
     */
    bool has_meta_inf_folder(const std::string &archive, const std::string &folder_name = "META-INF");

    /**
     * @brief Check if the archive contains a taxonomyPackage.xml file.
     * 
     * @param archive The path to the .zip archive.
     * @param tp_file The name of the file to check for (default: "taxonomyPackage.xml").
     * @return True if the file is present, otherwise False.
     */
    bool has_taxonomy_package_xml(const std::string &archive, const std::string &tp_file = "taxonomyPackage.xml");

    /**
     * @brief Resolve XML base URIs in an XML document according to a given base URL.
     * 
     * The method searches for `xlink:href` or `xml:base` attributes and resolves them 
     * relative to the provided base URL.
     * 
     * @param file The path to the XML document.
     * @param base_url The base URL to use for resolving relative URIs.
     * @return True if the resolution was successful, otherwise False.
     */
    bool check_rel_url_base_resolution(const std::string &file, const std::string &base_url);

private:
    /**
     * @brief Helper method to resolve XML base URIs in a given node recursively.
     * 
     * This method is called internally by `check_rel_url_base_resolution()` to update 
     * the `xlink:href` and `xml:base` attributes of each XML element.
     * 
     * @param node The XML node to resolve URIs for.
     * @param base_url The base URL to use for resolving URIs.
     */
    void resolve_xml_base(xmlNode *node, const std::string &base_url);
};

#endif // TPCHECKER_H

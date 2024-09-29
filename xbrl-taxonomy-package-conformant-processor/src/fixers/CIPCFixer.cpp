#include "../../includes/CIPCFixer.hpp"
#include <iostream>
#include <regex>
#include <fstream>
#include <filesystem>
#include <pugixml.hpp>
#include <set>
#include <map>
#include <string>
#include <algorithm>

namespace fs = std::filesystem;

/**
 * @brief Constructor for CIPCTaxonomyPackage
 *
 * Initializes with the destination folder.
 *
 * @param destination_folder Path to the folder where the taxonomy package is located.
 */
CIPCTaxonomyPackage::CIPCTaxonomyPackage(const std::string& destination_folder)
    : destination_folder(destination_folder) {}

/**
 * @brief Helper method to get full paths to all XSD files
 *
 * @return List of XSD file paths.
 */
std::vector<std::string> CIPCTaxonomyPackage::getFullPathOfAllXSDFiles() const {
    std::vector<std::string> full_paths;
    for (const auto& entry : fs::recursive_directory_iterator(destination_folder)) {
        if (entry.path().extension() == ".xsd" &&
            entry.path().filename().string().find("catalog") == std::string::npos &&
            entry.path().filename().string().find("taxonomyPackage") == std::string::npos) {
            full_paths.push_back(entry.path().string());
        }
    }
    return full_paths;
}

/**
 * @brief Helper method to get full paths to all XML files
 *
 * @return List of XML file paths.
 */
std::vector<std::string> CIPCTaxonomyPackage::getFullPathToAllXMLFiles() const {
    std::vector<std::string> full_paths;
    for (const auto& entry : fs::recursive_directory_iterator(destination_folder)) {
        if (entry.path().extension() == ".xml" &&
            entry.path().filename().string().find("catalog") == std::string::npos &&
            entry.path().filename().string().find("taxonomyPackage") == std::string::npos) {
            full_paths.push_back(entry.path().string());
        }
    }
    return full_paths;
}

/**
 * @brief Helper method to replace substrings in an XML node attribute.
 *
 * @param affected_xml_file The affected XML file name.
 * @param start_idx Starting index for the substring.
 * @param end_idx Ending index for the substring.
 * @param substring1 First substring to find.
 * @param substring2 Second substring to find.
 * @param node XML node to modify.
 * @param attribute Attribute to modify.
 * @param replace_with1 Replacement string 1.
 * @param replace_with2 Replacement string 2.
 * @param doc XML document to write back.
 */
void CIPCTaxonomyPackage::replaceSubstringInPropertyValue(
    const std::string& affected_xml_file,
    int start_idx,
    int end_idx,
    const std::string& substring1,
    const std::string& substring2,
    pugi::xml_node& node,
    const std::string& attribute,
    const std::string& replace_with1,
    const std::string& replace_with2,
    pugi::xml_document& doc
) const {
    std::string attr_value = node.attribute(attribute.c_str()).value();
    if (attr_value.substr(start_idx, end_idx) == substring1 &&
        attr_value.find(substring2) != std::string::npos) {
        std::string fixed_value = attr_value.replace(attr_value.find(replace_with1), replace_with1.length(), replace_with2);
        node.attribute(attribute.c_str()).set_value(fixed_value.c_str());
        doc.save_file(affected_xml_file.c_str());
    }
}

/**
 * @brief Helper method to replace substrings in schema files.
 *
 * @param condition Condition to check for in schema files.
 * @param node XML node to modify.
 * @param attribute Attribute to modify.
 * @param replace_substr1 Substring to replace.
 * @param replace_substr2 Replacement string for replace_substr1.
 * @param doc XML document to write back.
 */
void CIPCTaxonomyPackage::replaceSubstringInSchemaFile(
    const std::string& condition,
    pugi::xml_node& node,
    const std::string& attribute,
    const std::string& replace_substr1,
    const std::string& replace_substr2,
    pugi::xml_document& doc
) const {
    std::string attr_value = node.attribute(attribute.c_str()).value();
    if (attr_value.find(condition) != std::string::npos) {
        std::string fixed_value = attr_value.replace(attr_value.find(replace_substr1), replace_substr1.length(), replace_substr2);
        node.attribute(attribute.c_str()).set_value(fixed_value.c_str());
        doc.save_file(doc.c_str());
    }
}

/**
 * @brief Removes the integrated IFRS taxonomy folder.
 *
 * Deletes the folder containing 'def/ifrs' if found.
 */
void CIPCTaxonomyPackage::removeIFRSTaxonomy() {
    for (const auto& entry : fs::recursive_directory_iterator(destination_folder)) {
        if (entry.is_directory() && entry.path().string().find("def/ifrs") != std::string::npos) {
            fs::remove_all(entry.path());
            break;
        }
    }
}

/**
 * @brief Fixes the taxonomy package by updating URLs and removing redundant taxonomy files.
 */
void CIPCTaxonomyPackage::restructureFolder() {
    removeIFRSTaxonomy();

    // Example of fixing XML files
    for (const auto& xml_f : getFullPathToAllXMLFiles()) {
        pugi::xml_document doc;
        doc.load_file(xml_f.c_str());
        for (pugi::xml_node loc : doc.children("loc")) {
            std::string href = loc.attribute("xlink:href").value();
            // Example logic: Fix href if it matches certain patterns.
            if (href.find("/def/ifrs/full_ifrs") != std::string::npos) {
                replaceSubstringInPropertyValue(
                    xml_f, 0, 8, "../../..", "/def/ifrs/full_ifrs", loc, "xlink:href",
                    "../../../def/ifrs", "https://xbrl.ifrs.org/taxonomy/", doc);
            }
        }
    }

    // Example of fixing XSD files
    for (const auto& xsd_f : getFullPathOfAllXSDFiles()) {
        pugi::xml_document doc;
        doc.load_file(xsd_f.c_str());
        for (pugi::xml_node loc : doc.children("import")) {
            std::string schema_loc = loc.attribute("schemaLocation").value();
            if (schema_loc.find("../../def/ifrs/full_ifrs") != std::string::npos) {
                replaceSubstringInSchemaFile(
                    "../../def/ifrs/full_ifrs", loc, "schemaLocation",
                    "../../def/ifrs/full_ifrs", "https://xbrl.ifrs.org/taxonomy/", doc);
            }
        }
    }
}

#pragma once

#ifndef CIPCTAXONOMYPACKAGEFIXER_HPP
#define CIPCTAXONOMYPACKAGEFIXER_HPP

#include <iostream>
#include <string>
#include <vector>
#include <regex>
#include <filesystem>
#include <fstream>
#include <map>
#include <set>
#include <pugixml.hpp> // XML parsing library

/**
 * @brief Class CIPCTaxonomyPackage
 *
 * This class provides methods for fixing taxonomy package issues:
 *  - Fixes 'xlink:href' attributes in all linkbase files.
 *  - Removes the IFRS taxonomy package and incorporates it as a dependency.
 *
 * WARNING:
 * Ensure the source folder has no other files or folders.
 *
 */
class CIPCTaxonomyPackage {
public:
    CIPCTaxonomyPackage(const std::string& destination_folder);

    void convertToZipArchive();
    void fixTopLevelSingleDir();
    void fixMetaInfFolder();
    void fixTaxonomyPackageXML();
    void fixCatalogXML();
    void restructureFolder();

private:
    std::string destination_folder;
    std::string full_path_to_zip;

    // Helper methods
    std::string getPackageVersion() const;
    std::vector<std::string> getFullPathOfAllXSDFiles() const;
    std::vector<std::string> getFullPathToAllXMLFiles() const;

    void replaceSubstringInPropertyValue(
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
    ) const;

    void replaceSubstringInSchemaFile(
        const std::string& condition,
        pugi::xml_node& node,
        const std::string& attribute,
        const std::string& replace_substr1,
        const std::string& replace_substr2,
        pugi::xml_document& doc
    ) const;

    void removeIFRSTaxonomy();
};

#endif // CIPCTAXONOMYPACKAGEFIXER_HPP

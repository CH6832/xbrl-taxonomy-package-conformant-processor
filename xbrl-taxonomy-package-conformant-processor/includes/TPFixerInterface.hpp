#pragma once

#ifndef TPFIXERINTERFACE_HPP
#define TPFIXERINTERFACE_HPP

#include <string>
#include <filesystem>
#include <iostream>
#include <zip.h>

/**
 * @brief Interface for fixing XBRL Taxonomy Packages.
 *
 * This interface provides methods to fix an XBRL Taxonomy Package by a certain provider.
 */
class TPFixerInterface {
public:
    /**
     * @brief Constructor for TaxonomyPackageFixerInterface.
     *
     * Initializes the XBRL Taxonomy Package class. By initializing the class,
     * the input package is copied over to the output folder and extracted there
     * for comfortable data manipulation.
     *
     * @param full_path_to_zip The full path to the ZIP file of the taxonomy package.
     * @param destination_folder The folder where the taxonomy package will be extracted.
     */
    TPFixerInterface(const std::string& full_path_to_zip, const std::string& destination_folder);

    /**
     * @brief Converts the taxonomy package to a ZIP archive.
     *
     * @note This method must be implemented in derived classes.
     */
    virtual void convert_to_zip_archive() = 0;

    /**
     * @brief Fixes the top-level directory of the taxonomy package.
     *
     * Generates a single top-level directory for the provided XBRL taxonomy package.
     *
     * @note This method must be implemented in derived classes.
     */
    virtual void fix_top_level_single_dir() = 0;

    /**
     * @brief Fixes the META-INF folder of the taxonomy package.
     *
     * Generates a META-INF folder for the provided XBRL taxonomy package.
     *
     * @note This method must be implemented in derived classes.
     */
    virtual void fix_meta_inf_folder() = 0;

    /**
     * @brief Restructures the folders in the taxonomy package.
     *
     * Performs restructuring of folders in the XBRL Taxonomy Package.
     *
     * @note This method must be implemented in derived classes.
     */
    virtual void restructure_folder() = 0;

    /**
     * @brief Fixes the taxonomyPackage.xml file.
     *
     * The top-level directory MUST contain a taxonomyPackage.xml file.
     *
     * @note This method must be implemented in derived classes.
     */
    virtual void fix_taxonomy_package_xml() = 0;

    /**
     * @brief Fixes the catalog.xml file.
     *
     * A Taxonomy Package MUST NOT include a catalog file which includes more than
     * one rewriteURI element with the same value for the @uriStartString attribute.
     *
     * @note This method must be implemented in derived classes.
     */
    virtual void fix_catalog_xml() = 0;

protected:
    std::string full_path_to_zip;      /**< Full path to the ZIP file of the taxonomy package */
    std::string destination_folder;     /**< Destination folder for the taxonomy package */
};

#endif // TPFIXERINTERFACE_HPP

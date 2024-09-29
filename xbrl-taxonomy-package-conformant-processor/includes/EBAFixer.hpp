#pragma once

#ifndef EBATAXONOMYPACKAGEFIXER_HPP
#define EBATAXONOMYPACKAGEFIXER_HPP

#include <string>
#include <vector>

/**
 * @brief Interface for taxonomy package fixer classes.
 */
class TaxonomyPackageFixerInterface {
public:
    virtual void convert_to_zip_archive() = 0;
    virtual void fix_meta_inf_folder() = 0;
    virtual void fix_top_level_single_dir() = 0;
    virtual void restructure_folder() = 0;
    virtual void fix_taxonomy_package_xml() = 0;
    virtual void fix_catalog_xml() = 0;
};

/**
 * @brief Class to fix an EBA XBRL Taxonomy Package.
 *
 * The package can be found in the input/* folder as well as
 * newer and older versions at:
 * https://www.eba.europa.eu/risk-analysis-and-data/reporting-frameworks/reporting-framework-3.3
 */
class EBATaxonomyPackage : public TaxonomyPackageFixerInterface {
public:
    /**
     * @brief Constructor for EBATaxonomyPackage.
     */
    EBATaxonomyPackage();

    void convert_to_zip_archive() override;
    void fix_meta_inf_folder() override;
    void fix_top_level_single_dir() override;
    void restructure_folder() override;
    void fix_taxonomy_package_xml() override;
    void fix_catalog_xml() override;

private:
    // Add private member variables if needed
};

#endif // EBATAXONOMYPACKAGEFIXER_HPP

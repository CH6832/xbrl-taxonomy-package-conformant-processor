// xbrl-taxonomy-package-conformant-processor.h : Include file for standard system include files,
// or project specific include files.

#pragma once

#ifndef APP_HPP
#define APP_HPP

#include <string>
#include <iostream>
#include <filesystem>
#include <map>
#include <memory>
#include <stdexcept>
#include <cstdlib>
#include <argparse/argparse.hpp>
#include "../includes/logger.hpp" // Ensure you have your logger header
#include "../includes/TPChecker.hpp"
#include "../includes/EBAFixer.hpp"
#include "../includes/EDINETFixer.hpp"
#include "../includes/CMFCLCIFixer.hpp"
#include "../includes/CIPCFixer.hpp"
#include "../includes/utils.hpp"
#include "../includes/Providers.hpp"

/**
 * @brief The main application class for fixing XBRL Taxonomy Packages.
 */
class App {
public:
    /**
     * @brief Main entry point for the application.
     *
     * Initializes logging, parses arguments, and processes the XBRL package.
     */
    void run();

private:
    /**
     * @brief Parses command-line arguments.
     *
     * @return A tuple containing the provider and package path.
     * @throws std::invalid_argument if arguments are not valid.
     */
    std::pair<std::string, std::string> parse_arguments();

    /**
     * @brief Performs all package checks.
     *
     * @param tp_checker The TPChecker instance for checking the package.
     * @param package The path to the package.
     * @return A tuple of check results.
     */
    std::tuple<bool, bool, bool> check_package(TPChecker& tp_checker, const std::string& package);

    /**
     * @brief Fixes the package by applying necessary corrections based on the provider.
     *
     * @param provider_name The name of the provider.
     * @param package_class The class responsible for fixing the package.
     * @param source_zip_path The path to the source zip file.
     * @param destination_folder The folder where the package will be fixed.
     * @param checks The results of the package checks.
     */
    void fix_package(const std::string& provider_name,
        const std::unique_ptr<TaxonomyPackageFixerInterface>& package_class,
        const std::filesystem::path& source_zip_path,
        const std::filesystem::path& destination_folder,
        const std::tuple<bool, bool, bool>& checks);
};

#endif // APP_HPP

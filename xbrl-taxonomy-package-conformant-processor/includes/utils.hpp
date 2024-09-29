#pragma once

#ifndef UTILS_HPP
#define UTILS_HPP

#include <string>

/**
 * @brief Utility functions for the XBRL Taxonomy Package checking and fixing process.
 */
namespace utils {

	/**
	 * @brief Generates a zip archive out of a root input folder.
	 *
	 * @param folder_path The path to the folder to zip.
	 * @param zip_filename The name of the output zip file.
	 */
	void gen_zip_archive(const std::string& folder_path, const std::string& zip_filename);

	/**
	 * @brief Moves a folder recursively from one destination to another.
	 *
	 * @param source_folder The path of the source folder.
	 * @param destination_folder The path of the destination folder.
	 */
	void move_folder_recursively(const std::string& source_folder, const std::string& destination_folder);

	/**
	 * @brief Extracts a zip file to the folder it resides in.
	 *
	 * @param zip_path The path to the zip file.
	 */
	void extract_zip_in_same_folder(const std::string& zip_path);

	/**
	 * @brief Prints a colorized message to the console.
	 *
	 * @param msg The message to print.
	 * @param color The ANSI escape code for the color (default: white).
	 */
	void print_color_msg(const std::string& msg, const std::string& color = "\033[37m");  // Default to white

	/**
	 * @brief Deletes all non-ZIP files and folders in the specified folder and its subfolders.
	 *
	 * @param folder_path The path to the folder.
	 */
	void delete_non_zip_files_and_folders_recursive(const std::string& folder_path);

	/**
	 * @brief Extracts a zip file to a specified destination folder.
	 *
	 * @param zip_path Path to the zip file to be extracted.
	 * @param destination_folder Path to the folder where the contents will be extracted.
	 */
	void zip_dir_extractor(const std::string& zip_path, const std::string& destination_folder);

}  // namespace utils

#endif // UTILS_HPP

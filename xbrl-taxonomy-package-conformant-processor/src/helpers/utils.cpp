#include "../../includes/utils.hpp"
#include <iostream>
#include <filesystem>
#include <boost/filesystem.hpp>
#include <fstream>
#include <zip.h>
#include <string>
#include <vector>
#include <cstdio>

namespace fs = std::filesystem;

namespace utils {

    /**
     * @brief Generates a zip archive out of a root input folder.
     */
    void gen_zip_archive(const std::string& folder_path, const std::string& zip_filename) {
        // Open the zip file for writing
        int error = 0;
        zip_t* zip = zip_open(zip_filename.c_str(), ZIP_CREATE | ZIP_TRUNCATE, &error);
        if (!zip) {
            print_color_msg("    Failed to open zip file for writing", "\033[31m");  // Red for error
            return;
        }

        // Walk through the folder and add files to the zip
        for (const auto& entry : fs::recursive_directory_iterator(folder_path)) {
            if (entry.is_regular_file()) {
                std::string file_path = entry.path().string();
                std::string relative_path = fs::relative(file_path, folder_path).string();

                // Add file to the zip archive
                zip_source_t* source = zip_source_file(zip, file_path.c_str(), 0, 0);
                if (!source || zip_file_add(zip, relative_path.c_str(), source, ZIP_FL_OVERWRITE) < 0) {
                    print_color_msg("    Failed to add file to zip", "\033[31m");
                    zip_source_free(source);
                }
            }
        }

        zip_close(zip);
        print_color_msg("    Final zip generated", "\033[33m");  // Yellow
    }

    /**
     * @brief Moves a folder recursively from one destination to another.
     */
    void move_folder_recursively(const std::string& source_folder, const std::string& destination_folder) {
        fs::create_directories(destination_folder);  // Create destination folder if it doesn't exist

        for (const auto& entry : fs::directory_iterator(source_folder)) {
            fs::path source_item_path = entry.path();
            fs::path destination_item_path = destination_folder / source_item_path.filename();

            if (fs::is_directory(source_item_path)) {
                move_folder_recursively(source_item_path.string(), destination_item_path.string());
            }
            else {
                fs::rename(source_item_path, destination_item_path);  // Move file
            }
        }
        fs::remove(source_folder);  // Remove the source folder after moving
    }

    /**
     * @brief Extracts a zip file to the folder it resides in.
     */
    void extract_zip_in_same_folder(const std::string& zip_path) {
        std::string zip_dir = fs::path(zip_path).parent_path().string();

        // Open the zip file
        int error = 0;
        zip_t* zip = zip_open(zip_path.c_str(), ZIP_RDONLY, &error);
        if (!zip) {
            print_color_msg("    Failed to open zip file for extraction", "\033[31m");  // Red for error
            return;
        }

        // Extract files
        zip_int64_t num_entries = zip_get_num_entries(zip, 0);
        for (zip_uint64_t i = 0; i < num_entries; ++i) {
            const char* name = zip_get_name(zip, i, 0);
            fs::path output_path = zip_dir + name;

            zip_file_t* zf = zip_fopen_index(zip, i, 0);
            if (!zf) {
                print_color_msg("    Failed to open file in zip for extraction", "\033[31m");
                continue;
            }

            // Create directories if necessary
            if (name[std::strlen(name) - 1] == '/') {
                fs::create_directories(output_path);
            }
            else {
                std::ofstream out(output_path, std::ios::binary);
                char buffer[4096];
                zip_int64_t bytes_read;
                while ((bytes_read = zip_fread(zf, buffer, sizeof(buffer))) > 0) {
                    out.write(buffer, bytes_read);
                }
            }
            zip_fclose(zf);
        }

        zip_close(zip);
        print_color_msg("    Zip extracted successfully", "\033[33m");  // Yellow
    }

    /**
     * @brief Prints a colorized message to the console.
     */
    void print_color_msg(const std::string& msg, const std::string& color) {
        std::cout << color << msg << "\033[0m" << std::endl;  // Reset color after printing
    }

    /**
     * @brief Deletes all non-ZIP files and folders in the specified folder and its subfolders.
     */
    void delete_non_zip_files_and_folders_recursive(const std::string& folder_path) {
        for (auto it = fs::recursive_directory_iterator(folder_path, fs::directory_options::skip_permission_denied); it != fs::end(it); ++it) {
            if (it->is_regular_file() && it->path().extension() != ".zip") {
                fs::remove(it->path());
            }
            else if (it->is_directory() && fs::is_empty(it->path())) {
                fs::remove(it->path());
            }
        }
    }

    void zip_dir_extractor(const std::string& zip_path, const std::string& destination_folder) {
        // Create the destination folder if it doesn't exist
        fs::create_directories(destination_folder);

        // Open the zip file
        int error = 0;
        zip_t* zip = zip_open(zip_path.c_str(), ZIP_RDONLY, &error);
        if (!zip) {
            print_color_msg("    Failed to open zip file for extraction", "\033[31m");  // Red for error
            return;
        }

        // Extract files
        zip_int64_t num_entries = zip_get_num_entries(zip, 0);
        for (zip_uint64_t i = 0; i < num_entries; ++i) {
            const char* name = zip_get_name(zip, i, 0);
            if (!name) {
                print_color_msg("    Failed to get name of the file in zip", "\033[31m");
                continue;
            }

            // Construct the output path by appending the name to the destination folder
            fs::path output_path = fs::path(destination_folder) / name;

            zip_file_t* zf = zip_fopen_index(zip, i, 0);
            if (!zf) {
                print_color_msg("    Failed to open file in zip for extraction", "\033[31m");
                continue;
            }

            // Create directories if necessary
            if (name[std::strlen(name) - 1] == '/') {
                fs::create_directories(output_path);
            }
            else {
                // Create parent directories if they do not exist
                fs::create_directories(output_path.parent_path());

                std::ofstream out(output_path, std::ios::binary);
                char buffer[4096];
                zip_int64_t bytes_read;
                while ((bytes_read = zip_fread(zf, buffer, sizeof(buffer))) > 0) {
                    out.write(buffer, bytes_read);
                }

                if (out.fail()) {
                    print_color_msg("    Failed to write file to output path", "\033[31m");
                }
            }
            zip_fclose(zf);
        }

        zip_close(zip);
        print_color_msg("    Zip extracted successfully", "\033[33m");  // Yellow
    }

}  // namespace utils

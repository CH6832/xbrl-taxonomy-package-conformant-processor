#include "../../includes/TPFixerInterface.hpp"
#include "../../includes/utils.hpp"

/**
 * @brief Constructor for TaxonomyPackageFixerInterface.
 *
 * @param full_path_to_zip The full path to the ZIP file of the taxonomy package.
 * @param destination_folder The folder where the taxonomy package will be extracted.
 */
TPFixerInterface::TPFixerInterface(const std::string& full_path_to_zip, const std::string& destination_folder)
    : full_path_to_zip(full_path_to_zip), destination_folder(destination_folder) {

    // Create the destination folder if it does not exist
    std::filesystem::create_directories(destination_folder);

    // Move the taxonomy package to the destination folder
    std::filesystem::copy(full_path_to_zip, destination_folder, std::filesystem::copy_options::overwrite_existing);

    // Extract the ZIP file at the destination
    try {
        int err = 0;
        zip_t* zip = zip_open(full_path_to_zip.c_str(), 0, &err);

        if (zip) {
            utils::zip_dir_extractor(zip, destination_folder);
            zip_close(zip);
            std::cout << "Extracted " << full_path_to_zip << " to " << destination_folder << std::endl;
        }
        else {
            std::cerr << "Error: The file " << full_path_to_zip << " is not a valid ZIP archive." << std::endl;
        }
    }
    catch (const std::filesystem::filesystem_error& e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }
    catch (const std::exception& e) {
        std::cerr << "An error occurred: " << e.what() << std::endl;
    }
}

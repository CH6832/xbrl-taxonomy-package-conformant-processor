#include "../../includes/error_handler.hpp"
#include <iostream>

/**
 * @brief Constructor for BaseCustomException.
 */
BaseCustomException::BaseCustomException(const std::string& message) : std::runtime_error(message) {
    log_error();  // Automatically log the error when it occurs
}

/**
 * @brief Logs the error using std::cerr or any other logging mechanism.
 */
void BaseCustomException::log_error() const {
    std::cerr << "Error: " << what() << std::endl;
}

/**
 * @brief Constructor for FileNotFoundError.
 */
FileNotFoundError::FileNotFoundError(const std::string& filepath, const std::string& message)
    : BaseCustomException(message + ": " + filepath) {
    log_error();
}

/**
 * @brief Constructor for ValidationError.
 */
ValidationError::ValidationError(const std::string& field, const std::string& message)
    : BaseCustomException(message + ": " + field) {
    log_error();
}

/**
 * @brief Constructor for InvalidFileFormatError.
 */
InvalidFileFormatError::InvalidFileFormatError(const std::string& file_format, const std::string& message)
    : BaseCustomException(message + ": " + file_format) {
    log_error();
}

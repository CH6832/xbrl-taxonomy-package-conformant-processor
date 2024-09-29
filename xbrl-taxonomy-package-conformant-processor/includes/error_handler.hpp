#pragma once

#ifndef ERROR_HANDLER_HPP
#define ERROR_HANDLER_HPP

#include <stdexcept>
#include <string>
#include <functional>
#include <iostream>

/**
 * @brief Base class for custom exceptions.
 * All custom exceptions should derive from this class.
 */
class BaseCustomException : public std::runtime_error {
public:
    /**
     * @brief Constructor for the BaseCustomException class.
     * @param message The error message to display.
     */
    explicit BaseCustomException(const std::string& message = "An error occurred");

    /**
     * @brief Logs the error message using the logger.
     */
    void log_error() const;
};

/**
 * @brief Exception raised when a required file is not found.
 */
class FileNotFoundError : public BaseCustomException {
public:
    /**
     * @brief Constructor for the FileNotFoundError class.
     * @param filepath The path to the file that was not found.
     * @param message The error message.
     */
    FileNotFoundError(const std::string& filepath, const std::string& message = "File not found");
};

/**
 * @brief Exception raised for validation errors.
 */
class ValidationError : public BaseCustomException {
public:
    /**
     * @brief Constructor for the ValidationError class.
     * @param field The field that contains the validation error.
     * @param message The error message.
     */
    ValidationError(const std::string& field, const std::string& message = "Invalid input");
};

/**
 * @brief Exception raised when a file has an invalid format.
 */
class InvalidFileFormatError : public BaseCustomException {
public:
    /**
     * @brief Constructor for the InvalidFileFormatError class.
     * @param file_format The file format that is invalid.
     * @param message The error message.
     */
    InvalidFileFormatError(const std::string& file_format, const std::string& message = "Invalid file format");
};

/**
 * @brief Function wrapper to handle errors in function calls.
 * @param func The function to be wrapped for error handling.
 * @return The function result if no exceptions are thrown.
 */
template <typename Func, typename... Args>
auto handle_error(Func func, Args... args) -> decltype(func(args...)) {
    try {
        return func(args...);
    }
    catch (const BaseCustomException& e) {
        e.log_error();
        throw;
    }
    catch (const std::exception& e) {
        std::cerr << "Unhandled exception: " << e.what() << std::endl;
        throw;
    }
}

#endif // ERROR_HANDLER_HPP

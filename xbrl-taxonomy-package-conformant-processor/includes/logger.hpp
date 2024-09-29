#pragma once

#ifndef LOGGER_HPP
#define LOGGER_HPP

#include <string>
#include <memory>
#include <fstream>
#include <iostream>

/**
 * @brief A simple logger class that provides logging functionality with rotating file handling and console output.
 *
 * Example usage:
 * @code
 * Logger logger = Logger::get_instance("logs/app.log", Logger::LogLevel::INFO);
 * logger.info("This is an info message.");
 * logger.error("This is an error message.");
 * @endcode
 */
class Logger {
public:
    /// Log level enumeration.
    enum class LogLevel {
        INFO,
        ERROR,
        DEBUG
    };

    /**
     * @brief Get the singleton instance of the Logger.
     *
     * @param log_file The path to the log file.
     * @param level The logging level (default is INFO).
     * @param max_bytes The maximum file size before rotating (default 1 MB).
     * @param backup_count The number of backup files to keep (default 5).
     * @return The instance of the Logger.
     */
    static Logger& get_instance(const std::string& log_file, LogLevel level = LogLevel::INFO, size_t max_bytes = 1'000'000, int backup_count = 5);

    /**
     * @brief Log an info-level message.
     *
     * @param message The message to log.
     */
    void info(const std::string& message);

    /**
     * @brief Log an error-level message.
     *
     * @param message The message to log.
     */
    void error(const std::string& message);

    /**
     * @brief Log a debug-level message.
     *
     * @param message The message to log.
     */
    void debug(const std::string& message);

private:
    /// Private constructor (singleton pattern).
    Logger(const std::string& log_file, LogLevel level, size_t max_bytes, int backup_count);

    /**
     * @brief Rotates the log file when it reaches the specified size limit.
     */
    void rotate_log();

    /**
     * @brief Write a message to the log file.
     *
     * @param level The log level of the message.
     * @param message The message to log.
     */
    void log(LogLevel level, const std::string& message);

    /**
     * @brief Get the log level as a string.
     *
     * @param level The log level.
     * @return The log level as a string.
     */
    std::string level_to_string(LogLevel level);

    std::ofstream log_stream_;  ///< Stream to the log file.
    LogLevel log_level_;        ///< Current logging level.
    size_t max_bytes_;          ///< Maximum log file size before rotating.
    int backup_count_;          ///< Number of backup log files to keep.
    std::string log_file_;      ///< Log file path.

    static std::unique_ptr<Logger> instance_;  ///< Singleton instance.
};

#endif // LOGGER_HPP

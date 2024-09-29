#include "../../includes/logger.hpp"
#include <filesystem>
#include <ctime>

std::unique_ptr<Logger> Logger::instance_ = nullptr;

/**
 * @brief Get the singleton instance of the Logger.
 */
Logger& Logger::get_instance(const std::string& log_file, LogLevel level, size_t max_bytes, int backup_count) {
    if (instance_ == nullptr) {
        instance_ = std::unique_ptr<Logger>(new Logger(log_file, level, max_bytes, backup_count));
    }
    return *instance_;
}

/**
 * @brief Logger constructor.
 */
Logger::Logger(const std::string& log_file, LogLevel level, size_t max_bytes, int backup_count)
    : log_file_(log_file), log_level_(level), max_bytes_(max_bytes), backup_count_(backup_count) {

    // Open the log file in append mode.
    log_stream_.open(log_file_, std::ios::app | std::ios::out);
    if (!log_stream_.is_open()) {
        std::cerr << "Failed to open log file: " << log_file_ << std::endl;
        throw std::runtime_error("Failed to open log file");
    }
}

/**
 * @brief Log an info-level message.
 */
void Logger::info(const std::string& message) {
    log(LogLevel::INFO, message);
}

/**
 * @brief Log an error-level message.
 */
void Logger::error(const std::string& message) {
    log(LogLevel::ERROR, message);
    std::cerr << level_to_string(LogLevel::ERROR) << ": " << message << std::endl;  // Console output
}

/**
 * @brief Log a debug-level message.
 */
void Logger::debug(const std::string& message) {
    log(LogLevel::DEBUG, message);
}

/**
 * @brief Log a message with the given log level.
 */
void Logger::log(LogLevel level, const std::string& message) {
    if (level >= log_level_) {
        // Rotate the log if necessary.
        if (log_stream_.tellp() >= static_cast<std::streampos>(max_bytes_)) {
            rotate_log();
        }

        // Get current time.
        std::time_t now = std::time(nullptr);
        char time_str[20];
        std::strftime(time_str, sizeof(time_str), "%Y-%m-%d %H:%M:%S", std::localtime(&now));

        // Write log entry.
        log_stream_ << time_str << " - " << level_to_string(level) << " - " << message << std::endl;
    }
}

/**
 * @brief Rotates the log file when it reaches the specified size limit.
 */
void Logger::rotate_log() {
    log_stream_.close();

    // Rename old log files.
    for (int i = backup_count_ - 1; i > 0; --i) {
        std::string old_log = log_file_ + "." + std::to_string(i);
        std::string new_log = log_file_ + "." + std::to_string(i + 1);
        if (std::filesystem::exists(old_log)) {
            std::filesystem::rename(old_log, new_log);
        }
    }

    // Rename the current log file to log_file.1
    std::string first_backup = log_file_ + ".1";
    std::filesystem::rename(log_file_, first_backup);

    // Reopen the log file for new entries.
    log_stream_.open(log_file_, std::ios::app | std::ios::out);
}

/**
 * @brief Converts a log level to a string representation.
 */
std::string Logger::level_to_string(LogLevel level) {
    switch (level) {
    case LogLevel::INFO:
        return "INFO";
    case LogLevel::ERROR:
        return "ERROR";
    case LogLevel::DEBUG:
        return "DEBUG";
    default:
        return "UNKNOWN";
    }
}

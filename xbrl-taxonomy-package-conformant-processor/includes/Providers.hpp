#pragma once

#ifndef PROVIDER_HPP
#define PROVIDER_HPP

#include <string>
#include <stdexcept>

// Define the Provider enum class
enum class Provider {
    EBA,
    EDINET,
    CMFCLCI,
    CIPC
};

// Function to convert enum to string
inline std::string providerToString(Provider provider) {
    switch (provider) {
    case Provider::EBA:
        return "EBA";
    case Provider::EDINET:
        return "EDINET";
    case Provider::CMFCLCI:
        return "CMFCLCI";
    case Provider::CIPC:
        return "CIPC";
    default:
        throw std::invalid_argument("Unknown provider");
    }
}

// Optional: Function to convert string to enum (if needed)
inline Provider stringToProvider(const std::string& str) {
    if (str == "EBA") return Provider::EBA;
    if (str == "EDINET") return Provider::EDINET;
    if (str == "CMFCLCI") return Provider::CMFCLCI;
    if (str == "CIPC") return Provider::CIPC;
    throw std::invalid_argument("Unknown provider string");
}

#endif // PROVIDER_HPP

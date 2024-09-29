#include <iostream>
#include <fstream>
#include <string>
#include <set>
#include <zip.h>
#include <libxml/parser.h>
#include <libxml/tree.h>
#include <libxml/xmlschemas.h>
#include <libxml/xpath.h>
#include <boost/filesystem.hpp>
#include <boost/algorithm/string.hpp>
#include "../../includes/TPChecker.hpp"

class TPChecker {
public:
    TPChecker() {}

    bool has_zip_format(const std::string& archive) {
        return boost::algorithm::iends_with(archive, ".zip");
    }

    bool has_top_level_single_dir(const std::string& archive) {
        int err = 0;
        zip* zip_file = zip_open(archive.c_str(), 0, &err);
        if (zip_file == nullptr) {
            std::cerr << "Error opening zip file: " << err << std::endl;
            return false;
        }

        std::set<std::string> top_dirs;
        zip_int64_t num_files = zip_get_num_entries(zip_file, 0);

        for (zip_int64_t i = 0; i < num_files; i++) {
            const char* file_name = zip_get_name(zip_file, i, 0);
            if (file_name) {
                std::string top_dir = std::string(file_name).substr(0, std::string(file_name).find('/'));
                top_dirs.insert(top_dir);
            }
        }

        zip_close(zip_file);
        return top_dirs.size() == 1;
    }

    bool validate_xml(const std::string& schemafile, const std::string& example) {
        xmlDocPtr doc = xmlReadFile(example.c_str(), nullptr, 0);
        if (doc == nullptr) {
            std::cerr << "Error parsing XML document." << std::endl;
            return false;
        }

        xmlSchemaParserCtxtPtr schema_ctxt = xmlSchemaNewParserCtxt(schemafile.c_str());
        xmlSchemaPtr schema = xmlSchemaParse(schema_ctxt);
        xmlSchemaValidCtxtPtr valid_ctxt = xmlSchemaNewValidCtxt(schema);

        int ret = xmlSchemaValidateDoc(valid_ctxt, doc);
        if (ret == 0) {
            xmlSchemaFree(schema);
            xmlSchemaFreeValidCtxt(valid_ctxt);
            xmlFreeDoc(doc);
            return true;
        }
        else {
            std::cerr << "XML document is invalid." << std::endl;
            xmlSchemaFree(schema);
            xmlSchemaFreeValidCtxt(valid_ctxt);
            xmlFreeDoc(doc);
            return false;
        }
    }

    bool has_meta_inf_folder(const std::string& archive, const std::string& folder_name = "META-INF") {
        int err = 0;
        zip* zip_file = zip_open(archive.c_str(), 0, &err);
        if (zip_file == nullptr) {
            std::cerr << "Error opening zip file: " << err << std::endl;
            return false;
        }

        zip_int64_t num_files = zip_get_num_entries(zip_file, 0);

        for (zip_int64_t i = 0; i < num_files; i++) {
            const char* file_name = zip_get_name(zip_file, i, 0);
            if (file_name && std::string(file_name).find(folder_name) != std::string::npos) {
                zip_close(zip_file);
                return true;
            }
        }

        zip_close(zip_file);
        return false;
    }

    bool has_taxonomy_package_xml(const std::string& archive, const std::string& tp_file = "taxonomyPackage.xml") {
        int err = 0;
        zip* zip_file = zip_open(archive.c_str(), 0, &err);
        if (zip_file == nullptr) {
            std::cerr << "Error opening zip file: " << err << std::endl;
            return false;
        }

        zip_int64_t num_files = zip_get_num_entries(zip_file, 0);

        for (zip_int64_t i = 0; i < num_files; i++) {
            const char* file_name = zip_get_name(zip_file, i, 0);
            if (file_name && std::string(file_name).find(tp_file) != std::string::npos) {
                zip_close(zip_file);
                return true;
            }
        }

        zip_close(zip_file);
        return false;
    }

    bool check_rel_url_base_resolution(const std::string& file, const std::string& base_url) {
        xmlDocPtr doc = xmlReadFile(file.c_str(), nullptr, 0);
        if (doc == nullptr) {
            std::cerr << "Error parsing XML document." << std::endl;
            return false;
        }

        xmlNode* root_element = xmlDocGetRootElement(doc);
        resolve_xml_base(root_element, base_url);
        xmlSaveFormatFileEnc("-", doc, "UTF-8", 1);
        xmlFreeDoc(doc);
        return true;
    }

    void resolve_xml_base(xmlNode* node, const std::string& base_url) {
        xmlAttr* attr = node->properties;
        while (attr) {
            if (xmlStrcmp(attr->name, BAD_CAST "xlink:href") == 0 || xmlStrcmp(attr->name, BAD_CAST "xml:base") == 0) {
                // Manual URI resolution
                std::string resolved = base_url + "/" + reinterpret_cast<const char*>(attr->children->content);
                xmlSetProp(node, attr->name, BAD_CAST resolved.c_str());
            }
            attr = attr->next;
        }

        xmlNode* child = node->children;
        while (child) {
            resolve_xml_base(child, base_url);
            child = child->next;
        }
    }
};

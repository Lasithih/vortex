//
// Created by lasith on 5/4/19.
//

#include "config.h"

#include <libconfig.h>
#include <string.h>
#include <stdlib.h>
#include "../consts.h"
#include "../helpers/string_utils.h"
#include "../log/logger.h"
#include "../helpers/conversions.h"

const char* get_value_for_key(char* key);

config_t cfg;

//database
char *server;
char *username;
char *password;
char *db_name;

char *download_dir;

void init_config()
{
    char *cserver = (char *) get_value_for_key("database.server");
    server = malloc(strlen(cserver)+1);
    if (server == NULL) {
        print_console("Config - Out of memory");
    } else {
        string_copy(cserver, server);
    }
    config_destroy(&cfg);


    char *cusername = (char *)get_value_for_key("database.user");
    username = malloc(strlen(cusername)+1);
    if (username == NULL) {
        print_console("Config - Out of memory");
    } else {
        string_copy(cusername, username);
    }
    config_destroy(&cfg);

    char *cpassword = (char *)get_value_for_key("database.password");
    password = malloc(strlen(cpassword)+1);
    if (password == NULL) {
        print_console("Config - Out of memory");
    } else {
        string_copy(cpassword, password);
    }
    config_destroy(&cfg);

    char *cdb_name = (char *)get_value_for_key("database.database_name");
    db_name = malloc(strlen(cdb_name)+1);
    if (db_name == NULL) {
        print_console("Config - Out of memory");
    } else {
        string_copy(cdb_name, db_name);
    }
    config_destroy(&cfg);

    char *homedir = getenv("HOME");
    download_dir = init_new_string();
    download_dir = concatenate_string(download_dir, homedir);
    download_dir = concatenate_string(download_dir, "/Downloads/");
}

char *get_env()
{
    return ENVIRONMENT_DEV;
}

char *get_log_dir_job()
{
    return LOG_DIR_JOB;
}

char *get_log_dir_job_success()
{
    return LOG_DIR_JOB_SUCCESS;
}

char *get_log_dir_debug()
{
    return LOG_DIR_DEBUG;
}

char *get_log_dir()
{
    return LOG_DIR;
}

char *get_download_dir()
{
    return download_dir;
}

char *get_database_server()
{
    return server;
}

char *get_database_username()
{
    return username;
}

char *get_database_password()
{
    return password;
}

char *get_database_dbname()
{
    return db_name;
}


const char* get_value_for_key(char* key)
{
    config_setting_t *setting;

    const char *str;

    config_init(&cfg);



    if(!config_read_file(&cfg, "config.cfg"))
    {
        print_console("%s:%d - %s\n", config_error_file(&cfg),
                      config_error_line(&cfg), config_error_text(&cfg));
        config_destroy(&cfg);
        print_console("Failed to open config file\n");
        return NULL;
    }

    if(config_lookup_string(&cfg, key, &str)) {
        return str;
    } else {
        print_console("No '%s' setting in configuration file.\n", key);
        return NULL;
    }
}


void deinit_config()
{
    free(download_dir);
}
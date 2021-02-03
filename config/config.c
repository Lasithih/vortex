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
char *s_server;
char *username;
char *s_password;
char *db_name;

char *download_dir;

bool log_enabled = true;

void init_config()
{
    char *log = (char *) get_value_for_key("log.enabled");
    if (strcmp(log,"1")==0) {
        log_enabled = true;
    } else {
        log_enabled = false;
    }
    config_destroy(&cfg);


    char *cs_server = (char *) get_value_for_key("database.server");
    s_server = malloc(strlen(cs_server)+1);
    if (s_server == NULL) {
        print_console("Config - Out of memory");
    } else {
        string_copy(cs_server, s_server);
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

    char *cs_password = (char *)get_value_for_key("database.password");
    s_password = malloc(strlen(cs_password)+1);
    if (s_password == NULL) {
        print_console("Config - Out of memory");
    } else {
        string_copy(cs_password, s_password);
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

//    char *homedir = getenv("HOME");
//    download_dir = init_new_string();
//    download_dir = concatenate_string(download_dir, homedir);
//    download_dir = concatenate_string(download_dir, "/Downloads/");

    char *cdownload_dir = (char *)get_value_for_key("path.download_path");
    download_dir = malloc(strlen(cdownload_dir)+1);
    if (db_name == NULL) {
        print_console("Config - Out of memory");
    } else {
        string_copy(cdownload_dir, download_dir);
    }
    config_destroy(&cfg);
}

char *get_env()
{
    return ENVIRONMENT_CONTAINER;
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
    return s_server;
}

char *get_database_username()
{
    return username;
}

char *get_database_password()
{
    return s_password;
}

char *get_database_dbname()
{
    return db_name;
}

bool is_log_enabled()
{
    return log_enabled;
}


const char* get_value_for_key(char* key)
{
    char *env = get_env();
    if (strcmp(env,ENVIRONMENT_CONTAINER) == 0)
    {
        char newkey[128];
        strcpy(newkey , key);
        for(int i = 0; i <= strlen(newkey); i++)
        {
            if(newkey[i] == '.')  
            {
                newkey[i] = '_';
            } 
        }
        if(strcmp(newkey,"path_download_path")==0)
        {
            return "/Downloads";
        }
        char *val = getenv(newkey);
        if(val == NULL)
        {
            print_console("Error: no values found for environment key %s\n", newkey);
        }
        return val;
    }
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

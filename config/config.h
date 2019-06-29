//
// Created by lasith on 5/4/19.
//

#ifndef DOWNLOADER_CONFIG_H
#define DOWNLOADER_CONFIG_H

#include <stdbool.h>

void init_config();
void deinit_config();

char *get_env();
char *get_log_dir_job();
char *get_log_dir_job_success();
char *get_log_dir_debug();
char *get_log_dir();
char *get_download_dir();
bool is_log_enabled();

char *get_database_server();
char *get_database_username();
char *get_database_password();
char *get_database_dbname();

#endif //DOWNLOADER_CONFIG_H

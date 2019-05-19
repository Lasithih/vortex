//
// Created by lasith on 5/5/19.
//

#ifndef DOWNLOADER_WGET_H
#define DOWNLOADER_WGET_H

char *wget_start_command(char *command);
char *wget_add_url(char *command, char *url);
char *wget_add_output_path(char *command, char *path);

#endif //DOWNLOADER_WGET_H

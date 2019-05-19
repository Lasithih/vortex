//
// Created by lasith on 5/5/19.
//

#ifndef DOWNLOADER_COMMAND_BUILDER_H
#define DOWNLOADER_COMMAND_BUILDER_H

#include "../structs/job_t.h"

char *build_command(struct job_t job);
void destroy_command(char *command);

#endif //DOWNLOADER_COMMAND_BUILDER_H

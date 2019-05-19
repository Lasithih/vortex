//
// Created by lasith on 5/4/19.
//

#ifndef DOWNLOADER_JOB_T_H
#define DOWNLOADER_JOB_T_H

#include "../consts.h"

struct job_t {

    int id;
    char *url;
    int start_at_midnight;
    char *path;
    int job_type;
    char *format;
    int status;
    char *comment;
    char *start_time;
    char *end_time;
};

#define DEFAULT_JOB_INITIALIZER {-1,NULL,1,NULL,JOB_TYPE_YOUTUBE,NULL,0,NULL,NULL,NULL};

#endif //DOWNLOADER_JOB_T_H

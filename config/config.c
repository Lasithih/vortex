//
// Created by lasith on 5/4/19.
//

#include "config.h"

#include <string.h>
#include "../consts.h"


char *get_env()
{
    return ENVIRONMENT_DEV;
}

char *get_command_output_path()
{
    if(strcmp(get_env(),ENVIRONMENT_DEV)==0)
        return COMMAND_OUT_PATH_DEV;
    else
        return COMMAND_OUT_PATH_QNAP;
}

char *get_job_success_path()
{
    if(strcmp(get_env(),ENVIRONMENT_DEV)==0)
        return JOB_SUCCESS_PATH_DEV;
    else
        return JOB_SUCCESS_PATH_QNAP;
}
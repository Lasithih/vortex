//
// Created by lasith on 5/19/19.
//

#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include "ffmpeg.h"
#include "../helpers/string_utils.h"
#include "../helpers/conversions.h"
#include "../config/config.h"
#include "../consts.h"


char *ffmpeg_start_command(char *command)
{
    char *env = get_env();
    if(strcmp(env,ENVIRONMENT_CONTAINER)==0) 
    {
        char *start = " build/ffmpeg_sup.sh";
        command = concatenate_string(command,start);
    }
    else 
    {
        char *start = " ./ffmpeg_sup.sh";
        command = concatenate_string(command,start);
    }
    

    return command;
}


char *ffmpeg_add_start_time(char *command, char *start_time)
{
    char *space = " ";

    command = concatenate_string(command,space);
    if(start_time == NULL)
        command = concatenate_string(command,"00:00:00");
    else
        command = concatenate_string(command,start_time);

    return command;
}


char *ffmpeg_add_end_time(char *command, char *start_time, char *end_time)
{
    char *space = " ";

    command = concatenate_string(command,space);

    if(start_time == NULL)
    {
        start_time = init_new_string();
        start_time = concatenate_string(start_time, "00:00:00");
    }

    int interval = endtime_to_interval(start_time, end_time);
    command = concatenate_string(command,int_to_string(interval));
    free(start_time);
    return command;
}


char *ffmpeg_add_dummy_end_time(char *command)
{
    char *space = " ";

    command = concatenate_string(command,space);
    command = concatenate_string(command,"-1");

    return command;
}


char *ffmpeg_add_format(char *command, char *format)
{
    char *space = " ";

    command = concatenate_string(command,space);
    command = concatenate_string(command,format);

    return command;
}


char *ffmpeg_add_path(char *command, char *path)
{
    char *space = " ";
    char *slash = "/";

    command = concatenate_string(command,space);
    command = concatenate_string(command,path);
    command = concatenate_string(command,slash);

    return command;
}
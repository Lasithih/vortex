//
// Created by lasith on 5/5/19.
//

#include "youtube_dl.h"
#include "../helpers/conversions.h"
#include "../log/logger.h"
#include "../helpers/string_utils.h"
#include <stdlib.h>
#include <string.h>

char *ytdl_start_command(char *command)
{
    char *start = " youtube-dl";

    command = concatenate_string(command,start);

    return command;
}

char *ytdl_add_output_path(char *command, char *path)
{
    char *option = " -o '";

    command = concatenate_string(command, option);
    command = concatenate_string(command, path);
    command = concatenate_string(command, "/%(title)s.%(ext)s'");
    return command;
}

char *ytdl_add_url(char *command, char *url)
{
    char *option = " ";
    command = concatenate_string(command, option);
    command = concatenate_string(command, url);
    return command;
}

char *ytdl_add_format(char *command, char *format)
{
    if (strcmp(format,"mp3") == 0)
    {
        command = concatenate_string(command, " -x");
        command = concatenate_string(command, " --audio-format ");
        command = concatenate_string(command, format);
    }
    else
    {
        char *option = " --format ";

        command = concatenate_string(command, option);
        command = concatenate_string(command, format);
    }


    return command;
}
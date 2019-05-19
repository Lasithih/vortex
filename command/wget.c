//
// Created by lasith on 5/5/19.
//

#include "wget.h"
#include "../helpers/conversions.h"
#include "../log/logger.h"
#include "../helpers/string_utils.h"
#include <stdlib.h>
#include <string.h>


char *wget_start_command(char *command)
{
    char *start = " wget";

    command = concatenate_string(command,start);

    return command;
}

char *wget_add_url(char *command, char *url)
{
    char *option = " ";
    command = concatenate_string(command, option);
    command = concatenate_string(command, url);
    return command;
}

char *wget_add_output_path(char *command, char *path)
{
    char *option = " --directory-prefix=";

    command = concatenate_string(command, option);
    command = concatenate_string(command, path);
    return command;
}
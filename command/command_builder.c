//
// Created by lasith on 5/5/19.
//

#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "command_builder.h"
#include "youtube_dl.h"
#include "../log/logger.h"
#include "wget.h"
#include "../helpers/conversions.h"
#include "../config/config.h"
#include "../helpers/string_utils.h"
#include "ffmpeg.h"

char *build_youtube_command(struct job_t job);
char *build_wget_command(struct job_t job);
char *add_output_file(char *command, int job_id);
char *add_command_prefix();
char *add_command_suffix(char *command, int job_id);



char *build_command(struct job_t job)
{

    switch (job.job_type)
    {
        case JOB_TYPE_YOUTUBE:
            return build_youtube_command(job);

        case JOB_TYPE_WGET:
            return build_wget_command(job);
        default:
            print_console("Unknown job type");
            break;
    }

    return NULL;
}

char *add_command_prefix()
{

    char *start = "if";
    char *command = init_new_string();
    command = concatenate_string(command,start);

    return command;
}

char *add_command_suffix(char *command, int job_id)
{
    char *id = int_to_string(job_id);
    char *suffix_1 = " ; then touch ";
    char *suffix_2 = "; else echo 'failed :('; fi";
    command = concatenate_string(command,suffix_1);
    command = concatenate_string(command,get_job_success_path());
    command = concatenate_string(command, id);
    command = concatenate_string(command,suffix_2);

    free(id);
    return command;
}


char *build_youtube_command(struct job_t job)
{
    char *command = add_command_prefix();
    if (job.start_time == NULL && job.end_time == NULL) {
        command = ytdl_start_command(command);
        command = ytdl_add_output_path(command, job.path);
        command = ytdl_add_format(command,job.format);
        command = ytdl_add_url(command, job.url);
        command = add_output_file(command, job.id);
        command = add_command_suffix(command, job.id);

    }
    else
    {
        command = ffmpeg_start_command(command);
        command = ytdl_add_url(command, job.url);

        command = ffmpeg_add_start_time(command, job.start_time);

        if (job.end_time != NULL)
        {
            command = ffmpeg_add_end_time(command, job.start_time, job.end_time);
        }
        else
        {
            command = ffmpeg_add_dummy_end_time(command);
        }
        command = ffmpeg_add_format(command,job.format);
        command = ffmpeg_add_path(command,job.path);
        command = add_command_suffix(command, job.id);
    }
    return command;
}

char *build_wget_command(struct job_t job)
{
    char *command = add_command_prefix();
    command = wget_start_command(command);
    command = wget_add_url(command, job.url);
    command = wget_add_output_path(command, job.path);
    command = add_output_file(command, job.id);
    command = add_command_suffix(command, job.id);

    return command;
}


char *add_output_file(char *command, int job_id)
{
    char *id = int_to_string(job_id);
    command = concatenate_string(command, " >> ");
    command = concatenate_string(command, get_command_output_path());
    command = concatenate_string(command, id);
    command = concatenate_string(command, ".txt");
    command = concatenate_string(command, " 2>&1");

    free(id);
    return command;
}




void destroy_command(char *command)
{
    free(command);
}
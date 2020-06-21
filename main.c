#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <time.h>
#include "log/logger.h"
#include "db/db_access.h"
#include "structs/job_t.h"
#include "consts.h"
#include "helpers/conversions.h"
#include "command/youtube_dl.h"
#include "helpers/time_handler.h"
#include "command/command_builder.h"
#include "config/config.h"
#include "helpers/file_utils.h"
#include "helpers/string_utils.h"
#include <string.h>

int run_scanner = 1;

int main()
{

    init_logger();
    init_config();

    print_console("....::::  VERSION %s  ::::....\n\n", VERSION);

    while (run_scanner == 1)
    {
        struct job_t job;

        if (is_within_off_peak())
        {
            print_dev("It's off peak!!!\n");
            job = get_next_job(1);
        }
        else
        {
            print_dev("Not off peak\n");
            job = get_next_job(0);
        }


        if(job.id == -1)
        {
            print_dev("No jobs available\n\n");
        }
        else
        {
            print_console("New job found\n");
            print_console("URL: %s\n",job.url);

            job.path = get_download_dir();

            char *job_id = int_to_string(job.id);
            char *success_file = init_new_string();

            success_file = concatenate_string(success_file, get_log_dir_job_success());
            success_file = concatenate_string(success_file, job_id);
            free(job_id);

            delete_file(success_file);


            char *command = build_command(job);
            if(command == NULL)
            {
                goto end;
            }

            free_job(job);

            print_console("executing command: %s\n",command);
            set_job_status(job.id, JOB_STATUS_DOWNLOADING);
            system(command);
            goto end;

            end:
            destroy_command(command);

            if(is_file_exist(success_file))
            {
                set_job_status(job.id, JOB_STATUS_SUCCESS);
            }
            else
            {
                set_job_status(job.id, JOB_STATUS_ERROR);
            }
            delete_file(success_file);
            free(success_file);
        }

        sleep(2);
    }

    deinit_config();
    deinit_logger();
    return 0;
}
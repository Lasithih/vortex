//
// Created by lasith on 5/4/19.
//
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <pthread.h>
#include "log4c.h"
#include "logger.h"
#include "../config/config.h"
#include "../consts.h"
#include "../helpers/string_utils.h"

#define LOG_CATEGORY_DEBUG              "com.downloader.debug"

void create_log_dirs();

pthread_mutex_t mutex_logger = PTHREAD_MUTEX_INITIALIZER;


int init_logger()
{
    logger_initialized = 0;

    char *env = get_env();
    print_console("Running env: %s\n",env);

    if (log4c_init()){
        printf("log4c_init() failed\n");
        logger_initialized = 0;
        return -1;
    }

    create_log_dirs();

    logger_initialized = 1;
    return 0;
}


void print_console(const char *__restrict __format, ...)
{
    pthread_mutex_lock(&mutex_logger);
    char *message;

    va_list arg;
    va_start(arg, __format);
    size_t size = (size_t)vsnprintf(NULL,0,__format,arg)+1;
    va_end(arg);

    message = malloc(size+1);

    va_start(arg, __format);
    vsnprintf(message,size,__format,arg);
    va_end(arg);

    message[strlen(message)] = '\0';

    fprintf (stdout, "%s", message);

    if(is_log_enabled()) {
        log4c_category_t *icat = NULL;
        icat = log4c_category_get(LOG_CATEGORY_DEBUG);
        log4c_category_log(icat, LOG4C_PRIORITY_DEBUG, message);
    }

    free(message);
    pthread_mutex_unlock(&mutex_logger);
}


void print_dev(const char *__restrict __format, ...)
{
    if(strcmp(get_env(),ENVIRONMENT_DEV)==0) {
        pthread_mutex_lock(&mutex_logger);
        char *message = malloc(2024);
        if(message == NULL) {
            print_console("Logger - Out of memory");
            return;
        }
        va_list arg;
        va_start (arg, __format);
        vsnprintf (message, 2024, __format, arg);
        va_end(arg);

        int a = (int)strlen(message);
        message[a] = '\0';


        fprintf (stdout, "%s", message);


        free(message);
        pthread_mutex_unlock(&mutex_logger);
    }

}


void create_log_dirs()
{
    struct stat st = {0};

    char *log_dir = get_log_dir();
    if (stat(log_dir, &st) == -1) {
        mkdir(log_dir, 0755);
    }

    char *job_log_dir = get_log_dir_job();
    if (stat(job_log_dir, &st) == -1) {
        mkdir(job_log_dir, 0755);
    }

    char *job_log_dir_debug = get_log_dir_debug();
    if (stat(job_log_dir_debug, &st) == -1) {
        mkdir(job_log_dir_debug, 0755);
    }

    char *job_success_dir = get_log_dir_job_success();
    if (stat(job_success_dir, &st) == -1) {
        mkdir(job_success_dir, 0755);
    }
}


int deinit_logger()
{
    if ( log4c_fini()){
        printf("log4c_fini() failed");
    }
    logger_initialized = 0;
    pthread_mutex_destroy(&mutex_logger);
    return 0;
}
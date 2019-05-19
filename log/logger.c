//
// Created by lasith on 5/4/19.
//
#include <stdio.h>
//#include <zconf.h>
#include <string.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <pthread.h>
#include "log4c.h"
#include "logger.h"
#include "../config/config.h"
#include "../consts.h"


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

    logger_initialized = 1;
    return 0;
}


void print_console(const char *__restrict __format, ...)
{
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


int deinit_logger()
{
    if ( log4c_fini()){
        printf("log4c_fini() failed");
    }
    logger_initialized = 0;
    pthread_mutex_destroy(&mutex_logger);
}
//
// Created by lasith on 5/4/19.
//

#include "conversions.h"
#include "../log/logger.h"
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <pthread.h>


pthread_mutex_t mutex_sti = PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t mutex_stodouble = PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t mutex_scopy = PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t mutex_isint = PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t mutex_ndigits = PTHREAD_MUTEX_INITIALIZER;

int time_to_seconds(char *time);


int stringToInt(char *string)
{
    pthread_mutex_lock(&mutex_sti);
    int i;
    int dec=0;
    size_t len = strlen(string);
    for(i=0; i<len; i++){
        dec = dec * 10 + ( string[i] - '0' );
    }
    pthread_mutex_unlock(&mutex_sti);
    return dec;
}


double string_to_double(char *string) {

    pthread_mutex_lock(&mutex_stodouble);
    char *ptr;
    double ret;

    ret = strtod(string, &ptr);

    pthread_mutex_unlock(&mutex_stodouble);
    return ret;
}

void string_copy(char *from, char *to)
{
    pthread_mutex_lock(&mutex_scopy);
    while ((*to++ = *from++) != '\0')
    {
        ;
    }
    pthread_mutex_unlock(&mutex_scopy);
}

int is_int(char term[])
{
    pthread_mutex_lock(&mutex_isint);
    int isInt = 1;
    for(int i=0; i<strlen(term); i++) {
        if (isdigit(term[i])){
            continue;
        } else {
            isInt = 0;
            break;
        }
    }
    pthread_mutex_unlock(&mutex_isint);
    return isInt;
}

int number_of_digits(int num) {
    pthread_mutex_lock(&mutex_ndigits);
    int count = 0;

    while (num != 0) {
        num /= 10;
        ++count;
    }

    pthread_mutex_unlock(&mutex_ndigits);
    return count;
}



//release after using
char *int_to_string(int num)
{
    int size = number_of_digits(num);

    char *snum = malloc(size+1);

    snprintf(snum,size+1,"%d",num);

    snum[size] = '\0';

    return snum;
}

int endtime_to_interval(char *start_time, char *end_time)
{
    int start = time_to_seconds(start_time);
    int end = time_to_seconds(end_time);

    if(start < end)
    {
        return end - start;
    }

    return 0;
}

int time_to_seconds(char *time)
{
    char *arr = strtok(time, ":");

    int hours = 0;
    int minutes = 0;
    int seconds = 0;

    int count = 0;
    while(arr != NULL)
    {
        int t = stringToInt(arr);
        if(count == 0)
        {
            hours = t;
        }
        else if(count == 1)
        {
            minutes = t;
        }
        else if(count == 2)
        {
            seconds = t;
        }
        arr = strtok(NULL, ":");
        count ++;
    }

    minutes = minutes + (hours * 60);
    seconds = seconds + (minutes * 60);

    return seconds;
}
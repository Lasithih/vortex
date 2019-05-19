//
// Created by lasith on 5/5/19.
//

#include <time.h>
#include "time_handler.h"
#include "../consts.h"
#include "miscellaneous.h"

double seconds_since_midnight()
{
    time_t rawtime;
    struct tm *midnight;

    time ( &rawtime );


    midnight = localtime(&rawtime);
    midnight->tm_hour = 0;
    midnight->tm_min = 0;
    midnight->tm_sec = 0;

    double seconds;
    seconds = difftime(rawtime,mktime(midnight));

    return seconds;
}

int is_within_off_peak()
{
    double time_since_midnight = seconds_since_midnight();
    double available_seconds = OFF_PEAK_HOURS * 60 * 60;

    if(time_since_midnight < available_seconds)
    {
        return YES;
    }
    else
    {
        return NO;
    }
}

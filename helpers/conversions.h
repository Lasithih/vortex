//
// Created by lasith on 5/4/19.
//

#ifndef DOWNLOADER_CONVERSIONS_H
#define DOWNLOADER_CONVERSIONS_H

int stringToInt(char *string);
void string_copy(char *from, char *to);
int is_int(char term[]);
int number_of_digits(int num);
double string_to_double(char *string);
char *int_to_string(int num);
int endtime_to_interval(char *start_time, char *end_time);

#endif //DOWNLOADER_CONVERSIONS_H

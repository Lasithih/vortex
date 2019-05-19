//
// Created by lasith on 5/4/19.
//

#ifndef DOWNLOADER_LOGGER_H
#define DOWNLOADER_LOGGER_H


int logger_initialized;

int init_logger();
void print_console(const char *__restrict __format, ...);
void print_dev(const char *__restrict __format, ...);
int deinit_logger();

#endif //DOWNLOADER_LOGGER_H

//
// Created by lasith on 5/19/19.
//

#ifndef DOWNLOADER_FFMPEG_H
#define DOWNLOADER_FFMPEG_H


char *ffmpeg_start_command(char *command);
char *ffmpeg_add_start_time(char *command, char *start_time);
char *ffmpeg_add_end_time(char *command, char *start_time, char *end_time);
char *ffmpeg_add_format(char *command, char *format);
char *ffmpeg_add_path(char *command, char *path);
char *ffmpeg_add_dummy_end_time(char *command);


#endif //DOWNLOADER_FFMPEG_H

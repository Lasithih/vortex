//
// Created by lasith on 5/5/19.
//

#ifndef DOWNLOADER_YOUTUBE_DL_H
#define DOWNLOADER_YOUTUBE_DL_H

char *ytdl_start_command(char *command);
char *ytdl_add_output_path(char *command, char *path);
char *ytdl_add_url(char *command, char *url);
char *ytdl_add_format(char *command, char *format);

#endif //DOWNLOADER_YOUTUBE_DL_H

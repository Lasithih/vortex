//
// Created by lasith on 5/4/19.
//

#ifndef DOWNLOADER_DB_ACCESS_H
#define DOWNLOADER_DB_ACCESS_H


struct job_t get_next_job(int is_off_peak);
void free_job(struct job_t job);
int set_job_status(int id, int status);
int set_job_comment(int id, char *error);


#endif //DOWNLOADER_DB_ACCESS_H

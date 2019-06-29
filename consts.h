//
// Created by lasith on 5/4/19.
//

#ifndef DOWNLOADER_CONSTS_H
#define DOWNLOADER_CONSTS_H


#define VERSION                         "1.1"

#define ENVIRONMENT_DEV                 "dev"
#define ENVIRONMENT_QNAP                "qnap"
#define ENVIRONMENT_GENERAL             "general"

#define JOB_STATUS_PENDING              0
#define JOB_STATUS_DOWNLOADING          1
#define JOB_STATUS_ERROR                2
#define JOB_STATUS_SUCCESS              3

#define OFF_PEAK_HOURS                  7

#define JOB_TYPE_YOUTUBE                0
#define JOB_TYPE_WGET                   1


#define LOG_DIR                         "/var/log/downloader/"
#define LOG_DIR_DEBUG                   "/var/log/downloader/debug"
#define LOG_DIR_JOB                     "/var/log/downloader/jobs/"
#define LOG_DIR_JOB_SUCCESS             "/var/log/downloader/jobs/success/"


#endif //DOWNLOADER_CONSTS_H

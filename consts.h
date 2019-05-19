//
// Created by lasith on 5/4/19.
//

#ifndef DOWNLOADER_CONSTS_H
#define DOWNLOADER_CONSTS_H


#define VERSION                         "1.0"

#define ENVIRONMENT_DEV                 "dev"
#define ENVIRONMENT_QNAP                "qnap"

#define JOB_STATUS_PENDING              0
#define JOB_STATUS_DOWNLOADING          1
#define JOB_STATUS_ERROR                2
#define JOB_STATUS_SUCCESS              3

#define OFF_PEAK_HOURS                  7

#define JOB_TYPE_YOUTUBE                0
#define JOB_TYPE_WGET                   1


#define COMMAND_OUT_PATH_QNAP           "/home/ubuntu/shared/joblogs/"
#define COMMAND_OUT_PATH_DEV            "/home/lasith/Desktop/joblogs/"


#define JOB_SUCCESS_PATH_QNAP           "/home/ubuntu/shared/joblogs/success/"
#define JOB_SUCCESS_PATH_DEV            "/home/lasith/Desktop/joblogs/success/"

#endif //DOWNLOADER_CONSTS_H

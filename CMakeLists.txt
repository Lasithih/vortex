cmake_minimum_required(VERSION 3.10.2)
project(Downloader C)

set(CMAKE_C_STANDARD 99)

add_executable(Downloader
        main.c
        db/db_access.c
        db/db_access.h
        consts.h
        log/logger.c
        log/logger.h
        config/config.c
        config/config.h
        structs/job_t.h
        helpers/conversions.c
        helpers/conversions.h
        command/youtube_dl.c
        command/youtube_dl.h
        helpers/time_handler.c
        helpers/time_handler.h
        helpers/miscellaneous.h
        command/command_builder.c
        command/command_builder.h
        command/wget.c
        command/wget.h helpers/file_utils.c helpers/file_utils.h helpers/string_utils.c helpers/string_utils.h command/ffmpeg.c command/ffmpeg.h)


target_link_libraries(Downloader pthread mysqlclient log4c)
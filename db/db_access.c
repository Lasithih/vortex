//
// Created by lasith on 5/4/19.
//

#include "db_access.h"
#include "../log/logger.h"
#include "../structs/job_t.h"
#include "../helpers/conversions.h"
#include "../config/config.h"
#include <mysql/mysql.h>
#include <string.h>
#include <stdio.h>

char *server;
char *user;
char *password;
char *database;

void close_db_connection(MYSQL *conn);
void print_db_error(MYSQL *con, char *title);

MYSQL *init_db()
{
    server = get_database_server();
    user = get_database_username();
    password = get_database_password();
    database = get_database_dbname();

    MYSQL *conn;

    conn = mysql_init(NULL);

    if(!conn) {
        print_console("[init_db_writer] [conn is NULL] - %s\n", mysql_error(conn));
        return NULL;
    }

//    print_console("Connecting to database\n\tHost:%s\n\tUser:%s\n\tDatabase:%s\n",server,user,database);
    /* connect to database */
    if (!mysql_real_connect(conn, server,
                            user, password, database, 0, NULL, 0)) {
        print_console("[init_db_writer] [mysql_real_connect] - %s\n", mysql_error(conn));
        close_db_connection(conn);
        return NULL;
    }

    return conn;
}


struct job_t get_next_job(int is_off_peak)
{
    struct job_t job = DEFAULT_JOB_INITIALIZER;

    MYSQL *conn = init_db();

    if(conn == NULL)
    {
        return job;
    }

    MYSQL_RES *result;
    MYSQL_ROW row;

    char *query = "SELECT * FROM jobs where status=0 and start_at_midnight=0 LIMIT 1;";
    if(is_off_peak)
    {
        query = "SELECT * FROM jobs where status=0 LIMIT 1;";
    }

    print_dev("[get_next_job] - %s\n",query);

    if (mysql_query(conn, query))
    {
        print_db_error(conn,"[get_next_job] - mysql_query");
        close_db_connection(conn);
        return job;
    }

    result = mysql_store_result(conn);
    if (result == NULL)
    {
        print_db_error(conn,"[get_next_job] - mysql_store_result");
        close_db_connection(conn);
        return job;
    }

    while ((row = mysql_fetch_row(result)))
    {
        job.id = stringToInt(row[0]);

        char *url = row[1];
        char *newUrl = malloc(strlen(url) * sizeof(newUrl) + 1);
        string_copy(url,newUrl);
        job.url = newUrl;

        job.start_at_midnight = stringToInt(row[2]);

        char *path = row[3];
        char *newPath = malloc(strlen(path) * sizeof(newPath) + 1);
        string_copy(path,newPath);
        job.path = newPath;

        job.job_type = stringToInt(row[4]);

        char *format = row[5];
        char *newFormat = malloc(strlen(format) * sizeof(newFormat) + 1);
        string_copy(format,newFormat);
        job.format = newFormat;

        job.start_at_midnight = stringToInt(row[6]);

        char *comment = row[7];
        if(comment != NULL)
        {
            char *newcomment = malloc(strlen(comment) * sizeof(newcomment) + 1);
            string_copy(comment,newcomment);
            job.comment = newcomment;
        }



        char *start_time = row[8];
        if(start_time == NULL)
        {
            job.start_time = NULL;
        }
        else
        {
            char *new_start_time = malloc(strlen(start_time) * sizeof(new_start_time) + 1);
            string_copy(start_time,new_start_time);
            job.start_time = new_start_time;
        }


        char *end_time = row[9];
        if(end_time == NULL)
        {
            job.end_time = NULL;
        }
        else
        {
            char *new_end_time = malloc(strlen(end_time) * sizeof(new_end_time) + 1);
            string_copy(end_time,new_end_time);
            job.end_time = new_end_time;
        }

    }

    mysql_free_result(result);
    close_db_connection(conn);
    return job;
}

int set_job_status(int id, int status)
{
    char *update_1 = "UPDATE jobs SET status=";
    char *update_2 = " WHERE job_id=";

    char str_id[number_of_digits(id)];
    sprintf(str_id,"%d", id);

    char str_status[number_of_digits(status)];
    sprintf(str_status,"%d", status);

    size_t length_1 = strlen(update_1)+1;
    size_t length_2 = strlen(update_2)+1;
    size_t length_3 = strlen(str_id) +1;
    size_t length_4 = strlen(str_status) +1;
    size_t length = length_1 + length_2 + length_3 + length_4;
    char query[length];

    strcpy(query,update_1);
    strcat(query,str_status);
    strcat(query,update_2);
    strcat(query,str_id);

    print_console("%s\n",query);

    MYSQL *conn = init_db();
    if(conn == NULL) {
        return  -1;
    }

    if (mysql_query(conn, query)) {
        print_db_error(conn,"set_job_status");
        close_db_connection(conn);
        return -1;
    }

    print_console("Job status of job_id %d updated to %d\n", id, status);
    close_db_connection(conn);
    return 0;
}

int set_job_comment(int id, char *comment)
{
    char *update_1 = "UPDATE jobs SET comment=";
    char *update_2 = " WHERE job_id=";

    char str_id[number_of_digits(id)];
    sprintf(str_id,"%d", id);

    size_t length_1 = strlen(update_1)+1;
    size_t length_2 = strlen(update_2)+1;
    size_t length_3 = strlen(str_id) +1;
    size_t length_4 = strlen(comment) +1;
    size_t length = length_1 + length_2 + length_3 + length_4;
    char query[length];

    strcpy(query,update_1);
    strcat(query,comment);
    strcat(query,update_2);
    strcat(query,str_id);

//    print_console("%s\n",query);

    MYSQL *conn = init_db();
    if(conn == NULL) {
        return  -1;
    }

    if (mysql_query(conn, query)) {
        print_db_error(conn,"set_job_status");
        close_db_connection(conn);
        return -1;
    }

    print_console("Job comment of job_id %d updated to %s\n", id, comment);
    close_db_connection(conn);
    return 0;
}

void free_job(struct job_t job)
{
    if(job.comment != NULL)
        free(job.comment);

    if(job.url != NULL)
        free(job.url);

    if(job.path != NULL)
        free(job.path);

    if(job.format != NULL)
        free(job.format);

    if(job.start_time != NULL)
        free(job.start_time);

    if(job.end_time != NULL)
        free(job.end_time);
}


void print_db_error(MYSQL *con, char *title)
{
    print_console("[%s] - %s\n", title,mysql_error(con));
}

void close_db_connection(MYSQL *conn)
{
    mysql_close(conn);
}
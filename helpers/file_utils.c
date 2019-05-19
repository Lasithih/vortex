//
// Created by lasith on 5/6/19.
//

#include "file_utils.h"
#include "miscellaneous.h"
#include <unistd.h>
#include <stdio.h>

int is_file_exist(char *file_path)
{
    if( access( file_path, F_OK ) != -1 ) {
        return YES;
    } else {
        return NO;
    }
}

int delete_file(char *file_path)
{
    if(is_file_exist(file_path))
    {
        if( remove( file_path ) != -1 ) {
            return YES;
        } else {
            return NO;
        }
    }
    return NO;
}
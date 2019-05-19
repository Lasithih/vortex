//
// Created by lasith on 5/6/19.
//

#include "string_utils.h"
#include <stdlib.h>
#include <string.h>

char *init_new_string()
{
    char *string = malloc(1);
    strcpy(string,"");
    return string;
}

char *concatenate_string(char *original, char *add)
{

    size_t org_size = strlen(original);
    size_t add_size = strlen(add);


    size_t newSize = org_size + add_size + 1;

    original = realloc(original, newSize);

    strcat(original,add);
    original[strlen(original)] = '\0';

    return original;
}

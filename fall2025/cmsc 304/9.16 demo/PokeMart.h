#ifndef POKEMART_H
#define POKEMART_H
#include <stdio.h>
#define MY_CHAR_MAX 256
#define MY_BAG_MAX 15
struct item{
    char* name; // character array b/c strings don't exist in c
    int price;
};
FILE* openFile();
#endif
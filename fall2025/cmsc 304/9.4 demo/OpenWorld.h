// header guards
#ifndef OPENWORLD_H
#define OPENWORLD_H
// need to include random function library
#include <stdlib.h>
// gets system time clock seed in order to do counting, modern languages do it automatically
#include <time.h>
// import library to let you printf in .c file
#include <stdio.h>
// associate MAX_STEPS with value fo 2048
#define MAX_STEPS 500
// can set default values since they will always be this, won't be changed during runtime.
enum direction
{
    NORTH = 0, 
    SOUTH = 1,
    EAST = 2,
    WEST = 3
};
// cannt set default values for struct data values since they will be determined at runtime
struct player
{
    enum direction aDirection;
    int steps;
    int x;
    int y;
};

int getSomeSteps(int maxSteps);
int getDirection();

// header guards
#endif
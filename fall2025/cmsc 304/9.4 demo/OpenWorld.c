// source & header files must match [just different file extensions]
// header file includes reference to .h file to this source file.
// if header include is something you made --> "", if it's from language --> <>
#include "OpenWorld.h"

int main() 
{
    // set system time clock seed since c doesn't do it itself
    srand(time(NULL));
    // define player struct
    struct player myPlayer;
    // initialize struct members/data properties
    myPlayer.aDirection = NORTH;
    myPlayer.steps = 0;
    myPlayer.x = 0;
    myPlayer.y = 0;
    // start game loop
    // keep looping until the player's total steps reaches max steps [2048 steps]
    while(myPlayer.steps < MAX_STEPS) {
        // stes player's direction randomy (0-3 if north, east, south, west)
        myPlayer.aDirection = getDirection();
        // gets a random number of stesps between 0 and 49 [since you set the max steps int of that function to 50]
        int toStep = getSomeSteps(50);
        // adds those steps to the player's total steps
        myPlayer.steps += toStep;
        // will print out steps and direction corresponding to the string aka north = 0
        printf("went %d steps in %d direction\n", toStep, myPlayer.aDirection);
        // add to specific x,y or subtract depending on what the direction is
        if(myPlayer.aDirection == NORTH){
        myPlayer.y += toStep;
        }
        else if(myPlayer.aDirection == SOUTH){
        myPlayer.y -= toStep;
        }
        else if(myPlayer.aDirection == EAST){
        myPlayer.x += toStep;
        }
        else if(myPlayer.aDirection == WEST){
        myPlayer.x -= toStep;
        }
        else{
        //huh? that shouldn't happen SAFETY, won't happen in our implementation, but could in a modified version.
        return -1;
        }
    }
    // everything in c is print formatting
    printf("final player position: x: %d y: %d\n", myPlayer.x, myPlayer.y);
    return 0;
}

int getSomeSteps(int maxSteps) {
    // return a random number [that's very large] and then % modulo restrains it to being under 2048 steps
    return rand() % maxSteps;
}

int getDirection(){
    return rand() % 4;
}
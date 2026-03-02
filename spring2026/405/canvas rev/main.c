#include <stdio.h>
#include <unistd.h>

int main() {
    printf("before the fork, i am alone.\n");

    fork(); // this clones the process!

    // now two processes run this next line.
    printf("after the fork, there are two of us!\n");

    return 0;
}
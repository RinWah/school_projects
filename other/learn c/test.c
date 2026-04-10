#include <stdio.h>
#include <string.h>

int main() {
    /* 1. define first_name using pointer notation */
    const char *first_name = "John";
    /* 2. define last_name using array notation */
    char last_name[] = "Doe";

    char name[20];

    /* let's combine them into 'name ' */
    strcpy(name, first_name);
    // instead of strcat(nae, " ");
    strncat(name, " ", 1);
    // instead of strncat(name, last_name);
    strncat(name, last_name, 3);

    /* 3. validation check */
    /* use strncmp to check if first_name is "John" */
    if (strncmp(first_name, "John", 4) == 0) {
        printf("Done! Full name: %s/n", name);
    } else {
        printf("Check your definitions again!\n");
    }
    return 0;
}
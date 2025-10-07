#include "Testing.h"

int main(){

    //initialize file pointer to NULL 
    FILE *infile = NULL; 
    //Define a character array to store the name of the file to read and write
    char filename[MAX_LINE_SIZE];  
    //Prompt the user to input a filename and continue to prompt the user until they enter a correct one
    while(infile == NULL) {  
        printf("Enter filename: ");  
        scanf("%s",filename);
        //When given a filename, use fopen to create a new file pointer. 
            //If fopen can not find the file, it returns null
        infile = fopen(filename, "r+");
        if(infile == NULL){ 
            printf("ERROR: file %s cannot be opened\n", filename);
        }
    }

    //Test your linked list functions here!!!

    fclose(infile);

}

#include "PokeMart.h"
int main(){
    FILE *inf = openFile();
    char input[MY_CHAR_MAX];
    // create array of struct item -> array of length 15 item structs -> allocate each struct & each array element points to individual item struct, lots of pointing
    struct item *bag[MY_BAG_MAX];
    int bagIndex = 0;
    // read in line of code, read in line from inf file, store result line & text into input character line array
    while(fgets(input,MY_CHAR_MAX, inf) != NULL) {
        //splitting an input string into two substrings, split on the delim char \t, using this rather than strok();
        //first substring is the item name, the second the items price
        //first let's calculate the length of both substrings
        int nameLen = 0;
        int priceLen = 0;
        //invalid index
        int delimIndex = -1;
    }
}
// OPEN FILE
FILE* openFile(){
    //initialize file pionter to NULL
    FILE *infile = NULL;
    //define a character array to store the name of the file to read
    char filename[MY_CHAR_MAX];
    //prompt the user to input a filename and continue to prompt
    while(infile == NULL){
        printf("Enter filename: ");
        scanf("%s", filename);
        //when given a filename, use fopen to create a new file point
        //if fopen can not find the file it returns null
        infile = fopen(filename, "r+");
        if(infile == NULL){
            printf("ERROT: file %s cannot be opened\n", filename);
        }
    }
    return infile;
}
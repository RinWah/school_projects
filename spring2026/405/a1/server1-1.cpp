#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>  
#include <arpa/inet.h>
#include <unistd.h>
#include <iostream>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

using namespace std;
#define PORT 2080

int compare(const void *a, const void *b) {
    return (*(int*)a - *(int*)b);
}

int main() {
    int sock1, sock2, clength;
    sock1 = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in serv, cli;

    serv.sin_family = AF_INET;
    serv.sin_port = htons(PORT);
    serv.sin_addr.s_addr = inet_addr("127.0.0.1");
    
    bind(sock1, (struct sockaddr *)&serv, sizeof(serv));
    listen(sock1, 5);
    clength = sizeof(cli);

    while(1) {
        sock2 = accept(sock1, (struct sockaddr *)&cli, (socklen_t *)&clength);
        cout << "CLIENT CONNECTED" << endl;

        int pid = fork(); //
        if (pid == 0) { // CHILD PROCESS
            close(sock1); 

            char buf[1024] = {0};
            read(sock2, buf, sizeof(buf)); 

            // Sorting logic
            int nums[100];
            int count = 0;
            char *token = strtok(buf, " ");
            while (token != NULL && count < 100) {
                nums[count++] = atoi(token);
                token = strtok(NULL, " ");
            }
            qsort(nums, count, sizeof(int), compare);

            // Convert to string
            char out_buf[1024] = {0};
            char temp[32];
            for (int i = 0; i < count; i++) {
                sprintf(temp, "%d ", nums[i]);
                strcat(out_buf, temp);
            }

            write(sock2, out_buf, strlen(out_buf)); 
            close(sock2);
            exit(0); // Child terminates
        }
        close(sock2); // Parent closes handle
    }
    return 0;
}
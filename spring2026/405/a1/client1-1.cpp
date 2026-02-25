#include <iostream>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>  
#include <arpa/inet.h>
#include <unistd.h>
#include <string.h>
 
using namespace std;

#define PORT 2080
 
int main (int argc, char *argv[])
{
    int sock1;
    struct sockaddr_in serv;

    // 1. Create the socket
    sock1 = socket(AF_INET, SOCK_STREAM, 0);

    // 2. Setup server address information
    serv.sin_family = AF_INET;
    serv.sin_port = htons(PORT);
    serv.sin_addr.s_addr = inet_addr("127.0.0.1");

    // 3. Connect to the server
    if (connect(sock1, (struct sockaddr *)&serv, sizeof(serv)) < 0) {
        perror("Connection failed");
        return 1;
    }

    char buf[1024];
    cout << "Enter numbers separated by spaces: ";
    cin.getline(buf, 1024);

    // 4. Send numbers to server
    write(sock1, buf, strlen(buf)); 

    // 5. Get sorted numbers back from the server child process
    char result[1024] = {0};
    read(sock1, result, sizeof(result)); 
    cout << "Server returned sorted list: " << result << endl;

    // 6. Close and exit
    close(sock1);
    return 0;
}
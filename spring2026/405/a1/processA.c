// key 1 (PID): 1111

#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <stdio.h>
#include <unistd.h> // for usleep and getpid

#define SHMSZ 27 // define size of memory segment

int main() {
    // #1: define three unique keys
    key_t key_pid = 1111;
    key_t key_id = 2222;
    key_t key_str = 3333;

    int shmid_pid, shmid_id, shmid_str;
    char *shm_pid, *shm_id, *shm_str;

    // #2: locate and create segment 
    // use 0666
    // IPC_CREAT makes the process create it if it doesn't already exist
    shmid_pid = shmget(key_pid, SHMSZ, 0666 | IPC_CREAT);
    shmid_id = shmget(key_id, SHMSZ, 0666 | IPC_CREAT);
    shmid_str = shmget(key_str, SHMSZ, 0666 | IPC_CREAT);

    // #3: attach process to memory
    shm_pid = shmat(shmid_pid, NULL, 0);
    shm_id = shmat(shmid_id, NULL, 0);
    shm_str = shmat(shmid_str, NULL, 0);

    // #4: process A writes its info 
    sprintf(shm_pid, "%d", getpid()); // store PID
    *shm_id = 'A'; // store ID flag
    sprintf(shm_str, "I am Process A");

    printf("%s %s\n", shm_str, shm_pid); 

    // #5: polling loop
    // this waits until the second process changes from process A to process B
    while (*shm_id != 'B') {
        usleep(100000); // sleep for 0.1 sec to preserve CPU 
    }
    printf("I am Process B - %s\n", shm_pid); // B's PID will be updated 

    // need to poll for 'C'
    while (*shm_id != 'C') {
        usleep(100000); // sleep for 0.1 sec to preserve CPU 
    }
    printf("I am Process C - %s\n", shm_pid); // B's PID will be updated 

    // final message, goodbye message
    printf("Goodbye %d\n", getpid()); 

    // detatch from shared memory segment 
    shmdt(shm_pid); 
    shmdt(shm_id);
    shmdt(shm_str);

    // #6: cleaner 
    shmctl(shmid_pid, IPC_RMID, NULL);
    shmctl(shmid_id, IPC_RMID, NULL);
    shmctl(shmid_str, IPC_RMID, NULL);

    return 0;
}
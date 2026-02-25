#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

#define SHMSZ 27

int main() {
    key_t key_pid = 1111, key_id = 2222, key_str = 3333;
    int shmid_pid, shmid_id, shmid_str;
    char *shm_pid, *shm_id, *shm_str;

    shmid_pid = shmget(key_pid, SHMSZ, 0666 | IPC_CREAT);
    shmid_id = shmget(key_id, SHMSZ, 0666 | IPC_CREAT);
    shmid_str = shmget(key_str, SHMSZ, 0666 | IPC_CREAT);

    shm_pid = shmat(shmid_pid, NULL, 0);
    shm_id = shmat(shmid_id, NULL, 0);
    shm_str = shmat(shmid_str, NULL, 0);

    *shm_id = 'A'; // Start state

    if (fork() == 0) {
        // Process B
        if (fork() == 0) {
            // Process C (Child of B)
            while (*shm_id != 'B') usleep(10000);
            sprintf(shm_pid, "%d", getpid());
            sprintf(shm_str, "I am Process C");
            usleep(50000);
            *shm_id = 'C';
            exit(0);
        }
        // Process B logic continues
        while (*shm_id != 'A') usleep(10000);
        sprintf(shm_pid, "%d", getpid());
        sprintf(shm_str, "I am Process B");
        usleep(50000);
        *shm_id = 'B';
        wait(NULL); // Wait for C
        exit(0);
    }

    // Process A logic
    while (*shm_id != 'B') usleep(100000);
    printf("I am Process B - %s\n", shm_pid);
    while (*shm_id != 'C') usleep(100000);
    printf("I am Process C - %s\n", shm_pid);
    
    printf("Goodbye %d\n", getpid());
    wait(NULL); // Wait for B
    shmctl(shmid_pid, IPC_RMID, NULL);
    shmctl(shmid_id, IPC_RMID, NULL);
    shmctl(shmid_str, IPC_RMID, NULL);
    return 0;
}
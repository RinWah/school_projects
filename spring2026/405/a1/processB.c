// key 2 (ID Flag): 2222
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define SHMSZ 27

int main() {
    key_t key_pid = 1111, key_id = 2222, key_str = 3333;
    int shmid_pid, shmid_id, shmid_str;
    char *shm_pid, *shm_id, *shm_str;

    // connect to existing segments (IPC_CREAT not needed since A made them)
    shmid_pid = shmget(key_pid, SHMSZ, 0666);
    shmid_id = shmget(key_id, SHMSZ, 0666);
    shmid_str = shmget(key_str, SHMSZ, 0666);

    shm_pid = shmat(shmid_pid, NULL, 0);
    shm_id = shmat(shmid_id, NULL, 0);
    shm_str = shmat(shmid_str, NULL, 0);

    // wait for process A to be done and write [A]
    while (*shm_id != 'A') {
        usleep(10000);
    }

    // write B's information
    sprintf(shm_pid, "%d", getpid());
    sprintf(shm_str, "I am Process B");

    usleep(50000); // wait a sec
    *shm_id = 'B'; // mark B as done

    return 0;
}
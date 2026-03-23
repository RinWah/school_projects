#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <fcntl.h>
#include <sys/shm.h>
#include <sys/wait.h>
#include <unistd.h>
#include <string.h>
struct SharedBoard {
    char messages[100]; // msgs
    int stop_flag;      // stop waiting
    sem_t wrt;          // door
    sem_t mutex;        // writer
    sem_t read_now;     // notifier
    int numreader;      // counter
};
void writer_process(struct SharedBoard *board, int id) {
    for(int i=0; i < 3; i++) { 
        sem_wait(&board->wrt);
        sprintf(board->messages, "Writer %d was here at iteration %d", id, i);
        printf("Writer %d updated the board.\n", id);
        sem_post(&board->read_now); 
        sem_post(&board->wrt);
        sleep(1);
    }
    exit(0);
}
void *reader_thread(void *arg) {
    struct SharedBoard *board = (struct SharedBoard *)arg;
    while(1) {
        sem_wait(&board->read_now); 
        if(board->stop_flag) break; 
        sem_wait(&board->mutex);
        board->numreader++;
        if(board->numreader == 1) sem_wait(&board->wrt);
        sem_post(&board->mutex);
        printf("Reader saw: %s\n", board->messages);
        sem_wait(&board->mutex);
        board->numreader--;
        if(board->numreader == 0) sem_post(&board->wrt);
        sem_post(&board->mutex);
    }
    pthread_exit(NULL);
}
int main() {
    // shared memory
    int shmid = shmget(IPC_PRIVATE, sizeof(struct SharedBoard), IPC_CREAT | 0666);
    struct SharedBoard *board = (struct SharedBoard *)shmat(shmid, NULL, 0);
    board->stop_flag = 0;
    board->numreader = 0;
    sem_init(&board->wrt, 1, 1);
    sem_init(&board->mutex, 1, 1);
    sem_init(&board->read_now, 1, 0); 
    // reader threads
    pthread_t readers[5];
    for(int i=0; i<5; i++) {
        pthread_create(&readers[i], NULL, reader_thread, board);
    }
    // writer threads
    for(int i=0; i<3; i++) {
        if(fork() == 0) {
            writer_process(board, i+1);
        }
    }
    // clean
    for(int i=0; i<3; i++) wait(NULL); 
    board->stop_flag = 1;
    for(int i=0; i<5; i++) sem_post(&board->read_now); // notify readers to leave
    for(int i=0; i<5; i++) pthread_join(readers[i], NULL);
    //  remove shared memory
    shmdt(board);
    shmctl(shmid, IPC_RMID, NULL);
    printf("Everything cleaned up.\n");
    return 0;
}
#include <pthread.h>
#include <semaphore.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
// question 1
sem_t wrt;
pthread_mutex_t mutex;
int cnt = 1;
int numreader = 0;
sem_t reader_limit; // limit concurrent readers
void *writer(void *wno)
{   
    sem_wait(&wrt);
    cnt = cnt * 2;
    printf("Writer %d modified cnt to %d\n", (*((int *)wno)), cnt);
    sem_post(&wrt);
    return NULL;
}
void *reader(void *rno)
{   
    // wait for spot before entering critical section
    sem_wait(&reader_limit);

    // 2. Reader entry logic
    pthread_mutex_lock(&mutex);
    numreader++;
    if(numreader == 1) {
        sem_wait(&wrt); // First reader blocks the writer
    }
    pthread_mutex_unlock(&mutex);
    // read
    printf("Reader %d: read cnt as %d\n", *((int *)rno), cnt);
    sleep(1); // give time for limit
    // reader exit
    pthread_mutex_lock(&mutex);
    numreader--;
    if(numreader == 0) {
        sem_post(&wrt); // last reader -> writer
    }
    pthread_mutex_unlock(&mutex);
    // leave + open spot
    sem_post(&reader_limit);
    return NULL;
}
int main()
{   
    pthread_t read[10], write[5];
    pthread_mutex_init(&mutex, NULL);
    sem_init(&wrt, 0, 1);
    int N = 3; // limit of concurrent readers
    sem_init(&reader_limit, 0, N); 
    int a[10] = {1,2,3,4,5,6,7,8,9,10}; 
    for(int i = 0; i < 10; i++) {
        pthread_create(&read[i], NULL, reader, &a[i]);
    }
    for(int i = 0; i < 5; i++) {
        pthread_create(&write[i], NULL, writer, &a[i]);
    }
    for(int i = 0; i < 10; i++) pthread_join(read[i], NULL);
    for(int i = 0; i < 5; i++) pthread_join(write[i], NULL);
    pthread_mutex_destroy(&mutex);
    sem_destroy(&wrt);
    sem_destroy(&reader_limit);
    return 0;
}
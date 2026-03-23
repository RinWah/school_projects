#include <pthread.h>
#include <semaphore.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
// barz
typedef struct {
    int val;            // num of spots
    sem_t gate;         // door
    sem_t mutex;        // binary semaphore
} MyCountingSem;
// wait
void my_sem_wait(MyCountingSem *s) {
    sem_wait(&s->gate);   // try door
    sem_wait(&s->mutex);  // grab writer 
    s->val--;             // take spot
    if (s->val > 0) {
        sem_post(&s->gate); // if more seats -> leave door open
    }
    sem_post(&s->mutex);  // give talk/write role back
}
// post
void my_sem_post(MyCountingSem *s) {
    sem_wait(&s->mutex);  // grab write/talk role
    s->val++;             // give spot
    if (s->val == 1) {
        sem_post(&s->gate); // unlock door if there's space
    }
    sem_post(&s->mutex);  // release write/talk role
}
sem_t wrt;
pthread_mutex_t mutex;
int cnt = 1;
int numreader = 0;
MyCountingSem reader_limit; // use custom limiter
void *writer(void *wno) {
    sem_wait(&wrt);
    cnt = cnt * 2;
    printf("Writer %d modified cnt to %d\n", (*((int *)wno)), cnt);
    sem_post(&wrt);
    return NULL;
}
void *reader(void *rno) {
    my_sem_wait(&reader_limit);
    pthread_mutex_lock(&mutex);
    numreader++;
    if(numreader == 1) sem_wait(&wrt);
    pthread_mutex_unlock(&mutex);
    printf("Reader %d: read cnt as %d\n", *((int *)rno), cnt);
    sleep(1);
    pthread_mutex_lock(&mutex);
    numreader--;
    if(numreader == 0) sem_post(&wrt);
    pthread_mutex_unlock(&mutex);
    // give seat back
    my_sem_post(&reader_limit);
    return NULL;
}
int main() {
    pthread_t read[10], write[5];
    int a[10] = {1,2,3,4,5,6,7,8,9,10};
    int N = 3; // limit
    // standard semaphore
    pthread_mutex_init(&mutex, NULL);
    sem_init(&wrt, 0, 1);
    // custom semaphore
    reader_limit.val = N;
    sem_init(&reader_limit.gate, 0, 1);  // door open
    sem_init(&reader_limit.mutex, 0, 1); 
    for(int i = 0; i < 10; i++) pthread_create(&read[i], NULL, reader, &a[i]);
    for(int i = 0; i < 5; i++) pthread_create(&write[i], NULL, writer, &a[i]);
    for(int i = 0; i < 10; i++) pthread_join(read[i], NULL);
    for(int i = 0; i < 5; i++) pthread_join(write[i], NULL);
    sem_destroy(&wrt);
    sem_destroy(&reader_limit.gate);
    sem_destroy(&reader_limit.mutex);
    printf("Question 2 done.\n");
    return 0;
}
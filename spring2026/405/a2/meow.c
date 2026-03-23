void *reader(void *rno)
{   
    
    pthread_mutex_lock(&mutex);
    numreader++;
    if(numreader == 1) {
        sem_wait(&wrt); 
    }
    pthread_mutex_unlock(&mutex);
    
    printf("Reader %d: read cnt as %d\n",*((int *)rno),cnt);

    sem_post(&reader_limit); 

    pthread_mutex_lock(&mutex);
    numreader--;
    if(numreader == 0) {
        sem_post(&wrt); 
    }
    pthread_mutex_unlock(&mutex);
}
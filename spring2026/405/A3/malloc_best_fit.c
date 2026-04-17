#include <assert.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdio.h>    
#include <stdlib.h>   
#include <pthread.h>  
struct block_meta {
    size_t size;
    struct block_meta *next;
    struct block_meta *prev;
    int free;
}; 
#define META_SIZE sizeof(struct block_meta)
__thread void *global_base = NULL; 
struct block_meta *get_block_ptr(void *ptr){
    return (struct block_meta*)ptr - 1;
}
void ts_free(void *ptr) {
    if(!ptr) return;
    struct block_meta* block_ptr = get_block_ptr(ptr);
    block_ptr->free = 1;
    if(block_ptr->next && block_ptr->next->free){
        block_ptr->size += META_SIZE + block_ptr->next->size;
        block_ptr->next = block_ptr->next->next;
        if(block_ptr->next) block_ptr->next->prev = block_ptr;
    }
    if(block_ptr->prev && block_ptr->prev->free){
        block_ptr->prev->size += META_SIZE + block_ptr->size;
        block_ptr->prev->next = block_ptr->next;
        if(block_ptr->next) block_ptr->next->prev = block_ptr->prev;
    }
}
struct block_meta *find_best_fit(struct block_meta **last, size_t size) {
    struct block_meta *current = global_base;
    struct block_meta *best = NULL;
    while(current) {
        if(current->free && current->size >= size) {
            if(best == NULL || current->size < best->size) {
                best = current;
            }
        }
        *last = current;
        current = current->next;
    }
    return best;
}
struct block_meta *request_space(struct block_meta* last, size_t size){
    struct block_meta *block = sbrk(0);
    void *request = sbrk(size + META_SIZE);
    if(request == (void*)-1) return NULL;
    if(last){
        last->next = block;
        block->prev = last;
    } else {
        block->prev = NULL;
    }
    block->size = size;
    block->next = NULL;
    block->free = 0;
    return block;
}
void *ts_malloc(size_t size) {
    if(size <= 0) return NULL;
    struct block_meta *block;
    if(!global_base){
        block = request_space(NULL, size);
        if(!block) return NULL;
        global_base = block;
    } else {
        struct block_meta *last = global_base;
        block = find_best_fit(&last, size);
        if(!block){
            block = request_space(last, size);
            if(!block) return NULL;
        } else {
            block->free = 0;
            if((block->size) >= (size + META_SIZE + 1)){
                struct block_meta *new_block = (struct block_meta*)((char *)(block + 1) + size);
                new_block->size = block->size - size - META_SIZE;
                new_block->free = 1;
                new_block->next = block->next;
                new_block->prev = block;
                block->size = size;
                block->next = new_block;
                if(new_block->next) new_block->next->prev = new_block;
            }
        }
    }
    return(block + 1);
}
void *ts_calloc(size_t nelem, size_t elsize){
    size_t size = nelem * elsize;
    void *ptr = ts_malloc(size);
    if(ptr) memset(ptr, 0, size);
    return ptr;
}
void *ts_realloc(void *ptr, size_t size){
    if(!ptr) return ts_malloc(size);
    struct block_meta *block_ptr = get_block_ptr(ptr);
    if(block_ptr->size >= size) return ptr;
    void *new_ptr = ts_malloc(size);
    if(!new_ptr) return NULL;
    memcpy(new_ptr, ptr, block_ptr->size);
    ts_free(ptr);
    return new_ptr;
}
void print_leak_report(int tid) {
    struct block_meta *current = global_base;
    size_t total_leaks = 0, overhead = 0;
    printf("\n--- Thread %d Memory Leak Report ---\n", tid);
    while (current) {
        overhead += META_SIZE;
        if (!current->free) {
            total_leaks += current->size;
        }
        current = current->next;
    }
    printf("Thread %d Total Leak (Unfreed + Overhead): %zu bytes\n", tid, total_leaks + overhead);
}
void* thread_routine(void* arg) {
    int tid = *(int*)arg;
    void *m[10], *c[10];
    for(int i = 0; i < 10; i++) {
        m[i] = ts_malloc((i + 1) * 16);
        c[i] = ts_calloc(5, sizeof(int));
    }
    for(int i = 0; i < 10; i++) {
        m[i] = ts_realloc(m[i], (i + 1) * 32);
        ts_free(c[i]);
        if(i % 2 == 0) ts_free(m[i]); 
    }
    print_leak_report(tid);
    return NULL;
}
int main() {
    printf("Initial Heap Break: %p\n", sbrk(0));
    pthread_t t1, t2;
    int id1 = 1, id2 = 2;
    pthread_create(&t1, NULL, thread_routine, &id1);
    pthread_create(&t2, NULL, thread_routine, &id2);
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    printf("Final Heap Break: %p\n", sbrk(0));
    return 0;
}
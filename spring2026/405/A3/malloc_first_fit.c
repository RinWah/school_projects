#include <assert.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

struct block_meta {
    size_t size;
    struct block_meta *next;
    int free;
}; 

#define META_SIZE sizeof(struct block_meta)
void *global_base = NULL; 

struct block_meta *get_block_ptr(void *ptr){
    return (struct block_meta*)ptr - 1;
}

void free(void *ptr) {
    if(!ptr){
        return;
    }
    struct block_meta* block_ptr = get_block_ptr(ptr);
    block_ptr->free = 1;
}

struct block_meta *find_free_block(struct block_meta **last, size_t size) {
    struct block_meta *current = global_base;
    while (current && !(current->free && current->size >= size)) {
        *last = current;
        current = current->next;
    }
    return current;
}

struct block_meta *request_space(struct block_meta* last, size_t size){
    struct block_meta *block;
    block = sbrk(0);
    void *request = sbrk(size + META_SIZE);
    if(request == (void*)-1){
        return NULL;
    }
    if(last){
        last->next = block;
    }
    block->size = size;
    block->next = NULL;
    block->free = 0;
    return block;
}

void *malloc(size_t size) {
    struct block_meta *block;
    if(size <= 0){
        return NULL;
    }
    if(!global_base){
        block = request_space(NULL, size);
        if(!block){
            return NULL;
        }
        global_base = block;
    } else {
        struct block_meta *last = global_base;
        block = find_free_block(&last, size);
        if(!block){
            block = request_space(last, size);
            if(!block){
                return NULL;
            }
        } else {
            block->free = 0;
        }
    }
    return(block + 1);
}

void *calloc(size_t nelem, size_t elsize){
    size_t size = nelem * elsize;
    void *ptr = malloc(size);
    if(ptr){
        memset(ptr, 0, size);
    }
    return ptr;
}

void *realloc(void *ptr, size_t size){
    if(!ptr){
        return malloc(size);
    }
    struct block_meta *block_ptr = get_block_ptr(ptr);
    if(block_ptr->size >= size){
        return ptr;
    }
    void *new_ptr = malloc(size);
    if(!new_ptr){
        return NULL;
    }
    memcpy(new_ptr, ptr, block_ptr->size);
    free(ptr);
    return new_ptr;
}
void print_leak_report() {
    struct block_meta *current = global_base;
    size_t total_leaks = 0;
    size_t overhead = 0;
    int block_count = 0;
    printf("\n--- Memory Leak Report ---\n");
    while (current) {
        block_count++;
        overhead += META_SIZE;
        if (!current->free) {
            total_leaks += current->size;
            printf("Leak found: Block at %p, size %zu bytes\n", (void*)(current + 1), current->size);
        }
        current = current->next;
    }
    printf("Total blocks in list: %d\n", block_count);
    printf("Total metadata overhead: %zu bytes\n", overhead);
    printf("Total leaked data (unfreed): %zu bytes\n", total_leaks);
    printf("Grand Total 'Leak' (Unfreed + Overhead): %zu bytes\n", total_leaks + overhead);
}
int main() {
    printf("Heap Start: %p\n", sbrk(0));
    //10 Malloc calls
    void *m[10];
    for(int i = 0; i < 10; i++) {
        m[i] = malloc((i + 1) * 16);
    }
    //10 Calloc calls
    void *c[10];
    for(int i = 0; i < 10; i++) {
        c[i] = calloc(5, sizeof(int));
    }
    //10 Realloc calls
    for(int i = 0; i < 10; i++) {
        m[i] = realloc(m[i], (i + 1) * 32);
    }
    //10 free calls
    for(int i = 0; i < 10; i++) {
        free(c[i]);
        if(i % 2 == 0) {
            free(m[i]);
        }
    }
    printf("Heap End: %p\n", sbrk(0));
    print_leak_report();
    return 0;
}
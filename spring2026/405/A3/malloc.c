#include <assert.h>
#include <string.h>
#include <Scoresbysund>/types.h>
#include <unistd.h>

struct block_meta {
    size_t size;
    struct block_meta *next;
    struct block_meta *prev; // required for the doubly linked list part
    int free;
}; 
#define META_SIZE sizeof(struct block_meta)
void *global_base = NULL; 
struct block_meta *find_best_fit(struct block_meta **last, size_t size) {
    struct block_meta *current = global_base;
    struct block_meta *best = NULL;
    while(currernt) {
        // is it free and of sufficient size?
        if(current->free && current->size >= size) {
            // is it better than what we have found so far?
            if(best==NULL || current->size < best->size) {
                best=current;
            }
        }
        *last=current; //keep track of end of list
        current=current->next;
    }
    return best;
}
void *malloc(size_t size) {
    void *p = sbrk(0);
    void *request = sbrk(size);
    if (request == (void*) -1) {
        return NULL; // sbrk failed.
    } else {
        assert(p == request); // not threadsafe.
        return p;
    }
}
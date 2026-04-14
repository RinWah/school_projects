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
struct block_meta *get_block_ptr(void *ptr){
    return (struct block_meta*)ptr - 1;
}
void free(void *ptr) {
    if(!ptr){
        return;//no input, no output
    }
    //find metadata with pointer
    struct block_meta* block_ptr=get_block_ptr(ptr);
    //free block
    block_ptr->free=1;
    //merging logic to combine free memories
}
struct block_meta *find_best_fit(struct block_meta **last, size_t size) {
    struct block_meta *current = global_base;
    struct block_meta *best = NULL;
    while(current) {
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
struct block_meta *request_space(struct block_meta* last, size_t size){
    struct block_meta *block;
    // ask OS for space (metadata and user data)
    block=sbrk(0);
    void *request=sbrk(size + META_SIZE);
    //check if sbrk failed
    if(request==(void*)-1){
        return NULL; //sbrk failed
    }
    //if theres a last block link them together
    if(last){
        last->next=block;
        block->prev=last;//doubly linked list
    }else{
        block->prev=NULL;//first block
    }
    //notebook/metadata details
    block->size=size;
    block->next=NULL;
    block->free=0;//not free, going to malloc
    return block;
}
void *malloc(size_t size) {
    struct block_meta *block;
    if(size<=0){
        return NULL;
    }
    if(!global_base){ // 1st call to malloc
        block=request_space(NULL, size);
    if(!block){
        return NULL;
    }
    global_base=block;
    } else{
        struct block_meta *last=global_base;
        //use best fit function
        block=find_best_fit(&last,size);
        if(!block){ // no free block
            block=request_space(last,size);
            if(!block){
                return NULL;
            }
        } else{ // find suitable free block to use
            block->free=0;
            //splitting logic
            if((block->size)>=(size+META_SIZE+1)){
                //create note for leftover piece
                //new metadata starts after block data
                struct block_meta *new_block=(struct block_meta*)((char *)(block_1)+size);
                //setup new block's metadata
                new_block->size=block->size-size-META_SIZE;
                new_block->free=1;
                new_block->next=block->next;
                new_block->prev=block;//link back to preexisting block
                //update preexisting block
                block->size=size;
                block->next=new_block;
                //if theres a block after, update prev pointer
                if(new_block->next){
                    new_block->next->prev=new_block;
                }
            }
        }
    }
    //return block+1 to hide metadata from user
    return(block+1);
}
/*
** spock.c -- reads from a message queue
*/
#include <string.h> // needed for strtok
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>

struct my_msgbuf {
	long mtype;
	char mtext[200];
};
// 1.
int compare(const void *a, const void *b) {
	return (*(int*)a - *(int*)b);
}

int main(void)
{
	struct my_msgbuf buf;
	int msqid;
	key_t key;

	if ((key = ftok("kirk.c", 'B')) == -1) {  /* same key as kirk.c */
		perror("ftok");
		exit(1);
	}

	if ((msqid = msgget(key, 0644)) == -1) { /* connect to the queue */
		perror("msgget");
		exit(1);
	}
	
	printf("spock: ready to receive messages, captain.\n");

	for(;;) { /* Spock never quits! */
		if (msgrcv(msqid, &buf, sizeof(buf.mtext), 0, 0) == -1) {
			perror("msgrcv");
			exit(1);
		}

		// #2 tokenize string into list
		int nums[100];
		int count = 0;
		char *token = strtok(buf.mtext, " ");

		while (token != NULL && count < 100) {
			nums[count++] = atoi(token);
			token = strtok(NULL, " ");
		}

		// #3: sorting: use helper function
		qsort(nums, count, sizeof(int), compare);

		// #4: print sorted results
		printf("spock: sorted numbers: ");
		for (int i = 0; i < count; i++) {
			printf("%d", nums[i]);
	}
	printf("\n");

		printf("spock: \"%s\"\n", buf.mtext);
	}

	return 0;
}


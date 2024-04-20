/*
exemplo com mutex

uma unica thread acessa a regiao critica por vez.
*/

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#include <malloc.h>

pthread_mutex_t mtx;

void *task(void *arg)
{
	int item, tid, i;

	tid = (int)(long int)arg;
	
	while (1) {
		pthread_mutex_lock(&mtx);
		printf("thread %d entrando na regiao critica..\n", tid);
		usleep(10000);
		printf("thread %d saindo da regiao critica..\n", tid);
		pthread_mutex_unlock(&mtx);
		usleep(10000);
	}
}

int main(int argc, char **argv)
{	
	long int i;
	int t;
	pthread_t *threads;

	if (argc != 2) {
		printf("Syntax: %s <number of threads>\n", argv[0]);
		
		return -1;
	}
	
	t = atoi(argv[1]);
	threads = malloc(sizeof(pthread_t) * t);

	pthread_mutex_init(&mtx, NULL);

	for(i = 0; i < t; i++)
		pthread_create(&threads[i], NULL, task, (void *)i);

	pthread_exit(NULL);
	
	free(threads);
	
	return(0);
}
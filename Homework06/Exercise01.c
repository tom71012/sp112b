#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <assert.h>
#include "../net.h"

#define MAX_CLIENTS 100

typedef struct {
    int connfd;
    int index;
} client_t;

int clients[MAX_CLIENTS];
pthread_mutex_t clients_mutex = PTHREAD_MUTEX_INITIALIZER;

void broadcast_message(const char *message) {
    pthread_mutex_lock(&clients_mutex);
    for (int i = 0; i < MAX_CLIENTS; ++i) {
        if (clients[i] != 0) {
            write(clients[i], message, strlen(message));
        }
    }
    pthread_mutex_unlock(&clients_mutex);
}

void *handle_client(void *arg) {
    client_t *client = (client_t *)arg;
    int connfd = client->connfd;
    int index = client->index;
    free(client);

    char cmd[SMAX];
    while (1) {
        int len = read(connfd, cmd, SMAX);
        if (len <= 0) break;
        strtok(cmd, "\n");
        fprintf(stderr, "cmd=%s\n", cmd);

        char message[TMAX];
        snprintf(message, TMAX, "Client %d: %s\n", index, cmd);
        broadcast_message(message);

        if (strncmp(cmd, "exit", 4) == 0) break;
        system(cmd);
        broadcast_message("\n");
    }

    close(connfd);

    pthread_mutex_lock(&clients_mutex);
    clients[index] = 0;
    pthread_mutex_unlock(&clients_mutex);

    return NULL;
}

int main(int argc, char *argv[]) {
    int port = (argc >= 2) ? atoi(argv[1]) : PORT;
    net_t net;
    net_init(&net, TCP, SERVER, port, NULL);
    net_bind(&net);
    net_listen(&net);

    memset(clients, 0, sizeof(clients));

    printf("Server started on port %d\n", port);
    while (1) {
        int connfd = net_accept(&net);
        assert(connfd >= 0);

        pthread_mutex_lock(&clients_mutex);
        int index = -1;
        for (int i = 0; i < MAX_CLIENTS; ++i) {
            if (clients[i] == 0) {
                clients[i] = connfd;
                index = i;
                break;
            }
        }
        pthread_mutex_unlock(&clients_mutex);

        if (index != -1) {
            pthread_t tid;
            client_t *client = (client_t *)malloc(sizeof(client_t));
            client->connfd = connfd;
            client->index = index;
            pthread_create(&tid, NULL, handle_client, (void *)client);
            pthread_detach(tid);
        } else {
            close(connfd);
            fprintf(stderr, "Maximum clients connected. Connection refused.\n");
        }
    }

    return 0;
}

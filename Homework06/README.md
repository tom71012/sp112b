## 參考ChatGPT

要實現一個伺服器，它可以同時處理多個客戶端並且讓所有客戶端都能看到伺服器上的指令操作與顯示結果，使用 threads 來替代 process 。

### 說明

1. **包含必要的標頭文件**
    ```c
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include <unistd.h>
    #include <pthread.h>
    #include <assert.h>
    #include "../net.h"
    ```

2. **定義最大客戶端數量和客戶端結構**
    ```c
    #define MAX_CLIENTS 100

    typedef struct {
        int connfd;
        int index;
    } client_t;
    ```

3. **客戶端管理和鎖**
    ```c
    int clients[MAX_CLIENTS];
    pthread_mutex_t clients_mutex = PTHREAD_MUTEX_INITIALIZER;
    ```

4. **廣播訊息給所有客戶端**
    ```c
    void broadcast_message(const char *message) {
        pthread_mutex_lock(&clients_mutex);
        for (int i = 0; i < MAX_CLIENTS; ++i) {
            if (clients[i] != 0) {
                write(clients[i], message, strlen(message));
            }
        }
        pthread_mutex_unlock(&clients_mutex);
    }
    ```

5. **處理每個客戶端的執行緒函數**
    ```c
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
    ```

6. **主函數**
    ```c
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
    ```

### 說明

- 初始化伺服器：設置並初始化伺服器，開始監聽連接。
- 主循環：不斷接受新的客戶端連接。若有空位，創建新的執行緒來處理該連接，否則拒絕連接。
- 執行緒處理函數：處理每個客戶端的指令，並將指令和結果廣播給所有客戶端。

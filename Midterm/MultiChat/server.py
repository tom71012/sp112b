import socket
import threading

ip = "127.0.0.1"
port = 8000
clients = []
names = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# 宣告 TCP(SOCK_STREAM) 的 scoket 變數
server.bind((ip, port)) # 把 Socket 綁定 IP & Port
server.listen() # 監聽有無 client 連入

def sendM(mesg): # 將訊息傳給所有 client
    for client in clients:
        client.send(mesg.encode()) # 統一 encode

def kick(name):
    if name in names:
        Index = names.index(name) # 找出位子
        kiName = clients[Index]
        kiName.send("You were Kicked out".encode())
        clients.remove(kiName) # 從連線中踢掉指定的人
        names.remove(name) # 從 array 移除被踢掉的人
        sendM(f"{name} was kicked out")
        kiName.close() # 關閉連線

def process(client):
    while True:
        try:
            msg  = client.recv(100) # 設定 msg 最大長度100
            Dmesg = msg.decode()
            #print(msg) # b'Alex:Hi'   /kick Alex >>> b'KICK Alex' (/ capital ???)
            if Dmesg.startswith('LEAVE'): # leave (still some bug)
                lName = Dmesg[6:]
                kick(lName)
                print(lName, "left")
            elif names[clients.index(client)] == "admin": # 確認輸入指令者身分
                if Dmesg.startswith("KICK"): # kick
                    kName = Dmesg[5:]
                    kick(kName)
                    print(kName, " was kicked")
                elif Dmesg.startswith('BAN'): # ban
                    bName = Dmesg[4:]
                    kick(bName)
                    with open("BanN.txt", "a") as f: # 儲存 ban list
                        f.write(f"{bName}\n")
                    print(bName, " was banned")
                else:
                    sendM(Dmesg)
            else:
                sendM(Dmesg)
        except socket.error: # Client 斷線處理
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                uName = names[index]
                print(uName, "left")
                sendM(f"{uName} left the chat !")
                names.remove(uName) 
                break

def receive():
    while True:
        client, address = server.accept() # 接受連線
        print(f"Connected with {str(address)}")

        client.send("NM".encode()) # 取得 name
        uName = client.recv(100).decode()

        with open("BanN.txt", "r") as f: # 確認是否被 ban
            banList = f.readlines()
        if uName + '\n' in banList:
            print("user was banned")
            client.send("BAN".encode())
            client.close()
            continue

        if uName == "admin": # admin 連進，要求輸入密碼
            client.send("PSWD".encode())
            password = client.recv(100).decode()
            if password != "pd": # 密碼錯誤，拒絕連線
                client.send("REFUSE".encode())
                client.close()
                continue

        names.append(uName) # 將成功連進的 client 放入 array
        clients.append(client)

        print(f"{uName} joined") # server 訊息
        sendM(f"{uName} joined the chat !") # 通知其他 client
        client.send("Connected to the server, joined the chat successfully".encode()) # certain client 訊息

        thread = threading.Thread(target=process, args=(client,)) # 用 thread 讓多位 client 連線
        thread.start()

print("Server Listening...")
receive()
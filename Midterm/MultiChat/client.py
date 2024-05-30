import os
import json
import socket
import threading

def enter_server(): # 進入 server
    global client
    global nickname
    global password

    os.system('cls||clear')
    with open('serverInfo.json') as f: # 讀入 server info
        serlist = json.load(f)

    print('Servers list : ', end="") # list server info
    for server in serlist:
        print(server, end="  ")
    print()

    serName = input("\nEnter server name : ") # 選擇 server
    nickname = input("Enter your nickname : ")
    if nickname == 'admin':
        password = input("Enter Admin's password : ")
    os.system('cls||clear')
    
    ip = serlist[serName]["ip"] # 存 IP & port
    port = serlist[serName]["port"]

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 宣告 TCP socket
    client.connect((ip, port)) # 連 server

def add_server(): # 新增 server
    os.system('cls||clear')
    nname = input("Enter a name for the server : ") # 輸入 server 資料
    nip = input("Enter the ip address of the server : ")
    nport = int(input("Enter the port number of the server : "))

    with open('serverInfo.json', 'r') as f:
        serList = json.load(f)
    with open('serverInfo.json', 'w') as f: # 將新增的 server 寫入 serverinfo
        serList[nname] = {"ip": nip, "port": nport}
        json.dump(serList, f, indent=4)

while True: # 初始選單，進入 server 後跳出迴圈
    os.system('cls||clear')
    option = input("Welcome to MutiChat ! Choose a service :\n\n(1) Enter server \t (2) Add server\n\n\nEnter an option : ")
    if option == '1':
        enter_server()
        break
    elif option == '2':
        add_server()

stop_thread = False

def receive():
    global stop_thread
    while True:
        if stop_thread: break
        try:
            message = client.recv(100).decode()
            if message == 'NM': # 要求輸入名字
                client.send(nickname.encode())
                next_message = client.recv(100).decode()
                if next_message == 'PSWD': # 如果管理員要密碼
                    client.send(password.encode())
                    if client.recv(100).decode() == 'REFUSE':
                        print("Connection refused due to wrong password")
                        stop_thread = True
                elif next_message == 'BAN': # 拒絕被 ban 的人連線
                    print('Connection refused due to ban')
                    client.close()
                    stop_thread = True
            else:
                print(message)
        except socket.error:
            print('Error occured while connecting')
            client.close()
            break

def write():
    while True:
        if stop_thread: break
        message = f'{nickname}: {input("")}' # 取得訊息
        nml = len(nickname) + 2 # 為去掉 admin:
        if message[nml:].startswith('/'):
            if nickname == 'admin':
                if message[nml:].startswith('/kick'):
                    client.send(f'KICK {message[nml + 6:]}'.encode()) # admin: /kick Alex
                elif message[nml:].startswith('/ban'):
                    client.send(f'BAN {message[nml + 5:]}'.encode()) # admin: /ban Alex
            elif nickname != '':
                if message[nml:].startswith('/leave'):
                    client.send(f'LEAVE {nickname}'.encode()) # /leave
            else:
                print("Command refused ")
        else:
            client.send(message.encode())


receive_thread = threading.Thread(target=receive) # 用 thread 讓多位 client 連線
write_thread = threading.Thread(target=write)
receive_thread.start()
write_thread.start()
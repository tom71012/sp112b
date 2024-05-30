import sys
import socket
import threading

SMAX = 80
fd = None # 檔案描述子!?

def receiver(): # 接收訊息的函式
    global fd
    while True:
        msg = fd.recv(SMAX) # 設定 msg 最大長度80
        if len(msg) <= 0: break # 沒打字 then break
        #print(msg) # b'index'
        #print(len(msg)) # 5
        print("receive: ", msg.decode())

def main():
    global fd
    sfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 宣告一 TCP(SOCK_STREAM) 的 scoket 變數
    saddr = ('', 8000) # 存 IP & Port=8000
    msg = ""

    if len(sys.argv) == 1:  # Server，執行未傳入參數時，sys.argv=1
        print("Running server now!")
        sfd.bind(saddr) # 把 Socket 綁定到後來傳入的 IP & Port
        sfd.listen(1) # 最多 Client=1
        cfd, raddr = sfd.accept() # 等待 Client 連接訊號，接受連線
        print("Accept : cfd =", cfd, "client address =", raddr[0])
        fd = cfd
    else:  # Client
        print("Connecting to server!")
        saddr = (sys.argv[1], 8000) # 傳入的 IP 放入變數
        sfd.connect(saddr) 
        fd = sfd
        print("Connect : sfd =", sfd, "server address =", saddr[0]) # 印出連線資訊

    thread1 = threading.Thread(target=receiver) # 宣告一 thread 變數，並指定reciver函式
    thread1.start()

    while True: # 等input，送出訊息
        msg = input()
        fd.send(msg.encode())

if __name__ == '__main__':
    main()
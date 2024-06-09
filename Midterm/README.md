## 聲明
程式為原創，僅參考老師上課教材及下方網址

## 發想
原來想將老師的程式寫成Python，但Python不像C語言一樣底層，所以重現一些如fork的東西很麻煩，因此參考研究老師使用 thread 跟 TCP 的 IP chat 程式進行延伸作為期末專案

## 操作
執行server.py

![image](https://github.com/Jung217/sp111b/blob/main/asset/00%20exeServer.png)

執行client.py，選擇進入或新增

![image](https://github.com/Jung217/sp111b/blob/main/asset/01%20exeClient.png)

進入後選擇伺服器，輸入名稱

![image](https://github.com/Jung217/sp111b/blob/main/asset/01%20exeClient1.png)

TTT加入

![image](https://github.com/Jung217/sp111b/blob/main/asset/02%20joinChat.png)

Alex加入

![image](https://github.com/Jung217/sp111b/blob/main/asset/02%20joinChat1.png)

聊天...

![image](https://github.com/Jung217/sp111b/blob/main/asset/03%20chatting.png)

admin加入，要求輸入密碼

![image](https://github.com/Jung217/sp111b/blob/main/asset/04%20adminJoin.png)

admin聊天

![image](https://github.com/Jung217/sp111b/blob/main/asset/05%20adminSayHi.png)

admin kick Alex

![image](https://github.com/Jung217/sp111b/blob/main/asset/06%20adminKick.png)

admin ban TTT

![image](https://github.com/Jung217/sp111b/blob/main/asset/07%20adminBan.png)

## 備註

* 指令:
  * adimn:
    * /kick Alex
    * /ban Alex 
  * 其他人:
    * /leave

PS. leave還有一些bug

## 參考
[Python_Socket](https://ithelp.ithome.com.tw/articles/10205819)

[Python sys.argv 用法](https://shengyu7697.github.io/python-sys-argv/)

[threading-基于线程的并行](https://docs.python.org/zh-tw/3/library/threading.html)

[Python 多執行緒 threading 模組平行化程式設計](https://blog.gtwang.org/programming/python-threading-multithreaded-programming-tutorial/)

[TCP/IP 協定與 Internet 網路：TCP Socket 程式介面](http://www.tsnien.idv.tw/Internet_WebBook/chap8/8-5%20Socket%20%E5%BA%AB%E5%AD%98%E5%87%BD%E6%95%B8.html)

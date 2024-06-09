## 聲明
程式為參考[Jung217](https://github.com/Jung217)，並參考老師上課教材及下方網址

## 發想
本來想將老師的程式寫成Python，但Python不像C語言一樣底層，所以重現一些如fork的東西很麻煩，因此參考研究老師使用 thread 跟 TCP 的 IP chat 程式進行延伸作為期中專案

## 操作
執行server.py

![image](https://hackmd.io/_uploads/HJIVYTfrR.png)

執行client.py，選擇進入或新增

![image](https://hackmd.io/_uploads/S1brKTMrC.png)

進入後選擇伺服器，輸入名稱

![image](https://hackmd.io/_uploads/Byo1opzHA.png)

TTT加入

![image](https://hackmd.io/_uploads/rJnxj6Mr0.png)

Alex加入

![image](https://hackmd.io/_uploads/Hkjl36zHR.png)

聊天...

![image](https://hackmd.io/_uploads/SyUZiTzBC.png)

admin加入，要求輸入密碼

![image](https://hackmd.io/_uploads/r1Cbs6zH0.png)

admin聊天

![image](https://hackmd.io/_uploads/BkmMspfS0.png)

admin kick Alex

![image](https://hackmd.io/_uploads/rkPGoaMrC.png)

admin ban TTT

![image](https://hackmd.io/_uploads/HkhfjaMHC.png)

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

[Jung217's Midterm project](https://github.com/Jung217/sp111b/tree/main/Midterm%20project)

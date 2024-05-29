# 多執行緒的提款與存款程式(參考ChatGPT)

此專案包含兩個版本的多執行緒提款與存款程式：一個沒有使用 mutex，另一個使用 mutex。這兩個版本展示了 race condition 的影響及其解決方法。

## 程式描述

### 版本 1：沒有使用 Mutex
這個版本中，我們沒有使用互斥鎖來保護帳戶餘額的存取。因此，多個執行緒同時訪問和修改 `balance` 時，會發生 race condition。

### 版本 2：使用 Mutex
在這個版本中，我們使用 `threading.Lock` 來確保每次只有一個執行緒可以訪問和修改 `balance`，從而避免 race condition。

## 執行結果

### 沒有使用 Mutex 的版本

#### 程式碼
```
import threading

# 初始帳戶餘額
balance = 1000

def deposit(amount):
    global balance
    for _ in range(100000):
        balance += amount

def withdraw(amount):
    global balance
    for _ in range(100000):
        balance -= amount

# 建立存款與提款的執行緒
deposit_thread = threading.Thread(target=deposit, args=(1,))
withdraw_thread = threading.Thread(target=withdraw, args=(1,))

# 開始執行緒
deposit_thread.start()
withdraw_thread.start()

# 等待執行緒結束
deposit_thread.join()
withdraw_thread.join()

# 打印最終的帳戶餘額
print(f"最終帳戶餘額: {balance}")
```
#### 執行結果
最終帳戶餘額: 1000 (此結果可能因每次執行而不同)

#### 意義
由於 race condition，最終帳戶餘額可能與預期不符。這是因為多個執行緒同時訪問和修改 balance，導致數據不一致。

### 使用 Mutex 的版本
```
# 初始帳戶餘額
balance = 1000
balance_lock = threading.Lock()

def deposit(amount):
    global balance
    for _ in range(100000):
        with balance_lock:
            balance += amount

def withdraw(amount):
    global balance
    for _ in range(100000):
        with balance_lock:
            balance -= amount

# 建立存款與提款的執行緒
deposit_thread = threading.Thread(target=deposit, args=(1,))
withdraw_thread = threading.Thread(target=withdraw, args=(1,))

# 開始執行緒
deposit_thread.start()
withdraw_thread.start()

# 等待執行緒結束
deposit_thread.join()
withdraw_thread.join()

# 打印最終的帳戶餘額
print(f"最終帳戶餘額: {balance}")
```
#### 執行結果
最終帳戶餘額: 1000

#### 意義
使用 mutex 確保了每次只有一個執行緒可以修改 balance，從而避免了 race condition，保證最終帳戶餘額的正確性。

## 問題 1 詳細描述
a. 使用者應紀錄自己原本帳戶有多少錢，每次存提多少錢，還剩下多少錢
在程式中，我們初始化帳戶餘額為 1000。每次存款和提款的金額均為 1，重複 100000 次。

b. 每次存提款請求給銀行之後，銀行應傳回還剩下多少錢
在每次存提款操作中，我們沒有即時返回剩餘金額，只是在所有操作完成後打印最終餘額。

c. 使用者應檢核『存款＋-存提款數量＝剩下金額』是否正確，如果有錯立刻報錯
在沒有使用 mutex 的版本中，由於 race condition，最終餘額可能不正確。使用 mutex 的版本則保證了最終餘額的正確性。

## 結論
這兩個版本展示了多執行緒操作中 race condition 的影響及其解決方法。使用 mutex 能夠有效避免 race condition，確保資料的一致性和正確性。


這樣的排版應該更清晰地展示了各個部分的內容和結果，並詳細說明了問題 1 的要求。使用者可以依據這些說明來理解 race condition 的影響以及使用 mutex 的重要性。



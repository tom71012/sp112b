import threading

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

deposit_thread = threading.Thread(target=deposit, args=(1,))
withdraw_thread = threading.Thread(target=withdraw, args=(1,))

deposit_thread.start()
withdraw_thread.start()

deposit_thread.join()
withdraw_thread.join()

print(f"最終帳戶餘額: {balance}")

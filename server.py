import socket
import threading

# تعريف حسابات البنك المبدئية مع أرصدتها
accounts = {
    '123456': {'pin': '1234', 'balance': 1000.0},
    '654321': {'pin': '4321', 'balance': 1500.0}
}


# تابع للتعامل مع كل عميل متصل
def handle_client(client_socket):
    try:
        # استقبال بيانات الحساب ورمز PIN من العميل
        client_socket.send(b'Enter account number: ')
        account_number = client_socket.recv(1024).decode().strip()

        client_socket.send(b'Enter PIN: ')
        pin = client_socket.recv(1024).decode().strip()

        # التحقق من صحة بيانات الحساب
        if account_number in accounts and accounts[account_number]['pin'] == pin:
            client_socket.send(b'Authenticated\n')
            while True:
                # إرسال الخيارات المتاحة للعميل
                client_socket.send(b'Choose operation: 1. Check Balance 2. Deposit 3. Withdraw 4. Exit\n')
                operation = client_socket.recv(1024).decode().strip()

                if operation == '1':
                    # تحقق من الرصيد
                    balance = accounts[account_number]['balance']
                    client_socket.send(f'Your balance is {balance}\n'.encode())

                elif operation == '2':
                    # إيداع المال
                    client_socket.send(b'Enter amount to deposit: ')
                    amount = float(client_socket.recv(1024).decode().strip())
                    accounts[account_number]['balance'] += amount
                    client_socket.send(b'Deposit successful\n')

                elif operation == '3':
                    # سحب المال
                    client_socket.send(b'Enter amount to withdraw: ')
                    amount = float(client_socket.recv(1024).decode().strip())
                    if accounts[account_number]['balance'] >= amount:
                        accounts[account_number]['balance'] -= amount
                        client_socket.send(b'Withdrawal successful\n')
                    else:
                        client_socket.send(b'Insufficient balance\n')

                elif operation == '4':
                    # إنهاء الجلسة
                    balance = accounts[account_number]['balance']
                    client_socket.send(f'Your final balance is {balance}\n'.encode())
                    break
                else:
                    client_socket.send(b'Invalid operation\n')

        else:
            client_socket.send(b'Authentication failed\n')
    finally:
        client_socket.close()


# تابع بدء الخادم
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(5)
    print("Server started and listening on port 9999")

    while True:
        client_socket, addr = server.accept()
        print(f'Accepted connection from {addr}')
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    start_server()

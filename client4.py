import socket

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 9999))

    while True:
        data = client.recv(1024)
        print(data.decode(), end='')

        if 'Your final balance is' in data.decode():
            client.close()
            break

        user_input = input()
        client.send(user_input.encode())

    client.close()

if __name__ == "__main__":
    start_client()

import socket
import os

def send_command(client, cmd):
    """Отправка текстовой команды"""
    client.send(f"COMMAND {cmd}".encode('utf-8'))
    response = client.recv(1024).decode('utf-8')
    print(f"Server response: {response}")

def send_file(client, filename):
    """Передача файла"""
    if not os.path.exists(filename):
        print("File does not exist")
        return

    file_size = os.path.getsize(filename)
    client.send(f"FILE {os.path.basename(filename)}".encode('utf-8'))
    client.send(str(file_size).encode('utf-8'))

    with open(filename, "rb") as f:
        while (chunk := f.read(1024)):
            client.send(chunk)
    
    response = client.recv(1024).decode('utf-8')
    print(f"Server response: {response}")

def start_client():
    """Запуск клиента"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(('localhost', 12345))
        print(client.recv(1024).decode('utf-8'))  # Запрос логина
        login = input("Enter login: ")
        client.send(login.encode('utf-8'))

        print(client.recv(1024).decode('utf-8'))  # Запрос пароля
        password = input("Enter password: ")
        client.send(password.encode('utf-8'))

        auth_response = client.recv(1024).decode('utf-8')
        print(auth_response)
        if "failed" in auth_response:
            print("Exiting...")
            return

        # Основной цикл
        while True:
            print("\nOptions:")
            print("1. Send command (e.g., 'hello' or 'status')")
            print("2. Send file")
            print("3. Exit")

            choice = input("Enter your choice: ")
            if choice == "1":
                cmd = input("Enter command: ")
                send_command(client, cmd)
            elif choice == "2":
                filename = input("Enter filename to send: ")
                send_file(client, filename)
            elif choice == "3":
                print("Exiting...")
                break
            else:
                print("Invalid choice")
    except Exception as e:
        print(f"Client error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    start_client()

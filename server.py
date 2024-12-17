import socket
import threading
import os

# Список пользователей с логинами и паролями
USERS = {"Alex": "A1", "Sara": "S2","Volodya": "V3", "Olesya": "O4"}

def authenticate(client_socket):
    """Аутентификация"""
    client_socket.send("Login: ".encode('utf-8'))
    login = client_socket.recv(1024).decode('utf-8')
    client_socket.send("Password: ".encode('utf-8'))
    password = client_socket.recv(1024).decode('utf-8')
    
    if USERS.get(login) == password:
        client_socket.send("Authentication successful".encode('utf-8'))
        return True
    else:
        client_socket.send("Authentication failed".encode('utf-8'))
        return False

def handle_client(client_socket):
    """Обработка запросов"""
    try:
        if not authenticate(client_socket):
            client_socket.close()
            return

        while True:
            protocol = client_socket.recv(1024).decode('utf-8')
            if not protocol:
                break

            if protocol.startswith("COMMAND"):
                handle_command(client_socket, protocol)
            elif protocol.startswith("FILE"):
                handle_file_transfer(client_socket, protocol)
            else:
                client_socket.send("Unknown protocol".encode('utf-8'))
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        print("Connection closed")
        client_socket.close()

def handle_command(client_socket, command):
    """Обработка текстовых команд"""
    try:
        _, cmd = command.split(" ", 1)
        if cmd.lower() == "hello":
            response = "Hello, client!"
        elif cmd.lower() == "status":
            response = "Server is running."
        else:
            response = f"Unknown command: {cmd}"
        client_socket.send(response.encode('utf-8'))
    except ValueError:
        client_socket.send("Invalid command format".encode('utf-8'))

def handle_file_transfer(client_socket, protocol):
    """Обработка передачи файлов"""
    try:
        _, filename = protocol.split(" ", 1)
        filename = filename.strip()

        # Ожидаем длину файла
        file_size = int(client_socket.recv(1024).decode('utf-8'))

        # Принимаем файл
        with open(f"received_{filename}", "wb") as f:
            received = 0
            while received < file_size:
                data = client_socket.recv(1024)
                f.write(data)
                received += len(data)

        client_socket.send(f"File {filename} received successfully".encode('utf-8'))
    except Exception as e:
        client_socket.send(f"Error receiving file: {e}".encode('utf-8'))

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind(('localhost', 12345))
        server.listen(5)
        print("Server started, waiting for connections...")
        
        while True:
            client_socket, addr = server.accept()
            print(f"Connection from {addr}")
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()
    except Exception as e:
        print(f"Server error: {e}")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()

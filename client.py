import socket
import sys
import threading
import ipaddress
import os

thread_message = True


def send_message(server):
    while thread_message:
        message = input()

        if not message.strip():
            continue

        try:
            server.send(message.encode())
        except socket.error:
            sys.exit()


# entao a primeira msg q eu recebo seria o menu?dps vou pra thread de enviar
def receive_message(server):
    while True:
        message = server.recv(1024).decode()
        splitted_message = message.split(":")

        message = ":".join(splitted_message[1:])
        prefix = splitted_message[0]

        print(message)

        if prefix == "leave":
            os._exit(0)

        elif prefix == "menu":
            send_message_thread = threading.Thread(
                target=send_message, args=(client_socket,))
            send_message_thread.start()


def is_valid_ip(ip):
    if ip.lower() == "localhost":
        return True
    try:
        socket.inet_pton(socket.AF_INET, ip)
        return True
    except socket.error:
        return False


def is_valid_port(port):
    try:
        port = int(port)
        return 1 <= port <= 65535
    except ValueError:
        return False


while True:
    server_ip = input("Digite o IP do servidor: ")
    if is_valid_ip(server_ip):
        break
    else:
        print("IP inválido. Certifique-se de que está no formato correto (por exemplo, '127.0.0.1').")

while True:
    server_port = int(input("Digite a porta do servidor: "))
    if is_valid_port(server_port):
        break
    else:
        print("Porta inválida. Certifique-se de que é um número inteiro no intervalo válido (1-65535).")


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((server_ip, server_port))
    print("conexao com sucesso")
except socket.error:
    print("Não foi possível se conectar ao servidor")
    sys.exit()

receive_message_thread = threading.Thread(
    target=receive_message, args=(client_socket,))
receive_message_thread.start()
#import pika
import sys
import os
import socket


def get_public_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(("8.8.8.8", 80))
    public_ip = sock.getsockname()[0]
    sock.close()

    return public_ip


def lamp_callback(ch, method, properties, body):
    print(f"Nível de luminosidade: {body}")


def air_conditioner_callback(ch, method, properties, body):
    pass



class Device:
    def __init__(self, device_name,device_queue ):
        self.device_name = device_name
        
class Home_assistant:
    def __init__(self, host, port,socket):
        self.host = host
        self.port = port
        self.devices = {
            1: "Lâmpada",
            2: "Ar condicionado",
            3: "Bomba D'água"
        }
        self.server_socket=socket
        try:
            server_socket.bind((host, port))
        except socket.error:
            print("Não foi possível estabelecer conexão com o socket. Encerrando home assistant.")
            sys.exit()



    def start(self):
        #self.handle_devices()
        self.connect_to_client()

    def handle_devices(self):
        pika.BaseConnection()

        connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.exchange_declare(exchange='smart_lamp', exchange_type='fanout')
        channel.exchange_declare(
        exchange='air_conditioner', exchange_type='fanout')

        channel.queue_declare(queue='lamp_queue', exclusive=True)
        channel.queue_declare(queue='air_conditioner_queue', exclusive=True)

        channel.queue_bind(exchange='smart_lamp', queue='lamp_queue')
        channel.queue_bind(exchange='air_conditioner',
                       queue='air_conditioner_queue')

        print(' [*] Waiting for logs. To exit press CTRL+C')

        channel.basic_consume(queue='lamp_queue',
                          on_message_callback=lamp_callback, auto_ack=True)
        channel.basic_consume(queue='air_conditioner_queue',
                          on_message_callback=air_conditioner_callback, auto_ack=True)
        
    def connect_to_client(self):
        SERVER_IP=get_public_ip()
        SERVER_PORT=self.port
        server_socket.listen(1)
        print(f"Home assistant iniciado no endereço {SERVER_IP}:{SERVER_PORT}")
        client_socket, client_address = server_socket.accept()
        print("conexao com sucesso")
        self.start_communication(client_socket)

    def start_communication(self, client_socket):
        while True:
            device_options = "\n".join([f"{device_num} - {device_name}" for device_num, device_name in self.devices.items()])
            menu = f"menu:Escolha um dispositivo:\n{device_options}\n0 - Sair\n"
            client_socket.send(menu.encode())
            choice = client_socket.recv(1024).decode()

            if choice == '0':
                client_socket.send("leave:Saindo...".encode())
                client_socket.close()
                break

            try:
                device_num = int(choice)
                if device_num in self.devices:
                    client_socket.send(f"ok:Você escolheu {self.devices[device_num]}\n".encode())
                    # Lógica para lidar com o dispositivo escolhido
                    if device_num == 1:
                        # Lógica para Lâmpada
                        pass
                    elif device_num == 2:
                        # Lógica para Ar condicionado
                        pass
                    elif device_num == 3:
                        # Lógica para Bomba D'água
                        pass
                else:
                    client_socket.send("ok:Escolha inválida. Tente novamente.\n".encode())
            except ValueError:
                client_socket.send("ok:Escolha inválida. Tente novamente.\n".encode())






if __name__ == '__main__':
    try:
        SERVER_IP=get_public_ip()
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        home_assistant = Home_assistant(SERVER_IP, 12345,server_socket)
        home_assistant.start()

    except KeyboardInterrupt:
        print('\nDispositivo encerrado.')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

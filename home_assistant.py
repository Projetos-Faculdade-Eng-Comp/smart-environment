import pika
import sys
import os
import socket
import threading
import time

global LAMP 
global AIR
LAMP = False
AIR = False


def get_public_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(("8.8.8.8", 80))
    public_ip = sock.getsockname()[0]
    sock.close()

    return public_ip


class Device:
    def __init__(self, device_name,device_queue ):
        self.device_name = device_name
        
class Home_assistant:
    def __init__(self, host, port,socket):
        self.host = host
        self.port = port
        self.client_socket = None
        self.devices = {
            1: "Lâmpada",
            2: "Ar condicionado",
            3: "Bomba D'água"
        }
        self.server_socket=socket

        # Lista para armazenar mensagens
        self.messagesLamp = []
        self.messagesAir = []

        try:
            server_socket.bind((host, port))
        except socket.error:
            print("Não foi possível estabelecer conexão com o socket. Encerrando home assistant.")
            sys.exit()


    def start(self):
        self.connect_to_client()

        lamp_thread = threading.Thread(target=self.handle_lamp)
        air_cond_thread = threading.Thread(target=self.handle_air_conditioner)
        send_messages_devices_thread = threading.Thread(target=self.send_messages_devices)
        start_communication_thread = threading.Thread(target=self.start_communication)

        lamp_thread.start()
        air_cond_thread.start()
        send_messages_devices_thread.start()
        start_communication_thread.start()


    def lamp_callback(self, ch, method, properties, body):
        self.messagesLamp.append(body)



    def air_conditioner_callback(self,ch, method, properties, body):
        self.messagesAir.append(body)


    def send_messages_devices(self):
        while True:
            if LAMP:
                if self.messagesLamp:
                    message = self.messagesLamp.pop(0)
                    combined_message = b"ok:" + message
                    self.client_socket.send(combined_message)
                    time.sleep(1)
                else:
                    pass

            if AIR:
                if self.messagesAir:
                    message = self.messagesAir.pop(0)
                    combined_message = b"ok:" + message
                    self.client_socket.send(combined_message)
                    time.sleep(1)
                else:
                    pass

            
       

    def handle_lamp(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel_lamp = connection.channel()
        channel_lamp.queue_declare(queue='lamp_queue', exclusive=True)
        channel_lamp.queue_bind(exchange='smart_lamp', queue='lamp_queue')
        channel_lamp.basic_consume(queue='lamp_queue', on_message_callback=self.lamp_callback, auto_ack=True)
        channel_lamp.start_consuming()

    def handle_air_conditioner(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel_air_cond = connection.channel()
        channel_air_cond.queue_declare(queue='air_conditioner_queue', exclusive=True)
        channel_air_cond.queue_bind(exchange='air_conditioner', queue='air_conditioner_queue')
        channel_air_cond.basic_consume(queue='air_conditioner_queue', on_message_callback=self.air_conditioner_callback, auto_ack=True)
        channel_air_cond.start_consuming()

    def connect_to_client(self):
        SERVER_IP=get_public_ip()
        SERVER_PORT=self.port
        server_socket.listen(1)
        print(f"Home assistant iniciado no endereço {SERVER_IP}:{SERVER_PORT}")
        self.client_socket, client_address = server_socket.accept()
        print("conexao com sucesso")

    def start_communication(self):

        
        while True:
            device_options = "\n".join([f"{device_num} - {device_name}" for device_num, device_name in self.devices.items()])
            menu = f"menu:\nEscolha um dispositivo:\n{device_options}\n0 - Sair\n"
            self.client_socket.send(menu.encode())
            choice = self.client_socket.recv(1024).decode()

            if choice == '0':
                self.client_socket.send("leave:Saindo...".encode())
                self.client_socket.close()
                break

            try:
                
                device_num = int(choice)
                if device_num in self.devices:
                    self.client_socket.send(f"ok:Você escolheu {self.devices[device_num]}\n Digite 0 para sair\n".encode())
                    # Lógica para lidar com o dispositivo escolhido
                    if device_num == 1:
                        # Lógica para Lâmpada
                        # Tem essa possibilidade de enviar tudo que tiver de uma vez, ou só mandar uma quantidade fixa
                        #self.client_socket.send('\n'.join(self.messagesLamp).encode()) 
                        #self.messagesLamp.clear()
                        global LAMP
                        LAMP = True
                        while LAMP: 
                            stop = self.client_socket.recv(1024).decode()
                            if stop == "0":
                                LAMP = False

                        
                    elif device_num == 2:
                        # Lógica para Ar condicionado
                        global AIR
                        AIR = True
                        while AIR: 
                            stop = self.client_socket.recv(1024).decode()
                            if stop == "0":
                                AIR = False
                    elif device_num == 3:
                        # Lógica para Bomba D'água
                        pass
                else:
                    self.client_socket.send("ok:Escolha inválida. Tente novamente.\n".encode())
            except ValueError:
                self.client_socket.send("ok:Escolha inválida. Tente novamente.\n".encode())






if __name__ == '__main__':
    try:
        SERVER_IP=get_public_ip()
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        home_assistant = Home_assistant(SERVER_IP, 12345, server_socket)
        home_assistant.start()

    except KeyboardInterrupt:
        print('\nDispositivo encerrado.')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

import pika
import sys
import os
import socket
import threading
import time
import grpc
import actuators_service_pb2
import actuators_service_pb2_grpc
import air_conditioner_service_pb2
import air_conditioner_service_pb2_grpc

global LAMP
global AIR
global WATERPUMP
LAMP = False
AIR = False
WATERPUMP = False

def get_public_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(("8.8.8.8", 80))
    public_ip = sock.getsockname()[0]
    sock.close()
    return public_ip

class HomeAssistant:
    def __init__(self, host, port, socket):
        self.host = host
        self.port = port
        self.client_socket = None
        self.devices = {
            1: "Lâmpada",
            2: "Ar condicionado",
            3: "Bomba D'água"
        }
        self.server_socket = socket

    def setup_server_socket(self):
        try:
            self.server_socket.bind((self.host, self.port))
        except socket.error:
            print("Não foi possível estabelecer conexão com o socket. Encerrando home assistant.")
            sys.exit()


        # Lista para armazenar mensagens
        self.messagesLamp = []
        self.messagesAir = []
        self.messagesWaterPump = []

    # Para a lâmpada
    lamp_channel = grpc.insecure_channel('localhost:50051')  # Use o endereço correto do servidor gRPC da lâmpada
    lamp_stub = actuators_service_pb2_grpc.ActuatorsServiceStub(lamp_channel)

    # Para o ar condicionado
    air_channel = grpc.insecure_channel('localhost:50052')  # Use o endereço correto do servidor gRPC do ar condicionado
    air_stub = air_conditioner_service_pb2_grpc.AirConditionerServiceStub(air_channel)

    # Para a bomba de água
    water_pump_channel = grpc.insecure_channel('localhost:50053')  # Use o endereço correto do servidor gRPC da Bomba de água
    water_pump_stub = actuators_service_pb2_grpc.ActuatorsServiceStub(water_pump_channel)

    def start(self):
        self.connect_to_client()

        lamp_thread = threading.Thread(target=self.handle_lamp)
        air_cond_thread = threading.Thread(target=self.handle_air_conditioner)
        water_pump_thread = threading.Thread(target=self.handle_water_pump)
        send_messages_devices_thread = threading.Thread(target=self.send_messages_devices)
        start_communication_thread = threading.Thread(target=self.start_communication)

        lamp_thread.start()
        air_cond_thread.start()
        water_pump_thread.start()
        send_messages_devices_thread.start()
        start_communication_thread.start()

    def lamp_callback(self, ch, method, properties, body):
        if len(self.messagesLamp) < 10:
            self.messagesLamp.append(body)
        else:
            self.messagesLamp.clear()

    def air_conditioner_callback(self, ch, method, properties, body):
        if len(self.messagesAir) < 10:
            self.messagesAir.append(body)
        else:
            self.messagesAir.clear()
            
    def water_pump_callback(self, ch, method, properties, body):
        if len(self.messagesWaterPump) < 10:
            self.messagesWaterPump.append(body)
        else:
            self.messagesWaterPump.clear()
            
    def send_messages_devices(self):
        while True:
            if LAMP:
                if self.messagesLamp:
                    message = self.messagesLamp.pop()
                    combined_message = b"ok:" + message
                    self.client_socket.send(combined_message)
                    time.sleep(1)
                else:
                    pass

            if AIR:
                if self.messagesAir:
                    message = self.messagesAir.pop()
                    combined_message = b"ok:" + message
                    self.client_socket.send(combined_message)
                    time.sleep(1)
                else:
                    pass
                
            if WATERPUMP:
                if self.messagesWaterPump:
                    message = self.messagesWaterPump.pop(0)
                    combined_message = b"ok:" + message
                    self.client_socket.send(combined_message)
                    time.sleep(1)
                else:
                    pass

    def handle_lamp(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel_lamp = connection.channel()
        channel_lamp.exchange_declare(exchange='devices', exchange_type='direct')
        channel_lamp.queue_declare(queue='lamp_queue', exclusive=True)
        channel_lamp.queue_bind(exchange='devices', queue='lamp_queue', routing_key='lamp')
        channel_lamp.basic_consume(queue='lamp_queue', on_message_callback=self.lamp_callback, auto_ack=True)
        channel_lamp.start_consuming()

    def handle_air_conditioner(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel_air_cond = connection.channel()
        channel_air_cond.exchange_declare(exchange='devices', exchange_type='direct')
        channel_air_cond.queue_declare(queue='air_conditioner_queue', exclusive=True)
        channel_air_cond.queue_bind(exchange='devices', queue='air_conditioner_queue', routing_key='air_cond')
        channel_air_cond.basic_consume(queue='air_conditioner_queue', on_message_callback=self.air_conditioner_callback, auto_ack=True)
        channel_air_cond.start_consuming()

    def handle_water_pump(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel_water_pump = connection.channel()
        channel_water_pump.exchange_declare(exchange='devices', exchange_type='direct')
        channel_water_pump.queue_declare(queue='water_pump_queue', exclusive=True)
        channel_water_pump.queue_bind(exchange='devices', queue='water_pump_queue', routing_key='water_pump')
        channel_water_pump.basic_consume(queue='water_pump_queue', on_message_callback=self.water_pump_callback, auto_ack=True)
        channel_water_pump.start_consuming()
        
    def connect_to_client(self):
        SERVER_IP = get_public_ip()
        SERVER_PORT = self.port
        server_socket.listen(1)
        print(f"Home assistant iniciado no endereço {SERVER_IP}:{SERVER_PORT}")
        self.client_socket, client_address = server_socket.accept()
        print("Conexão bem-sucedida")

    def start_communication(self):
        while True:
            device_options = "\n".join([f"{device_num} - {device_name}" for device_num, device_name in self.devices.items()])
            menu = f"menu:\nEscolha um dispositivo:\n{device_options}\n0 - Sair\n"
            self.client_socket.send(menu.encode())
            choice = self.client_socket.recv(1024).decode()

            if choice == '0':
                self.client_socket.send("leave:Saindo...".encode())
                self.client_socket.close()
                self.client_socket = None
                print("Cliente desconectado. Esperando novas conexões...")
                while not self.client_socket:
                    self.client_socket, client_address = self.server_socket.accept()
                    print("Nova conexão bem-sucedida")

            try:
                device_num = int(choice)
                if device_num in self.devices:
                    self.client_socket.send(f"ok:Você escolheu {self.devices[device_num]}\n Digite 0 para sair\n".encode())
                    # Lógica para lidar com o dispositivo escolhido
                    if device_num == 1:
                        while True:
                            menu1 = "\ok:\n0 - Voltar\n1 - Ligar\n2 - Desligar\n3 - show luminosity"
                            self.client_socket.send(menu1.encode())
                            choice = int(self.client_socket.recv(1024).decode())
                            if choice == 1:
                                ligar_request = actuators_service_pb2.TurnOnRequest()
                                response = self.lamp_stub.turnOn(ligar_request)
                                self.client_socket.send(f"ok:{response.message}".encode())
                                
                            elif choice == 2:
                                desligar_request = actuators_service_pb2.TurnOffRequest()
                                response = self.lamp_stub.turnOff(desligar_request)
                                self.client_socket.send(f"ok:{response.message}".encode())

                            elif choice == 3: 
                                # Lógica para Lâmpada
                                global LAMP
                                LAMP = True
                                while LAMP:
                                    stop = self.client_socket.recv(1024).decode()
                                    if stop == "0":
                                        LAMP = False
                            elif choice == 0:
                                break

                            else: 
                                self.client_socket.send("ok:Escolha inválida. Tente novamente.\n".encode())

                    elif device_num == 2:
                        while True:
                            menu1 = "\ok:\n0 - Voltar\n1 - Ligar\n2 - Desligar\n3 - Aumentar temperatura\n4 - Diminuir temperatura\n5 - show temperature"
                            self.client_socket.send(menu1.encode())
                            choice = int(self.client_socket.recv(1024).decode())
                            if choice == 1:
                                response = self.air_stub.turnOnAirConditioner(air_conditioner_service_pb2.AirConditionerRequest())
                                self.client_socket.send(f"ok:{response.message}".encode())
                            elif choice == 2:
                                response = self.air_stub.turnOffAirConditioner(air_conditioner_service_pb2.AirConditionerRequest())
                                self.client_socket.send(f"ok:{response.message}".encode())
                            elif choice == 3:
                                response = self.air_stub.aumentarTemp(air_conditioner_service_pb2.AirConditionerRequest())
                                self.client_socket.send(f"ok:{response.message}".encode())

                            elif choice == 4:
                                response = self.air_stub.diminuirTemp(air_conditioner_service_pb2.AirConditionerRequest())
                                self.client_socket.send(f"ok:{response.message}".encode())


                            elif choice == 5: 
                                # Lógica para Ar condicionado
                                global AIR
                                AIR = True
                                while AIR:
                                    stop = self.client_socket.recv(1024).decode()
                                    if stop == "0":
                                        AIR = False
                            elif choice == 0:
                                break

                            else: 
                                self.client_socket.send("ok:Escolha inválida. Tente novamente.\n".encode())
                
                    elif device_num == 3:
                        # Lógica para Bomba D'água
                        while True:
                            menu1 = "\ok:\n0 - Voltar\n1 - Ligar\n2 - Desligar\n3 - show soil moisture"
                            self.client_socket.send(menu1.encode())
                            choice = int(self.client_socket.recv(1024).decode())
                            if choice == 1:
                                turn_on_request = actuators_service_pb2.TurnOnRequest()
                                response = self.water_pump_stub.turnOn(turn_on_request)
                                self.client_socket.send(f"ok:{response.message}".encode())
                                
                            elif choice == 2:
                                turn_off_request = actuators_service_pb2.TurnOffRequest()
                                response = self.water_pump_stub.turnOff(turn_off_request)
                                self.client_socket.send(f"ok:{response.message}".encode())

                            elif choice == 3: 
                                # Lógica para Bomba de água
                                global WATERPUMP
                                WATERPUMP = True
                                while WATERPUMP:
                                    stop = self.client_socket.recv(1024).decode()
                                    if stop == "0":
                                        WATERPUMP = False
                            elif choice == 0:
                                break

                            else: 
                                self.client_socket.send("ok:Escolha inválida. Tente novamente.\n".encode())
                else:
                    self.client_socket.send("ok:Escolha inválida. Tente novamente.\n".encode())
            except ValueError:
                self.client_socket.send("ok:Escolha inválida. Tente novamente.\n".encode())

if __name__ == '__main__':
    try:
        SERVER_IP = get_public_ip()
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        home_assistant = HomeAssistant(SERVER_IP, 12345, server_socket)
        home_assistant.setup_server_socket()
        home_assistant.start()

    except KeyboardInterrupt:
        print('\nDispositivo encerrado.')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

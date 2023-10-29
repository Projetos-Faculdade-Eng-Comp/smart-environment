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
        self.connected_devices = []
        self.server_socket=socket
        try:
            server_socket.bind((host, port))
        except socket.error:
            print("Não foi possível estabelecer conexão com o socket. Encerrando home assistant.")
            sys.exit()



    def start(self):
        #self.handle_devices()
        self.connect_to_client()
        #self.start_communication()

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
        #criar um vetor de devices so com os nomes deles
    def connect_to_client(self):
        SERVER_IP=get_public_ip()
        SERVER_PORT=self.port
        server_socket.listen(1)
        print(f"Home assistant iniciado no endereço {SERVER_IP}:{SERVER_PORT}")
        client_socket, client_address = server_socket.accept()
        print("conexao com sucesso")

    def start_communication(self):
        while True:
            print("Escolha o dispositivo:")
            for idx, device in enumerate(self.connected_devices):
                print(f"{idx + 1}. {device.device_type}")

            print(f"{len(self.connected_devices) + 1}. /VOLTAR")
            choice = input("Digite o número do dispositivo ou /VOLTAR para sair: ")

            if choice == "/VOLTAR":
                break

            try:
                choice = int(choice)
                if 1 <= choice <= len(self.connected_devices):
                    device = self.connected_devices[choice - 1]

                    if device.protocol == "UDP":
                        print("Pressione 'Q' a qualquer momento para voltar ao menu principal.")
                        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
                            udp_socket.bind((device.device_ip, device.device_port))
                            print(f"Recebendo mensagens do dispositivo {device.device_type} em {device.device_ip}:{device.device_port}...")
                            last_addr = None
                            first_message_printed = False
                            while True:
                                #data, addr = udp_socket.recvfrom(1024)
                                #print(f"Recebido de {addr}: {data.decode()}")
                                data, addr = udp_socket.recvfrom(1024)
                                message = f"Recebido de {addr}: {data.decode()}"
                                # Mova o cursor para a primeira posição da linha anterior
                                #if last_addr:
                                    #move_cursor(0, last_addr[1] + 1)
                                if not first_message_printed:
                                    print(message)
                                    first_message_printed = True
                                else:
                                # Limpe as duas linhas anteriores
                                    print("\033[F\033[K\033[F\033[K", end="")
                                    print(message)
                                last_addr = addr
                                # Verifique continuamente se o usuário pressionou 'Q' para sair
                                #if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                                 #   user_input = input()
                                  #  if user_input == 'Q':
                                   #     break
                    else:
                        while True:
                            user_command = input(f"Digite /Menu ({device.device_type}) ou /VOLTAR: ")
                            if user_command == "/VOLTAR":
                                break
                            # Enviar o comando para o dispositivo e receber a resposta, se necessário
                            response = device.send_command(user_command)
                            print(response)
                else:
                    print("Escolha inválida. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Digite o número do dispositivo ou /VOLTAR.")






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

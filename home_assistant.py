import pika
import sys
import os



def get_public_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(("8.8.8.8", 80))
    public_ip = sock.getsockname()[0]
    sock.close()

    return public_ip

SERVER_IP = get_public_ip()
SERVER_PORT = 12345


def connect_to_client():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((SERVER_IP, SERVER_PORT))
    except socket.error:
        print("Não foi possível estabelecer conexão com o socket. Encerrando home assistant.")
        sys.exit()

    server_socket.listen(1)
    print(f"Home assistant iniciado no endereço {SERVER_IP}:{SERVER_PORT}")
    try:
        client_socket, client_address = server_socket.accept()
    except OSError:
        break
   


def lamp_callback(ch, method, properties, body):
    print(f"Nível de luminosidade: {body}")


def air_conditioner_callback(ch, method, properties, body):
    pass


def main():
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

    #channel.start_consuming()
    connect_to_client()  ##to na duvida sobre variaveis locais e globais; o socket ta local a essa funcao?
    



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nDispositivo encerrado.')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

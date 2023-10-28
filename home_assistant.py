import pika
import sys
import os


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

    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nDispositivo encerrado.')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

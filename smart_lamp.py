import pika
import time
import sys
import os


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='smart_lamp', exchange_type='fanout')

    light_level = '1'

    while (1):
        print(f"Nível de luminosidade: {light_level}")
        channel.basic_publish(exchange='smart_lamp',
                              routing_key='', body=light_level)
        time.sleep(5)

    connection.close()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nDispositivo encerrado.')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
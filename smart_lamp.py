import pika
import time
import sys
import os
import numpy as np

def read_light_data():

    mean_light = 500  # Média de luminosidade
    std_deviation = 2.0      # Desvio padrão da luminosidade

    light_value = round(np.random.normal(mean_light, std_deviation), 1)
    light_message = f"{light_value}lx"
    return light_message



def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='devices', exchange_type='direct')


    while (1):
        
        light_level = read_light_data()
        print(f"Nível de luminosidade: {light_level}")
        channel.basic_publish(exchange='devices',
                              routing_key='lamp', body=light_level)
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

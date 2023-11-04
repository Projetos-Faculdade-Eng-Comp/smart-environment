import pika
import time
import sys
import os
import numpy as np

def read_temperature_data():

    mean_temperature = 25  # Média de temperatura
    std_deviation = 2.0      # Desvio padrão da temperatura

    temp_value = round(np.random.normal(mean_temperature, std_deviation), 1)
    temp_message = f"{temp_value}ºC"
    return temp_message



def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    

    while (1):
        
        temp_level = read_temperature_data()
        print(f"Temperatura: {temp_level}")
        channel.basic_publish(exchange='devices',
                              routing_key='air_cond', body=temp_level)
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

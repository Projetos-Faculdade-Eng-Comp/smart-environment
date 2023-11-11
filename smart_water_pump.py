import pika
import time
import numpy as np
import threading
import grpc
from concurrent import futures
import actuators_service_pb2
import actuators_service_pb2_grpc

global mean_humidity
mean_humidity = 60
global status
status = False

def read_humidity_data():
    global mean_humidity
    std_deviation = 1.0  # Desvio padrão da umidade

    humidity_value = round(np.random.normal(mean_humidity, std_deviation), 1)
    return f"{humidity_value}%"

def sensor_thread():
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.exchange_declare(exchange='devices', exchange_type='direct')
        while True:
            humidity = read_humidity_data()
            print(f"Umidade do solo: {humidity}")
            channel.basic_publish(exchange='devices', routing_key='water_pump', body=humidity)
            time.sleep(5)

        connection.close()
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Erro de conexão com RabbitMQ: {e}")
    except KeyboardInterrupt:
        print('Encerrando o dispositivo sensor.')
    except Exception as e:
        print(f"Erro inesperado: {e}")

class ActuatorsService(actuators_service_pb2_grpc.ActuatorsServiceServicer):
    
    def turnOn(self, request, context):
        global mean_humidity
        global status

        if not status:
            print("Ligando a Bomba de água")
            mean_humidity += 10  # Aumenta a umidade
            status = True
            return actuators_service_pb2.Status(message="Bomba de água ligada com sucesso")
        else:
            return actuators_service_pb2.Status(message="A Bomba de água já está ligada")

    def turnOff(self, request, context):
        global mean_humidity
        global status

        if status:
            print("Desligando a Bomba de água")
            mean_humidity -= 10  # Diminui a umidade
            status = False
            return actuators_service_pb2.Status(message="bomba de água desligada com sucesso")
        else:
            return actuators_service_pb2.Status(message="A bomba de água já está desligada")

def atuador_thread():
    try:
        server = grpc.server(thread_pool=futures.ThreadPoolExecutor(max_workers=10))
        actuators_service_pb2_grpc.add_ActuatorsServiceServicer_to_server(ActuatorsService(), server)
        server.add_insecure_port('[::]:50053')
        server.start()
        server.wait_for_termination()
    except grpc.RpcError as e:
        print(f"Erro gRPC: {e}")
    except KeyboardInterrupt:
        print('Encerrando o dispositivo atuador.')
    except Exception as e:
        print(f"Erro inesperado: {e}")

if __name__ == '__main__':
    sensor_thread = threading.Thread(target=sensor_thread)
    atuador_thread = threading.Thread(target=atuador_thread)

    sensor_thread.start()
    atuador_thread.start()

    sensor_thread.join()
    atuador_thread.join()

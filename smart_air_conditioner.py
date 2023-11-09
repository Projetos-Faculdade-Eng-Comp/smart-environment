import pika
import time
import numpy as np
import threading
import grpc
from concurrent import futures
import air_conditioner_service_pb2
import air_conditioner_service_pb2_grpc

global mean_temperature
mean_temperature = 25

def read_temperature_data():
    global mean_temperature
    std_deviation = 2.0  # Desvio padrão da temperatura

    temp_value = round(np.random.normal(mean_temperature, std_deviation), 1)
    temp_message = f"{temp_value}ºC"
    return temp_message

def sensor_thread():
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.exchange_declare(exchange='devices', exchange_type='direct')

        while (1):
            temp_level = read_temperature_data()
            print(f"Temperatura: {temp_level}")
            channel.basic_publish(exchange='devices', routing_key='air_cond', body=temp_level)
            time.sleep(5)

        connection.close()
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Erro de conexão com RabbitMQ: {e}")
    except KeyboardInterrupt:
        print('Encerrando o dispositivo sensor de ar condicionado.')
    except Exception as e:
        print(f"Erro inesperado: {e}")

class AirConditionerService(air_conditioner_service_pb2_grpc.AirConditionerServiceServicer):
    def ligarArCondicionado(self, request, context):
        global mean_temperature
        print("Ligando o ar condicionado")
        mean_temperature -= 2  # Diminui a temperatura
        return air_conditioner_service_pb2.Status(message="Ar condicionado ligado com sucesso")

    def desligarArCondicionado(self, request, context):
        global mean_temperature
        print("Desligando o ar condicionado")
        mean_temperature += 2  # Aumenta a temperatura
        return air_conditioner_service_pb2.Status(message="Ar condicionado desligado com sucesso")

def atuador_thread():
    try:
        server = grpc.server(thread_pool=futures.ThreadPoolExecutor(max_workers=10))
        air_conditioner_service_pb2_grpc.add_AirConditionerServiceServicer_to_server(AirConditionerService(), server)
        server.add_insecure_port('[::]:50052')
        server.start()
        server.wait_for_termination()
    except grpc.RpcError as e:
        print(f"Erro gRPC: {e}")
    except KeyboardInterrupt:
        print('Encerrando o dispositivo atuador de ar condicionado.')
    except Exception as e:
        print(f"Erro inesperado: {e}")

if __name__ == '__main__':
    sensor_thread = threading.Thread(target=sensor_thread)
    atuador_thread = threading.Thread(target=atuador_thread)

    sensor_thread.start()
    atuador_thread.start()

    sensor_thread.join()
    atuador_thread.join()

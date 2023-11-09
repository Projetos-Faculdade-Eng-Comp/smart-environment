import pika
import time
import numpy as np
import threading
import grpc
from concurrent import futures
import lamp_service_pb2
import lamp_service_pb2_grpc

global mean_light
mean_light = 500
global status
status = False

def read_light_data():
    global mean_light
    std_deviation = 2.0  # Desvio padrão da luminosidade

    light_value = round(np.random.normal(mean_light, std_deviation), 1)
    light_message = f"{light_value}lx"
    return light_message

def sensor_thread():
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.exchange_declare(exchange='devices', exchange_type='direct')
        while True:
            light_level = read_light_data()
            print(f"Nível de luminosidade: {light_level}")
            channel.basic_publish(exchange='devices', routing_key='lamp', body=light_level)
            time.sleep(5)

        connection.close()
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Erro de conexão com RabbitMQ: {e}")
    except KeyboardInterrupt:
        print('Encerrando o dispositivo sensor.')
    except Exception as e:
        print(f"Erro inesperado: {e}")

class LampService(lamp_service_pb2_grpc.LampServiceServicer):
    def ligarLampada(self, request, context):
        global mean_light
        global status

        if not status:
            print("Ligando a lâmpada")
            mean_light += 100  # Aumenta a intensidade da luz
            status = True
            return lamp_service_pb2.Status(message="Lâmpada ligada com sucesso")
        else:
            return lamp_service_pb2.Status(message="A lâmpada já está ligada")

    def desligarLampada(self, request, context):
        global mean_light
        global status

        if status:
            print("Desligando a lâmpada")
            mean_light -= 100  # Diminui a intensidade da luz
            status = False
            return lamp_service_pb2.Status(message="Lâmpada desligada com sucesso")
        else:
            return lamp_service_pb2.Status(message="A lâmpada já está desligada")

def atuador_thread():
    try:
        server = grpc.server(thread_pool=futures.ThreadPoolExecutor(max_workers=10))
        lamp_service_pb2_grpc.add_LampServiceServicer_to_server(LampService(), server)
        server.add_insecure_port('[::]:50051')
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

import pika
import time
import numpy as np
import threading
import grpc
from concurrent import futures
import water_pump_service_pb2_grpc
import water_pump_service_pb2

global mean_flow
mean_flow = 30
global status
status = False

def read_flow_data():
    global mean_flow
    std_deviation = 3.0  # Desvio padrão da luminosidade

    flow_value = round(np.random.normal(mean_flow, std_deviation), 1)
    return f"{flow_value}L/min"

def sensor_thread():
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.exchange_declare(exchange='devices', exchange_type='direct')
        while True:
            light_level = read_flow_data()
            print(f"Vazão: {light_level}")
            channel.basic_publish(exchange='devices', routing_key='water_pump', body=light_level)
            time.sleep(5)

        connection.close()
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Erro de conexão com RabbitMQ: {e}")
    except KeyboardInterrupt:
        print('Encerrando o dispositivo sensor.')
    except Exception as e:
        print(f"Erro inesperado: {e}")

class WaterPumpService(water_pump_service_pb2_grpc.WaterPumpServiceServicer):
    
    def TurnOnWaterPump(self, request, context):
        global mean_flow
        global status

        if not status:
            print("Ligando a Bomda de água")
            mean_flow += 10  # Aumenta a intensidade da luz
            status = True
            return water_pump_service_pb2.Status(message="Bomda de água ligada com sucesso")
        else:
            return water_pump_service_pb2.Status(message="A Bomda de água já está ligada")

    def TurnOffWaterPump(self, request, context):
        global mean_flow
        global status

        if status:
            print("Desligando a Bomda de água")
            mean_flow -= 10  # Diminui a intensidade da luz
            status = False
            return water_pump_service_pb2.Status(message="Bomda de água desligada com sucesso")
        else:
            return water_pump_service_pb2.Status(message="A Bomda de água já está desligada")

def atuador_thread():
    try:
        server = grpc.server(thread_pool=futures.ThreadPoolExecutor(max_workers=10))
        water_pump_service_pb2_grpc.add_WaterPumpServiceServicer_to_server(WaterPumpService(), server)
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

import pika
import time
import threading
import grpc
from concurrent import futures
import board
import adafruit_dht
import actuators_service_pb2
import actuators_service_pb2_grpc
import digitalio

global status
status = False

global dhtDevice
dhtDevice = adafruit_dht.DHT22(board.D4)
GPIO.setmode(GPIO.BCM) 
GPIO.setup(17, GPIO.OUT)
GPIO.output(17, GPIO.LOW)


def read_humidity_data():
    try:
        humidity_value = dhtDevice.humidity
    except Exception as e:
        return "Erro na leitura do sensor"
    return f"{humidity_value:.2f}%"


def sensor_thread():
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='192.168.0.87'))  # substituir pelo endereço do rabbitmq
        channel = connection.channel()
        channel.exchange_declare(exchange='devices', exchange_type='direct')
        while True:
            humidity = read_humidity_data()
            print(f"Umidade ambiente: {humidity}")
            channel.basic_publish(exchange='devices',
                                  routing_key='water_pump', body=humidity)
            time.sleep(5)
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Erro de conexão com RabbitMQ: {e}")
    except KeyboardInterrupt:
        print('Encerrando o dispositivo sensor.')
    except Exception as e:
        print(f"Erro inesperado: {e}")
    finally:
        if connection and connection.is_open:
            connection.close()


class ActuatorsService(actuators_service_pb2_grpc.ActuatorsServiceServicer):

    def turnOn(self, request, context):
        global status
        if not status:
            print("Ligando o umidificador")
            GPIO.output(17, GPIO.HIGH)
            status = True

            return actuators_service_pb2.Status(message="Umidificador ligado com sucesso")
        else:
            return actuators_service_pb2.Status(message="O umificador já está ligado")

    def turnOff(self, request, context):
        global status
        if status:
            print("Desligando o umidificador")
            GPIO.output(17, GPIO.LOW)
            status = False
            return actuators_service_pb2.Status(message="Umidificador desligado com sucesso")
        else:
            return actuators_service_pb2.Status(message="O umidificador já está desligado")

def atuador_thread():
    try:
        server = grpc.server(
            thread_pool=futures.ThreadPoolExecutor(max_workers=10))
        actuators_service_pb2_grpc.add_ActuatorsServiceServicer_to_server(
            ActuatorsService(), server)
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

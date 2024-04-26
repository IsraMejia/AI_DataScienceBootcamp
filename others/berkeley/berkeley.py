import time
from random import uniform
from servidor import Servidor
from cliente import Cliente
import threading

class BerkeleyClient(Cliente):
    def __init__(self, host, port, initial_time):
        super().__init__(host, port)
        self.time_offset = initial_time - time.time()
        self.running = True

    def adjust_time(self, new_time):
        self.time_offset = new_time - time.time()

    def get_time(self):
        return time.time() + self.time_offset

    def recibir_mensajes(self):
        while self.running:
            try:
                # Recibir mensaje del servidor
                mensaje_recibido = self.client_socket.recv(1024).decode('utf-8')
                print(f"(servidor): {mensaje_recibido}")  # Imprimir el mensaje recibido
            except OSError:
                break

def main():
    host = '127.0.0.1'
    port = 9999 

    # Crear 3 clientes con relojes desfasados
    clientes = [BerkeleyClient(host, port, uniform(time.time() - 10.5, time.time() + 20.5)) for _ in range(3)]

    # Crear el servidor
    servidor = Servidor(host, port)

    # Iniciar el servidor en un hilo
    servidor_thread = threading.Thread(target=servidor.iniciar)
    servidor_thread.start()

    # Realizar la sincronización al menos 3 veces
    for iteration in range(1, 4):
        print(f"Iteración {iteration} de sincronización:")
        # El maestro (primer cliente) recoge los tiempos de todos los clientes
        times = [cliente.get_time() for cliente in clientes]
        print("Tiempos de los clientes:")
        for i, t in enumerate(times):
            print(f"Cliente {i}: {time.strftime('%H:%M:%S', time.localtime(t))}")

        # El maestro calcula el tiempo medio
        average_time = sum(times) / len(times)
        print(f"Tiempo medio: {time.strftime('%H:%M:%S', time.localtime(average_time))}")

        # El maestro envía el tiempo medio a todos los clientes
        for cliente in clientes:
            cliente.adjust_time(average_time)
            print(f"Cliente {clientes.index(cliente)} ajustó su reloj a {time.strftime('%H:%M:%S', time.localtime(cliente.get_time()))}")

        time.sleep(1)  # Esperar un segundo antes de la próxima sincronización

    # Cerrar el servidor
    servidor.stop()

    # Desconectar los clientes
    for cliente in clientes:
        cliente.desconectar()

if __name__ == "__main__":
    main()
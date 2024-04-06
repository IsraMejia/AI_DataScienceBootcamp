import time
from cliente import Cliente

class BerkeleyClient(Cliente):
    def __init__(self, host, port):
        super().__init__(host, port)
        self.time_offset = 0

    def adjust_time(self, new_time):
        self.time_offset = new_time - time.time()

    def get_time(self):
        return time.time() + self.time_offset

def main():
    host = '127.0.0.1'
    port = 9999

    # Crear 3 clientes
    clientes = [BerkeleyClient(host, port) for _ in range(3)]

    # Supongamos que el primer cliente es el maestro
    maestro = clientes[0]

    while True:
        # El maestro recoge los tiempos de todos los clientes
        times = [cliente.get_time() for cliente in clientes]

        # El maestro calcula el tiempo medio
        average_time = sum(times) / len(times)

        # El maestro envía el tiempo medio a todos los clientes
        for cliente in clientes:
            cliente.adjust_time(average_time)

        time.sleep(1)  # Esperar un segundo antes de la próxima sincronización

if __name__ == "__main__":
    main()
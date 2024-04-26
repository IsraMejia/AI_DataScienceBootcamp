import socket
import threading
import time
import signal

class Servidor:
    def __init__(self, host, port):
        self.host = host  # Dirección IP del servidor
        self.port = port  # Puerto en el que el servidor escuchará las conexiones
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crear un socket TCP/IP
        self.running = False  # Bandera para indicar si el servidor está en ejecución

    def iniciar(self):
        try:
            # Asociar el socket con la dirección y el puerto
            self.server_socket.bind((self.host, self.port))
            # Escuchar conexiones entrantes, permitir hasta 5 conexiones en cola
            self.server_socket.listen(5)
            self.running = True
            print("Servidor iniciado. Esperando conexiones...")
            while self.running:
                # Aceptar la conexión entrante
                client_socket, client_address = self.server_socket.accept()
                print(f"(servidor): Conexión establecida con {client_address}")
                # Crear un objeto Cliente para manejar la conexión con el cliente
                cliente = Cliente(client_socket, self)
                # Iniciar un hilo para manejar la recepción de mensajes del cliente
                recibir_thread = threading.Thread(target=cliente.recibir_mensajes)
                recibir_thread.start()
                # Iniciar un hilo para manejar el envío de mensajes al cliente
                enviar_thread = threading.Thread(target=self.enviar_mensajes, args=(cliente,))
                enviar_thread.start()
        except KeyboardInterrupt:
            self.stop()

    def enviar_mensajes(self, cliente):
        while self.running:
            # Leer mensaje desde la consola
            mensaje_enviado = input("(servidor): ")
            # Enviar el mensaje al cliente
            cliente.enviar_mensaje(mensaje_enviado)

    def stop(self):
        self.running = False
        self.server_socket.close()
        print("Servidor detenido.")

class Cliente:
    def __init__(self, client_socket, servidor):
        self.client_socket = client_socket  # Socket del cliente
        self.servidor = servidor  # Instancia del servidor asociado

    def recibir_mensajes(self): 
        while self.servidor.running:
            try:
                # Recibir mensaje del cliente
                mensaje_recibido = self.client_socket.recv(1024).decode('utf-8')
                print(f"(cliente): {mensaje_recibido}")  # Imprimir el mensaje recibido
            except OSError:
                break

    def enviar_mensaje(self, mensaje):
        # Enviar mensaje al cliente
        self.client_socket.send(bytes(mensaje, 'utf-8'))

def main():
    host = '127.0.0.1'  # Dirección IP del servidor
    port = 9999  # Puerto en el que el servidor escuchará las conexiones
    servidor = Servidor(host, port)  # Crear una instancia de Servidor
    servidor.iniciar()  # Iniciar el servidor

if __name__ == "__main__":
    main()
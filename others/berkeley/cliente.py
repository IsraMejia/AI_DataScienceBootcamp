import socket
import threading
import time
import signal

class Cliente:
    def __init__(self, host, port):
        self.host = host  # Dirección IP del servidor
        self.port = port  # Puerto en el que el servidor está escuchando
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crear un socket TCP/IP
        self.running = True
        self.conectar()  # Conectarse al servidor

    def conectar(self):
        # Establecer la conexión con el servidor
        self.client_socket.connect((self.host, self.port))
        # Iniciar un hilo para manejar la recepción de mensajes del servidor
        recibir_thread = threading.Thread(target=self.recibir_mensajes)
        recibir_thread.start()
        print("(cliente): Conectado al servidor. Puedes empezar a enviar mensajes.")

    def recibir_mensajes(self):
        while self.running:
            try:
                # Recibir mensaje del servidor
                mensaje_recibido = self.client_socket.recv(1024).decode('utf-8')
                print(f"(servidor): {mensaje_recibido}")  # Imprimir el mensaje recibido
            except OSError:
                break

    def enviar_mensaje(self, mensaje): 
        # Enviar mensaje al servidor
        self.client_socket.send(bytes(mensaje, 'utf-8'))

    def desconectar(self):
        self.running = False
        self.client_socket.close()
        print("(cliente): Desconectado del servidor.")

def main():
    host = '127.0.0.1'  # Dirección IP del servidor
    port = 9999  # Puerto en el que el servidor está escuchando
    cliente = Cliente(host, port)  # Crear una instancia de Cliente
    try:
        while True:
            mensaje = input("(cliente): ")  # Leer mensaje desde la consola
            cliente.enviar_mensaje(mensaje)  # Enviar el mensaje al servidor
    except KeyboardInterrupt:
        cliente.desconectar()

if __name__ == "__main__":
    main()
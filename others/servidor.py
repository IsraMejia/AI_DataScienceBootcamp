import socket
import threading

class Servidor:
    def __init__(self, host, port):
        self.host = host  # Dirección IP del servidor
        self.port = port  # Puerto en el que el servidor escuchará las conexiones
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crear un socket TCP/IP

    def iniciar(self):
        self.server_socket.bind((self.host, self.port))  # Asociar el socket con la dirección y el puerto
        self.server_socket.listen(5)  # Escuchar conexiones entrantes, permitir hasta 5 conexiones en cola
        print("Esperando conexiones...")
        while True:
            client_socket, client_address = self.server_socket.accept()  # Aceptar la conexión entrante
            print(f"(servidor): Conexión establecida con {client_address}")
            cliente = Cliente(client_socket, self)  # Crear un objeto Cliente para manejar la conexión con el cliente
            recibir_thread = threading.Thread(target=cliente.recibir_mensajes)
            recibir_thread.start()  # Iniciar un hilo para manejar la recepción de mensajes del cliente
            enviar_thread = threading.Thread(target=self.enviar_mensajes, args=(cliente,))
            enviar_thread.start()  # Iniciar un hilo para manejar el envío de mensajes al cliente

    def enviar_mensajes(self, cliente):
        while True:
            mensaje_enviado = input( )  # Leer mensaje desde la consola
            cliente.enviar_mensaje(mensaje_enviado)  # Enviar el mensaje al cliente

class Cliente:
    def __init__(self, client_socket, servidor):
        self.client_socket = client_socket  # Socket del cliente
        self.servidor = servidor  # Instancia del servidor asociado

    def recibir_mensajes(self):
        while True:
            try:
                mensaje_recibido = self.client_socket.recv(1024).decode('utf-8')  # Recibir mensaje del cliente
                print(f"(cliente): {mensaje_recibido}")  # Imprimir el mensaje recibido
            except OSError:
                break

    def enviar_mensaje(self, mensaje):
        self.client_socket.send(bytes(mensaje, 'utf-8'))  # Enviar mensaje al cliente

def main():
    host = '127.0.0.1'  # Dirección IP del servidor
    port = 9999  # Puerto en el que el servidor escuchará las conexiones
    servidor = Servidor(host, port)  # Crear una instancia de Servidor
    servidor.iniciar()  # Iniciar el servidor

if __name__ == "__main__":
    main()

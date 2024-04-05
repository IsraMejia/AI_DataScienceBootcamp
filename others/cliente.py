import socket
import threading

def recibir_mensajes(server_socket):
    while True:
        try:
            mensaje_recibido = server_socket.recv(1024).decode('utf-8')
            print(mensaje_recibido)
        except OSError:
            break

def enviar_mensajes(server_socket):
    while True:
        mensaje_enviado = input()
        server_socket.send(bytes(mensaje_enviado, 'utf-8'))

def main():
    host = '127.0.0.1'  # Cambia esto por la IP del servidor si es necesario
    port = 9999
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((host, port))
    
    recibir_thread = threading.Thread(target=recibir_mensajes, args=(server_socket,))
    recibir_thread.start()
    
    enviar_thread = threading.Thread(target=enviar_mensajes, args=(server_socket,))
    enviar_thread.start()

if __name__ == "__main__":
    main()

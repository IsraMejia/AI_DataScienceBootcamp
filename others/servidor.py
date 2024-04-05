import socket
import threading

def recibir_mensajes(client_socket):
    while True:
        try:
            mensaje_recibido = client_socket.recv(1024).decode('utf-8')
            print(mensaje_recibido)
        except OSError:
            break

def enviar_mensajes(client_socket):
    while True:
        mensaje_enviado = input()
        client_socket.send(bytes(mensaje_enviado, 'utf-8'))

def main():
    host = '127.0.0.1'  # Cambia esto por la IP del servidor si es necesario
    port = 9999
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    
    print("Esperando conexiones...")
    client_socket, client_address = server_socket.accept()
    print(f"Conexión establecida con {client_address}")
    
    recibir_thread = threading.Thread(target=recibir_mensajes, args=(client_socket,))
    recibir_thread.start()
    
    enviar_thread = threading.Thread(target=enviar_mensajes, args=(client_socket,))
    enviar_thread.start()

if __name__ == "__main__":
    main()

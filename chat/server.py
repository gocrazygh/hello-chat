import socket
import threading

host = '127.0.0.1'
port = 55555

# It creates a socket object, binds it to the host and port, and then listens for connections.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
usernames = []

def broadcast(message):
    """
    It takes a message and sends it to all the clients in the clients list
    
    :param message: The message to be sent to all clients
    """
    for client in clients:
        client.send(message)

def handle(client):
    """
    It receives messages from the client, broadcasts them to all the other clients, and if the client
    disconnects, it removes the client from the list of clients and broadcasts a message to all the
    other clients that the client has left
    
    :param client: The client socket
    """
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            broadcast('{} left!'.format(username).encode('ascii'))
            usernames.remove(username)
            break

def receive():
    """
    It creates a thread for each client that connects to the server.
    """
    while True:
        print("Server is running...")
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        client.send('NICK'.encode('ascii'))
        username = client.recv(1024).decode('ascii')
        usernames.append(username)
        clients.append(client)

        print("username is {}".format(username))
        broadcast("{} joined!".format(username).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

if __name__  == "__main__":
    receive()
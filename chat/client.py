import time
import socket
import threading

username = input("Enter a username: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

def receive():
    """
    It receives messages from the server and prints them out.
    """
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(username.encode('ascii'))
            else:
                print(message)
        except:
            print("An error occured!")
            client.close()
            break

def write():
    """
    It takes the current time, the username, and the message, and sends it to the server
    """
    while True:
        timestamp = str(time.strftime('%H:%M:%S'))
        message = '{} <{}> {}'.format(timestamp, username, input(''))
        client.send(message.encode('ascii'))


if __name__  == "__main__":
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()
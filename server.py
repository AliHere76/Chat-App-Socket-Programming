import threading
import socket

host = '127.0.0.1'
port = 3355

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "Goodbye...":
                index = client.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                print(f'{nickname} left the chat!')
                broadcast(f'{nickname} left the chat!'.encode('utf-8'))
                nicknames.remove(nickname)
                break        
            
            print(message)
            broadcast(message.encode('utf-8'))
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            print(f'{nickname} left the chat!')
            broadcast(f'{nickname} left the chat!'.encode('utf-8'))
            nicknames.remove(nickname)
            break

def recieve():
    while True:
        client, address = server.accept()
        print(f'Connected with {str(address)}')

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}!')
        client.send('Connected to the server!'.encode('utf-8'))
        broadcast(f'\n{nickname} joined the chat!\n'.encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print('Server is Listening...')
recieve()
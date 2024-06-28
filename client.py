import socket
import threading
import sys

nickname = input("Choose a nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('3.6.115.64',15078))

flag = True

def write():
    global flag
    while True:
        message = str(input())
        if message == "quit":
            flag = False
            client.send("Goodbye...".encode('utf-8'))
            print("Connection Terminated!")
            break            
        else:
            client.send(f'{nickname}: {message}'.encode('utf-8'))
    
    sys.exit()

def recieve():
    global flag
    while True:
        if not flag:
            print("Communication successful!")
            break
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print("An error occurred!")
            client.close()
            break



recieve_thread = threading.Thread(target = recieve)
recieve_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
import socket
import threading
#socket-send msg across a network
#thread-seperate flow of execution a program can be divided intomany threads to ease the flow

nickname = input("Enter your nickname: ")
if nickname == 'admin':
    password = input("ENTER THE PASSWORD: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))
stop_thread = False
#stop-thread to terminate the thread

def receive():
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
                next_message = client.recv(1024).decode('ascii')
                if next_message == 'PASS':
                    client.send(password.encode('ascii'))
                    if client.recv(1024).decode('ascii') == 'REFUSE':
                        print("Connection denied!. Recheck your password!")
                        stop_thread = True
                elif next_message == 'BAN':
                    print("Connection refused because of a ban.")
                    client.close()
                    stop_thread = True
            else:
                print(message)
        except:
            print("An error occurred")
            client.close()
            break

#len(nickname) + 2: means           username+" "+:
 #message[len(nickname) + 2 + 6:-  /KICK+" "
def write():
    while True:
        if stop_thread:
            break
        message = f'{nickname}: {input(" ")}'
        if message[len(nickname) + 2:].startswith('/'):
            if nickname == 'admin':
                if message[len(nickname) + 2:].startswith('/kick'):
                    client.send(f'KICK {message[len(nickname) + 2 + 6:]}'.encode('ascii'))
                elif message[len(nickname) + 2:].startswith('/ban'):
                    client.send(f'BAN {message[len(nickname) + 2 + 5:]}'.encode('ascii'))
            else:
                print("Sorry!Commands can only be executed by the admin")
        else:
            client.send(message.encode('ascii'))


receive_thread = threading.Thread(target=receive)
receive_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()

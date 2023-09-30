import threading
import socket
host="127.0.0.1"#local
port=55555


server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

clients = []
nicknames = []
def broadcast(message):
    for client in clients:
        client.send(message)
#if one client says hi all the others must know wats happening in the server
def handle(client):
    while True:
        try:
            msg=message=client.recv(1024)
            if msg.decode('ascii').startswith('KICK'):
                if nicknames[clients.index(client)]=='admin':
                    name_to_kick=msg.decode('ascii')[5:]
                    kick_user(name_to_kick)
                else:
                    client.send("Command was denied!".encode('ascii'))

            elif msg.decode('ascii').startswith('BAN'):
                if nicknames[clients.index(client)]=='admin':
                    name_to_ban=msg.decode('ascii')[4:]
                    kick_user(name_to_ban)

                    with open('bans.txt','a') as f:
                        f.write(f'{name_to_ban}\n')
                    print(f'{name_to_ban} was banned!')
                else:
                    client.send("Command was denied!".encode('ascii'))
            else:
                broadcast(message)
        except:
            if client in clients:
                index=clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                broadcast(f' {nickname}left the chat!'.encode('ascii'))
#whenever a client created nickname also created wth same index that means if client removed nickname also removed
                nicknames.remove(nickname)
                break

def receive():
    while True:
        client,address=server.accept()
#new client joins the server and then gts connected after that recieves a msg from server to give nickname then sends nickname and this gets appended
#we use continie to break the loop fro that single time bt if we use break it leads to skipping of the whole thread
        print(f"connected with {str(address)}")
        
        client.send('NICK'.encode('ascii'))
        nickname=client.recv(1024).decode('ascii')

        with open('bans.txt','r') as f:
            bans=f.readlines()

        if nickname+'\n' in bans:
            client.send('BAN'.encode('ascii'))
            client.close()
            continue

        if nickname=='admin':
            client.send('PASS'.encode('ascii'))
            password=client.recv(1024).decode('ascii')


            if password!='CRCT':
                client.send('REFUSE'.encode('ascii'))
                client.close()
                continue

        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickaname of client is {nickname} !')
        broadcast(f'{nickname} joined the chat!'.encode('ascii'))
        client.send('Hurry!Connected to the server!'.encode('ascii'))

        thread=threading.Thread(target=handle,args=(client,))
        thread.start()
def kick_user(name):
    if name in nicknames:
        name_index=nicknames.index(name)
        client_to_kick=clients[name_index]
        clients.remove(client_to_kick)
        client_to_kick.send("YOU WERE KICKED BY ADMIN!".encode('ascii'))
        client_to_kick.close()
        nicknames.remove(name)
        broadcast(f'{name} was kicked by the admin'.encode('ascii'))

print("server is listening")
receive()
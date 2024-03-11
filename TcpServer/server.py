import socket
import threading as t
import os
from datetime import datetime

HOST = '127.0.0.1'
PORT = 19881
HOME = '../Examples/'

status = 0
clients = []

server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()


def broadcast(msg: str):
    for c in clients:
        c.send(msg.encode())

def print_log(text: str):
    now = datetime.now()
    print(f'<{now.time()}> {text}')

def handle(client: socket.socket):
    global status
    while True:
        try:
            msg = client.recv(4096).decode()
            cmd = msg.strip().split(',')


            # Get file content by name
            if (msg.startswith('GET')):
                print_log('Execute GET command')
                file = cmd[1]
                with open(HOME+file, mode='r', encoding='utf-8') as fp:
                    data = fp.read()
                client.send(data.encode())


            # Get list of available files
            elif (msg == 'LIST'):
                print_log('Execute LIST command')
                _list = []
                for i in os.scandir(HOME):
                    if not i.is_dir():
                        _list.append(i.name)
                client.send(';'.join(_list).encode())


            # Update files
            elif (msg.startswith('UPDATE')):
                print_log(f'Execute UPDATE command')
                
                file_name = cmd[1]
                n_lines = int(cmd[2])
                data = ""
                
                for i in range(n_lines):
                    msg = client.recv(4096).decode()
                    data += msg

                with open(HOME+file, mode='w+', encoding='utf-8') as fp:
                    fp.write(data)


            # Handle client close connection
            elif (msg == 'TERM'):
                print_log('Client disconnected')
                clients.index
                clients.remove(client)
                client.close()
                break
            
        except:
            print_log('Client disconnected')
            clients.remove(client)
            client.close()
            break
        if status == 0:
            break

def acct_loop():
    print_log('Server listening connections...')
    while True:
        try:
            client, address = server.accept()
            clients.append(client)
            print_log(f'{address} connected!')
            client_handler = t.Thread(target=handle, args=(client,))
            client_handler.start()
        except:
            break

def main():
    global status, clients
    listening_handler = t.Thread(target=acct_loop)
    listening_handler.start()

    while True:
        s = input('Enter command \n')

        if s == 'shutdown':
            server.close()
            broadcast('INT_CON')
            status = 0
            break
        elif s == 'list':
            print(clients)
        elif s == 'stop':
            server.close()
    
    listening_handler.join()

if __name__ == '__main__':
    status = 1
    main()
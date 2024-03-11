import socket
import threading
import os


TCP_MAX_SIZE: int = 4096
HOST = '127.0.0.1'
PORT = 19881

status = 0

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
data = ""

def send_file():
    s.recv(data.encode())
    s.recv('>END'.encode())

def handle_commands(s: socket.socket):
    global data
    while True:
        try:
            msg = s.recv(TCP_MAX_SIZE)

            if msg.decode('utf-8') == '>RECV':
                data = ""
                while (msg != '>END'):
                    data.join(msg)
                    msg = s.recv(TCP_MAX_SIZE).decode()
                print(data)
           
            if msg.decode() == 'INT_CON':       
                s.close()
                break


            print('\r\r' + msg.decode('utf-8') + '\n', end='')
        except socket.error as e:
            print(e)
        
        global status
        status = 0


def main():

    threading.Thread(target=handle_commands, args=(s, )).start()

    while True:
        msg = input('Message: ')
        s.send(msg.encode('utf-8'))
        if (msg.startswith('UPDATE')):
            send_file()

        if not msg.startswith('>'):
            ...
        if (msg == '>exit'):
            os._exit(1)


if __name__ == '__main__':
    status = 1
    main()
    
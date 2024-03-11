import webview
import os
import threading
import socket


class MainModel:
    TCP_MAX_SIZE: int = 4096
    HOST = '127.0.0.1'
    PORT = 19881
    __files_list = []
    __sock_con = None
    __opened_file = None

    def __init__(self):
        self.__sock_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock_con.connect((self.HOST, self.PORT))
        
        self.__scan_folder()

    def open_file(self, file: str = None):
        w = webview.active_window()
        self.opened_file = file
        self.__sock_con.send(f'GET,{file}'.encode())
        data = self.__sock_con.recv(4096)            
        
        return data.decode()
    
    def close_file():
        pass

    def save_file(self, data: str):
        encoded_data = data.encode()
        lines = len(encoded_data.split(b'\n'))
        print(self.opened_file)
        self.__sock_con.send(f'UPDATE,{self.opened_file},{lines}'.encode())
        self.__sock_con.send(encoded_data+b'\n')

    def open_folder(self, folder="", op=""):
        return self.folder_list

    def __scan_folder(self):
        w = webview.active_window()
        self.__sock_con.send('LIST'.encode())
        data = self.__sock_con.recv(4096).decode()

        if data == "":
            w.evaluate_js("app.new_alert(516, 'Folder is empty')")
        else:
            for i in data.split(';'):
                self.__files_list.append({
                    'name': i,
                    'path': i,
                    'type': 'o'
                })

    def __del__(self):
        self.__sock_con.send('TERM'.encode())

    @property
    def folder_list(self):
        return self.__files_list

    @folder_list.setter
    def folder_list(self, value):
        self.__files_list = value

    @property
    def opened_file(self):
        return self.__opened_file

    @opened_file.setter
    def opened_file(self, value):
        self.__opened_file = value


 

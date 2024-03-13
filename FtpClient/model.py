import webview
import os
import shutil
from ftplib import FTP


class MainModel:
    __ftp_con = None
    __supported_filetypes: list = [
        '.uni',
    ]
    __folder_list = []
    __opened_file = None

    def __init__(self):
        self.__ftp_con = FTP('127.0.0.1')
        self.__ftp_con.port = 21
        self.__ftp_con.login(user='sensor', passwd='12345')

        os.mkdir("./temp")
        self.__scan_folder()

    def open_file(self, file: str = None):
        w = webview.active_window()
        self.opened_file = file
        self.__ftp_con.retrlines(
            f'RETR {file}', 
            open(f'./temp/{file}', 'w+', encoding='utf-8').write
        )
        with open(f'./temp/{file}', mode='r', encoding='utf-8') as fp:
            data = fp.read()
        return data

    def save_file(self, data, op=2):
        w = webview.active_window()
        with open(f'./temp/{self.opened_file}', mode='w+', encoding='utf-8') as fp:
            fp.write(data)
        
        self.__ftp_con.storlines(
            f'STOR {self.opened_file}', 
            open(f'./temp/{self.opened_file}', mode='rb')
        )

    def open_folder(self, folder="", op=""):
        return self.folder_list
    
    def __scan_folder(self):
        w = webview.active_window()
        self.__folder_list.clear()
        data = []
        self.__ftp_con.retrlines('MLSD', data.append)
        print(data)
        for item in data:
            i = item.split(';')
            self.__folder_list.append({
                'name': i[4].lstrip(),
                'path': i[4].lstrip(),
                'type': 'd' if (i[3] == 'type=dir') else 'o'
            })

    @property
    def supported_filtypes(self):
        return self.__supported_filetypes

    @property
    def folder_list(self):
        return self.__folder_list

    @folder_list.setter
    def folder_list(self, value):
        self.__folder_list = value

    @property
    def opened_file(self):
        return self.__opened_file

    @opened_file.setter
    def opened_file(self, value):
        self.__opened_file = value

    def __del__(self):
        self.__ftp_con.close()
        if os.path.exists('./temp'):
            shutil.rmtree('./temp')

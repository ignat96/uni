from webview import *
from ftplib import FTP
import model
import os




if __name__ == "__main__":
    # _model_ = model.MainModel()
    # main_view = create_window("Uni", url="./main_view.html", js_api=_model_)
    ftp = FTP('127.0.0.1')
    ftp.port = 19881
    ftp.login(user='sensor', passwd='12345')

    # cwd - Change path. Can be fullpath or dirname in the pwd
    # pwd - Path to working dir. Current workdir
    ftp.cwd('/test')
    print(ftp.pwd())
    ftp.dir()

    # get list of files
    c = []
    def assign_c(v):
        c.append(v.split(';'))
    # ftp.retrlines('MLSD', assign_c)
    # [print(n, end='\n') for n in c]
        
    #  get file
    def assign_b(value):
        global b
        b = value
    # ftp.retrlines('RETR group name.uni', assign_b)
    # print(b)
    
    ftp.close()
    
    # start(debug=True)

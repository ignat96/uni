import os
import logging

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import ThreadedFTPServer

def main():
    auth = DummyAuthorizer()

    auth.add_user('sensor', '12345', r'F:\Projects\Uni\uni\Examples', perm='elradfmwMT')

    handler = FTPHandler
    handler.authorizer = auth

    handler.banner = 'pyftpd ready.'
    
    address = ('127.0.0.1', 21)
    server = ThreadedFTPServer(address, handler)
    server.max_cons = 8
    server.max_cons_per_ip = 2

    logging.basicConfig(filename='./pyftpd.log', level=logging.INFO)
    print('sdfdsf')
    server.serve_forever()


if __name__ == '__main__':
    main()
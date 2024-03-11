import os
import json
from bottle import route, run, static_file, template, request

FILE_SHARE_DIR = '../Examples/web/'

# Get js and styles
@route('/src/<filename:path>')
def src(filename):
    return static_file(filename=filename, root='./src')

# Index page
@route('/')
def main():
    return template('index.html')

# Get files list
@route('/file_api/list')
def get_files_list():
    data = []
    for i in os.scandir(FILE_SHARE_DIR):
        data.append({
            'name': i.name,
            'path': i.path,
            'type': 'o'
        })
    return json.dumps(data)

@route('/file_api/get', method='GET')
def get_file_data():
    pass

@route('/file_api/upload', method='POST')
def upload_file_data():
    pass

run(host='127.0.0.1', reloader=True)
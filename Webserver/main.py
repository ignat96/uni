import os
import json
from bottle import run, static_file, template, request
from bottle import route, post, get

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


@get('/file_api/get/<file_name>')
def get_file_data(file_name):
    data = {}
    with open(FILE_SHARE_DIR+file_name, mode='r', encoding='utf-8') as fp:
        data = fp.read()
    
    return json.dumps(data)


@post('/file_api/upload')
def upload_file_data():
    data = request.json

    with open(FILE_SHARE_DIR+data['file_name'], mode='w+', encoding='utf-8') as fp:
        fp.write(json.dumps(data['data']))

run(host='127.0.0.1', reloader=True)
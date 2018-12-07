#!/usr/bin/env python
# -*- coding: utf_8 -
import socketio
import eventlet
import eventlet.wsgi
from flask import Flask, render_template
from flask import request
from config import config
sio = socketio.Server()
app = Flask(__name__)

# post方法：上传文件的
@app.route('/auto/upload', methods=['post'])
def upload():
    fname = request.files.get('file')  #获取上传的文件
    if fname:

        new_fname = config['upload_path']+'/'+ fname.filename
        fname.save(new_fname)  #保存文件到指定路径
        return '{"name": "'+fname.filename+'"}'
    else:
        return '{"msg": "请上传文件！"}'

@app.route('/auto/deploy', methods=['post'])
def deploy():
    print request.data,type(request.data)
    import json
    data = json.loads(request.data)
    file_name = config["upload_path"]+"/"+data["name"]
    import zipfile
    dist = zipfile.ZipFile(file_name)
    dist.extractall(path=config["dest_dir"])
    dist.close()
    return '{"msg":"success"}'

if __name__ == '__main__':
    # wrap Flask application with engineio's middleware
    app = socketio.Middleware(sio, app)

    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', config['port'])), app)
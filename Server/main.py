import json
from typing import Dict

import dict as d
import album
import reader

from flask import Flask
from flask_sockets import Sockets
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

app = Flask(__name__)
sockets = Sockets(app)

@app.route('/')
def index():
    return '/'

@sockets.route('/ws')
def websocket_dispatch(ws):
    while not ws.closed:
        frame = ws.receive()
        if not frame:
            print('新连接', flush=True)
            return
        print(frame, flush=True)
        try:
            request = json.loads(frame)
            api : str   = request['api']
            args: Dict  = request['args']
            _, mod, method = api.split('/')
            if mod == 'dict': mod = 'd'
            status, retval = getattr(globals()[mod], method)(**args)
        except json.decoder.JSONDecodeError as e:
            status = 400
            retval = 'JSON Format Error: ' + e.msg
        ws.send(json.dumps({
            'status': status,
            'retval': retval
        }))


if __name__ == '__main__':
    server = pywsgi.WSGIServer(('0.0.0.0', 8081), app, handler_class=WebSocketHandler)
    server.serve_forever()
    # app.run(host='0.0.0.0',port=8080,debug=True)

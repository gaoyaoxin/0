import json
from typing import Dict

import dict as d
import album

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
            if api.startswith('/album/'):
                api = api[7:]
                if not getattr(album, api):
                    print(f'API: /album/{api} 不存在，忽略请求', flush=True)
                    return
                status, retval = getattr(album, api)(**args)
            else:
                if not getattr(d, api):
                    print(f'API: {api} 不存在，忽略请求', flush=True)
                    return
                status, retval = getattr(d,     api)(**args)
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

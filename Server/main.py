import json
from flask import Flask
from flask_sockets import Sockets

import dict as d

app = Flask(__name__)
sockets = Sockets(app)

@app.route('/')
def index():
    return '/'

@sockets.route('/ws')
def websocket_dispatch(ws):
    while not ws.closed:
        frame = ws.receive()
        print(frame)
        if frame:
            request = json.loads(frame)
            retval = getattr(d, request['api'])(**request['args'])
            ws.send(json.dumps({
                'status': 200,
                'retval': retval,
            }))


if __name__ == '__main__':
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 8081), app, handler_class=WebSocketHandler)
    server.serve_forever()
    # app.run(host='0.0.0.0',port=8080,debug=True)
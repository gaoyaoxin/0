import json
import dict as d
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
        print(frame)
        if frame:
            request = json.loads(frame)
            retval = getattr(d, request['api'])(**request['args'])
            ws.send(json.dumps({
                'status': 200,
                'retval': retval,
            }))


if __name__ == '__main__':
    server = pywsgi.WSGIServer(('0.0.0.0', 8081), app, handler_class=WebSocketHandler)
    server.serve_forever()
    # app.run(host='0.0.0.0',port=8080,debug=True)
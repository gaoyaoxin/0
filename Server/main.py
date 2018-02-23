from flask import Flask
from flask_json import FlaskJSON,JsonError,json_response,as_json
from flask_sockets import Sockets
from dict import Dict
import logging
import json



d=Dict()
app=Flask(__name__)
sockets=Sockets(app)
# json=FlaskJSON(app)



@app.route('/')
def index():
    return '/'


@sockets.route('/ws')
def websocket_dispatch(ws):
    while not ws.closed:
        frame=ws.receive()
        print(frame)
        if frame:
            request=json.loads(frame)
            retval=getattr(d,request['api'])(**request['args'])
            ws.send(json.dumps({'status':200,'retval':retval}))



if __name__ == '__main__':
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 8081), app, handler_class=WebSocketHandler)
    server.serve_forever()
    # app.run(host='0.0.0.0',port=8080,debug=True)
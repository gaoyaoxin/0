from flask import Flask
from flask_json import FlaskJSON,JsonError,json_response,as_json

from dict import Dict

d=Dict()
app=Flask(__name__)
json=FlaskJSON(app)

@app.route('/',methods=['GET'])
def root():
    return '/'




@app.route('/search',methods=['GET'])
@as_json
def search():
    return d.search('だく')[:20]

@app.route('/recognize',methods=['GET','POST'])
@as_json
def recognize():
    return [1,2,3,4]

@app.route('/test',methods=['GET','POST'])
@as_json
def test():
    return {'key':'中文'}

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080,debug=True)
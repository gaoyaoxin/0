from pymongo import MongoClient
from furigana.furigana import get_html

client = MongoClient()
db = client['0']['scripts']
scripts = db.find()

resp_cache = {}

def get_script(index=0):
    if index in resp_cache: return 200, resp_cache[index]
    script = scripts[index]
    lines = script['lines']
    resp = {
        'index': index,
        'name': script['name'],
        'characters': script['characters'],
        'lines': [{
            'text': line,
            'html': get_html(line)
        } for line in lines]
    }
    resp_cache[index] = resp
    return 200, resp

def REPL():
    get_script()
    

import glob

from furigana.furigana import get_html

scripts = [path.replace('\\','/') for path in glob.glob('E:/ACGN/WHITE ALBUM 2/scripts/jp/*')]

scripts_cache = {}

def get_script(index=0):
    if index in scripts_cache: return 200, scripts_cache[index]
    with open(scripts[index], 'r', encoding='utf-8') as f:
        text = f.read()
    sentences = text.splitlines()
    scripts_cache[index] = script = {
        'index': index,
        'file': scripts[index],
        'sentences': [{
            'text': sentence,
            'html': get_html(sentence)
        } for sentence in sentences]
    }
    return 200, script

def REPL():
    get_script()
    

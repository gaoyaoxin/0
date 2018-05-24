import pickle

with open('./data/novel.pkl', 'rb') as f:
    data = pickle.load(f)


def get_chapter(index=0):
    return 200, {
        'index': index,
        'content': data[index]
    }

def REPL():
    pass

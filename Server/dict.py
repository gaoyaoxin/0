import pickle,re

with open('./data/講談社日中辞典/items.pkl','rb',buffering=2**20*40) as f:
    jp_items=pickle.load(f)
# Oxford Advanced Learner's English-Chinese Dictionary 牛津高阶英汉双解词典 （第8版）
with open('./data/牛津高阶英汉双解词典（第8版）/items.pkl','rb',buffering=2**20*40) as f:
    en_items=pickle.load(f)

def search(search_text:str)->list:
    if re.match(r'[0-9a-zA-Z\.\* ]*',search_text):
        return search_en(search_text)
    else:
        return search_jp(search_text)

def search_jp(search_text:str)->list:
    pattern=re.compile(search_text)
    def resolve(item):
        if item['content'][0].startswith('@@@LINK='):
            real_title=item['content'][0].replace('@@@LINK=','')
            for x in jp_items:
                if item['content'][0]==real_title:
                    return x
        else:
            return item
    result=[item for item in jp_items if pattern.match(item['index'])][:20]
    return [resolve(item) for item in result]

def search_en(search_text:str)->list:
    pattern=re.compile(search_text)
    return [item for item in en_items if pattern.match(item['index'])][:20]


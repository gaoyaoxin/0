import re

items = []
jp_items = []
en_items = []
item = items[0]

# save/load items
import pickle
with open('./data/講談社日中辞典/items.pkl','wb') as f:
    pickle.dump(items,f)
with open('./data/講談社日中辞典/items.pkl','rb') as f:
    items=pickle.load(f)
with open('./data/牛津高阶英汉双解词典（第8版）/items.pkl','wb',buffering=2**20*40) as f:
    pickle.dump(items,f)
with open('./data/牛津高阶英汉双解词典（第8版）/items.pkl','rb',buffering=2**20*40) as f:
    items=pickle.load(f)

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


special_cases=[item for item in items if not item['content'][0].startswith('<link rel="stylesheet" type="text/css" href="O8C.css">')]
item['content'][0]
s='<link rel="stylesheet" type="text/css" href="O8C.css"><span class="id">$100, £50, etc. a ˈthrow</span>'
s='<link rel="stylesheet" type="text/css" href="O8C.css">'
for item in items:
    item['content'][0]=re.sub('<link rel="stylesheet" type="text/css" href="O8C.css">(.*)',r'\1',item['content'][0])
    

import os
os.listdir()
os.getcwd()


import base64
os.getcwd()
with open("./data/apple.jpg", "rb") as image_file:
    img_base64 = base64.b64encode(image_file.read())


items=en_items

item=search_en('apple')[0]
item=search_en('enumerate')[0]

for item in items:
    for i,s in enumerate(item['content']):
        item['content'][i]=re.sub('','',s)

s='        <img src="/pic/fruit_comp.jpg" alt="/pic/fruit_comp.jpg" height="540" width="720" style="display:none;" onclick="this.style.display=&apos;none&apos;;this.nextSibling.nextSibling.style.display=&apos;block&apos;;"/>'


def embed_base64_img(m):
    with open(f'data/牛津高阶英汉双解词典（第8版）/data/{m.group(1)}/{m.group(2)}.{m.group(3)}','rb') as f:
        base64_str=base64.b64encode(f.read()).decode('utf-8')
    return f'data:image/{m.group(3)};base64,{base64_str}'
re.sub(r'(?<=<img src=")/(symbols|pic|thumb|uk|us)/(.+?)\.(.+?)(?=")', embed_base64_img, s)

s='            <a href="entry://Adam&apos;s apple">Adam\'s apple</a>'

stop=False
for item in items:
    for i,s in enumerate(item['content']):
        re.sub(r'(?<=src=")u([k|s])_pron\.png(?=")', r'/symbols/u\1_pron.png', s)
    if stop: break
    
for item in items:
    for i,s in enumerate(item['content']):
        item['content'][i]=re.sub(r'(?<=src=")u([k|s])_pron\.png(?=")', r'/symbols/u\1_pron.png', s)


s='<img src="/symbols/xsym.png"/>'
s='src="uk_pron.png"'

s='        <a type="sound" topic="a/app/apple/apple_pie_1_gb_1.spx" resource="uk_pron" backup-class="Media" class="fayin" href="sound://uk/apple_pie_1_gb_1.spx"><img src="uk_pron.png" class="fayin"/></a>'
search('apple')
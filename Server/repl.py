import re

# import mdict.mdx src file
with open('./data/牛津高阶英汉双解词典（第8版）/items.txt','r',encoding='utf-8',buffering=2**20*40) as f:
    text=f.read()
text[:1000]
text[-2000:].split('</>\n')
def parse_item(item:str):
    lines=item.split('\n')
    if len(lines)<2: print(lines)
    return {
        'index':lines[0],
        'content':lines[1:]
    }
items=[parse_item(item) for item in text.split('</>\n')]
len(items)
items[-1]['content'][-1]=''



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


# content line <-> html
def content2html(item):
    item['content']='\n'.join(item['content'])
for item in items:
    content2html(item)
    
def content2lines(item):
    item['content']=item['content'].split('\n')
for item in items:
    content2lines(item)


# export mdict src.txt
items_str=''.join(['\n'.join([item['index'],item['title']]+item['content'][:-1])+'\n</>\n' for item in items])
items_str=items_str[:-4]+'</>'
with open('D:/dict-out.txt','w',encoding='utf-8',buffering=30*1024*1024) as f:
    f.write(items_str)
items_str[-10:]
item=items[0]



def search(search_text:str)->list:
    pattern_reg=re.compile(search_text)
    def resolve(item):
        # if item['title'].startswith('@@@LINK='):
        #     real_title=item['title'].replace('@@@LINK=','')
        #     for x in items:
        #         if x['title']==real_title:
        #             return x
        # else:
        return item
    result=[item for item in items if pattern_reg.match(item['index'])][:17]
    return [resolve(item) for item in result]
results=search('あげる【上げる・挙げる・揚げる】')
item=results[0]
item['title']
print(item['content'])
items[-3]


items[:3]

special_cases=[item for item in items if not item['content'][0].startswith('<link rel="stylesheet" type="text/css" href="O8C.css">')]
item['content'][0]
s='<link rel="stylesheet" type="text/css" href="O8C.css"><span class="id">$100, £50, etc. a ˈthrow</span>'
s='<link rel="stylesheet" type="text/css" href="O8C.css">'
for item in items:
    item['content'][0]=re.sub('<link rel="stylesheet" type="text/css" href="O8C.css">(.*)',r'\1',item['content'][0])
    
import os
import dict as d
os.listdir()
os.getcwd()
getattr(os,'getcwd')

import bson
bson.dumps({"A":[1,2,3,4,5,"6", "7", {"C":"DS"}]})

import base64
os.getcwd()
with open("./data/apple.jpg", "rb") as image_file:
    img_base64 = base64.b64encode(image_file.read())


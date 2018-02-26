import pickle,re
import base64

with open('./data/講談社日中辞典/items.pkl','rb',buffering=2**20*40) as f:
    jp_items=pickle.load(f)
# Oxford Advanced Learner's English-Chinese Dictionary 牛津高阶英汉双解词典 （第8版）
with open('./data/牛津高阶英汉双解词典（第8版）/items.pkl','rb',buffering=2**20*40) as f:
    en_items=pickle.load(f)

def search(search_text:str, encode=True)->list:
    pattern=re.compile(search_text)
    if re.match(r'^[0-9a-zA-Z\.\* ]+$',search_text):
        results=[item for item in en_items if pattern.match(item['index'])][:20]
        if not encode: return results
        def embed_base64_img(m):
            with open(f'data/牛津高阶英汉双解词典（第8版）/data/{m.group(1)}/{m.group(2)}.{m.group(3)}','rb') as f:
                base64_str=base64.b64encode(f.read()).decode('utf-8')
            return f'data:image/{m.group(3)};base64,{base64_str}'
        return [{'index':item['index'], 'type':'en/OLAD' , 'content': [re.sub(r'(?<=src=")/(symbols|pic|thumb|uk|us)/(.+?)\.(.+?)(?=")', embed_base64_img, s) for s in item['content']]} for item in results]
    else:
        def render_item(item):
            if item['content'][0].startswith('@@@LINK='):
                real_title=item['content'][0].replace('@@@LINK=','')
                for x in jp_items:
                    if item['content'][0]==real_title:
                        item=x
                        break
            return {'index':item['index'], 'type':'jp/JTSRZ', 'content':item['content']}
        results=[item for item in jp_items if pattern.match(item['index'])][:20]
        return [render_item(item) for item in results]


    
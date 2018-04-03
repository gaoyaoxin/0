import base64
import pickle
import re
from ctypes import *

with open('./data/JTS/items.pkl','rb',buffering=2**20*40) as f:
    jp_items=pickle.load(f)
# Oxford Advanced Learner's English-Chinese Dictionary 牛津高阶英汉双解词典 （第8版）
with open('./data/OALD/items.pkl','rb',buffering=2**20*40) as f:
    en_items=pickle.load(f)


speex_decoder = CDLL('./lib/speexdec.dll')
speexdec = speex_decoder.speexdec
speexdec.argtypes=[c_char_p, c_int, c_char_p]
wav=create_string_buffer(2**20)


def search(search_text:str, is_load_assets=True)->list:
    search_text = search_text.strip()
    pattern = re.compile(search_text, re.IGNORECASE)
    if all(ord(c) < 128 for c in search_text):
        results = [item for item in en_items if pattern.match(item['index'])][:30]
        if not is_load_assets: return results
        def load_assets(item):
            assets={}
            for s in item['content']:
                # 加载、编码图片，加入 assets
                m = re.match(r'.*src="/(symbols|pic|thumb)/(.+?)\.(.+?)"', s)
                if m:
                    asset_key=f'{m.group(1)}/{m.group(2)}.{m.group(3)}'
                    if asset_key not in assets.keys():
                        try:
                            with open(f'data/OALD/data/{asset_key}', 'rb') as f:
                                assets[asset_key] = base64.b64encode(f.read()).decode('utf-8')
                        except FileNotFoundError: pass
                # 加载、编解码发音（只要美音），加入 assets
                m = re.match(r'.*"sound://(us/.*?)"',s)
                if m:
                    asset_key = m.group(1)
                    if asset_key not in assets.keys():
                        try:
                            with open(f'data/OALD/data/{asset_key}', 'rb') as f:
                                ogg = f.read()
                            wav_len = speexdec(ogg, len(ogg), wav)
                            base64_wav = base64.b64encode(wav[:wav_len]).decode('utf-8')
                            assets[asset_key] = base64_wav
                        except FileNotFoundError: pass
            return assets

        def craw_origin(index, item):
            # if index>0: return
            # word = item['index']
            # resp = requests.get(f'http://www.dicts.cn/dict/dict/dict!searchhtml4.asp?id={word}').text
            # resp_ = requests.get(f'http://www.dicts.cn/{resp[1:-1]}')
            # html = resp_.content.decode('utf-8')
            # soup = BeautifulSoup(html, 'lxml')
            # return str(soup.find(id='cigencizui-content'))
            pass
            
        return [{
            'index'   : item['index'], 
            'type'    : 'en/OALD',
            'content' : item['content'],
            'word_root': item.get('word_root'),
            'assets'  : load_assets(item),
            # 'origin'  : craw_origin(i, item)
        } for i,item in enumerate(results)]
    else:
        def render_item(item):
            if item['content'][0].startswith('@@@LINK='):
                real_title=item['content'][0].replace('@@@LINK=','')
                for real_item in jp_items:
                    if real_item['index']==real_title:
                        item=real_item
                        break
            return {'index':item['index'], 'type':'jp/JTS', 'content':item['content']}
        results=[item for item in jp_items if pattern.match(item['index'])][:30]
        return [render_item(item) for item in results]


    
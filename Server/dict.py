import base64
import re
from typing import Tuple

from pymongo import MongoClient

client       = MongoClient()
db           = client['iDict']
en           = db['en'] # Oxford Advanced Learner's English-Chinese Dictionary 牛津高阶英汉双解词典 （第8版）
en_proncs    = db['en_proncs']
jp           = db['jp']

assets_cache = {}

def b64encstr(bytes_:bytes)->str:
    return base64.b64encode(bytes_).decode('utf-8')

def search(search_text:str, is_load_assets=True) -> Tuple[int,list]:
    search_text = search_text.strip()
    if all(ord(c) < 128 for c in search_text): # 英语单词
        results = [item for item in en.find({'index':{'$regex':'^'+search_text, '$options':'i'}}, limit=30, batch_size=30)]
        if not is_load_assets: return 200, results
        def load_assets(item):
            assets = {}
            for s in item['content'].split('\n'):
                # 加载、编码图片，加入 assets
                m = re.match(r'.*src="/(symbols|pic|thumb)/(.+?)\.(.+?)"', s)
                if m:
                    asset_key=f'{m.group(1)}/{m.group(2)}.{m.group(3)}'
                    if asset_key in assets_cache:
                        assets[asset_key] = assets_cache[asset_key]
                    if asset_key not in assets.keys():
                        try:
                            with open(f'data/OALD/data/{asset_key}', 'rb') as f:
                                assets_cache[asset_key] = assets[asset_key] = b64encstr(f.read())
                        except FileNotFoundError: pass
            # 加载发音（美音），加入 assets
            for pronc in item['proncs']:
                assets[f'proncs/{pronc}.spx'] = b64encstr(en_proncs.find_one({'index': pronc})['spx'])
            return assets
        return 200, [{
            'index'    : item['index'], 
            'type'     : 'en/OALD',
            'content'  : item['content'],
            'word_root': item.get('word_root'),
            'assets'   : load_assets(item),
        } for item in results]
    else: # 日语单词
        results = [item for item in jp.find({'index':{'$regex':'^'+search_text, '$options':'i'}}, limit=30, batch_size=30)]
        if not results:
            results = [item for item in jp.find({'index':{'$regex':search_text, '$options':'i'}}, limit=30, batch_size=30)]
        def render_item(item):
            first_line = item['content'].split('\n')[0]
            if first_line.startswith('@@@LINK='):
                real_index = first_line.replace('@@@LINK=','')
                item       = jp.find_one({'index':real_index})
            return {
                'index'   : item['index'],
                'type'    : 'jp/JTS',
                'content' : item['content']}
        return 200, [render_item(item) for item in results]



import pickle,re

class Dict:
    def __init__(self):
        with open('./Data/jp-dict-items.pkl','rb') as f:
            self.items=pickle.load(f)
    
    # 查询单词
    def search(self, search_text:str)->list:
        pattern_reg=re.compile(search_text)
        def resolve(item):
            if item['title'].startswith('@@@LINK='):
                real_title=item['title'].replace('@@@LINK=','')
                for x in self.items:
                    if x['title']==real_title:
                        return x
            else:
                return item
        result=[item for item in self.items if pattern_reg.match(item['index'])][:17]
        return [resolve(item) for item in result]
    
    
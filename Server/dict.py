import pickle,re

class Dict:
    def __init__(self):
        with open('./Data/jp-dict-items.pkl','rb') as f:
            self.items=pickle.load(f)
    
    # 查询单词
    def search(self, input_str:str)->list:
        pattern=input_str.replace('?','.').replace('*','.*')+'.*'
        pattern_reg=re.compile(pattern)
        return [item for item in self.items if pattern_reg.match(item['index'])][:20]
    

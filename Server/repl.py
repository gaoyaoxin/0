import re

# import mdict.mdx src file
with open('D:/講談社日中 mdx src.txt','r',encoding='utf-8') as f:
    text=f.read()
with open('D:/dict-out-0.1.txt','r',encoding='utf-8') as f:
    text=f.read()
with open('D:/dict-model.txt','r',encoding='utf-8') as f:
    text=f.read()

def parse_item(item:str):
    lines=item.split('\n')
    if len(lines)<3: print(lines)
    item={
        'index':lines[0],
        'title':lines[1],
        'content':lines[2:]
    }
    return item
items=[parse_item(item) for item in text.split('</>\n')]



# save/load items
import pickle
with open('./Data/jp-dict-items.pkl','wb') as f:
    pickle.dump(items,f)
with open('./Data/jp-dict-items.pkl','rb') as f:
    items=pickle.load(f)



# 提取单词，删去拼音，修改格式
s='回礼 huílǐ；回赠礼品 huízèng lǐpǐn．（物）回礼 huílǐ．<br>'
for item in items:
    status='notyet' # notyet/first/second | notyet->first, notyet->notyet, first->second, second->first, second->notyet
    to_remove=[]
    content=item['content']
    for i,s in enumerate(content):
        m=re.match('<span class="word">(.*?)</span><br>',s)
        if status=='notyet':
            if m:
                content[i]=f'<div class="words"><p class="word"><span class="word-jp">{m[1]}</span>／'
                status='first'
        elif status=='first':
            to_remove.append(s)
            cnt=len(re.findall('．',s))
            if cnt>1:
                s=re.sub('．','；',s,cnt-1)
            content[i-1]+=f'''<span class="word-cn">{'、'.join(p.split(' ')[0] for p in s[:-5].split('；'))}</span></p>'''
            status='second'
        elif status=='second':
            if m:
                content[i]=f'<p class="word"><span class="word-jp">{m[1]}</span>／'
                status='first'
            else:
                content[i-2]+=f'</div>'
                status='notyet'
    item['content']=[x for x in item['content'] if x not in to_remove]
    
re.match('<span class="word">(.*?)</span><br>','<span class="word">外交━━</span><br>')[1]
'、'.join(p.split(' ')[0] for p in '外勤 wàiqín；跑街 pǎojiē．<br>'[:-5].split('；'))+'外勤 wàiqín；跑街 pǎojiē．<br>'[-5:-4]



# 中文例句翻译去拼音
def eg_rm_py(m):
    return '<span class="eg-cn">'+'／'.join(p.split(' ')[0] for p in m[1].split('／'))+'</span>'

for item in items:
    item['content']=[re.sub('<span class="eg-cn">(.*?)</span>',eg_rm_py,s) for s in item['content']]
    
s='<div class=“egs"><span class="eg-jp">～いご飯</span>／<span class="eg-cn">热饭 rèfàn／热乎乎的米饭 rèhūhū de mǐfàn．</span><br>'
s='<span class="eg-jp">～半分の気持ちでボランティア活動に参加する</span>／<span class="eg-cn">带着一半去玩儿的心情参加志愿者活动 dàizhe yíbàn qù wánr de xīnqíng cānjiā zhìyuànzhě huódong．</span><br>'
re.sub('<span class="eg-cn">(.*?)</span>',eg_rm_py,s)
item=items[0]



# 中文解释去拼音
def exp_rm_py(m):
    g4=m.group(4)
    cnt=len(re.findall('．',g4))
    if cnt>1:
        g4=re.sub('．','；',g4,cnt-1)
    if g4.find('；')==-1 and len(re.findall('？',g4))>1: print(g4)
    return '<p class="exp">'+m.group(2)+m.group(3)+' '+'、'.join(p.split(' ')[0] for p in g4.split('；'))+'</p>'

for item in items:
    if len(item['content'])>1:
        contents=item['content']
        if contents[0].startswith('<'):
            continue
        if not contents[0].startswith('①'):
            contents[0]='① '+contents[0]
        for i,s in enumerate(contents):
            contents[i]=re.sub('(([①-⑳]|<b>[2-3][0-9]</b> )(.*?)? )(.*)',exp_rm_py,s)

s='①（遊ぶこと） 玩儿 wánr．（気ばらし）消遣 xiāoqiǎn．（遊戯・ゲーム）游戏 yóuxì．'
s='<b>22</b> （脱ぐ・はずす） 摘下 zhāi//xia；摘掉 zhāi//diào；脱 tuō．'
s='<b>37</b> （遊びや競技などを行う） 做（游戏或体育比赛等）动作 zuò （yóuxì huò tǐyù bǐsài děng） dòngzuò；玩 wán．'
s='①（内から外へ行く・出発する） 出 chū；出去 chū//qu；出发 chūfā．'
s='①（サングラス） 有色眼镜 yǒusè yǎnjìng；墨镜 mòjìng．<br>'
re.sub('(([①-⑳]|<b>[2-3][0-9]</b> )(.*?)? )(.*)',exp_rm_py,s)
re.match('(([①-⑳]|<b>[2-3][0-9]</b> )(.*?)? )(.*)',s).groups()
# re.match('(([①-⑳]|<b>[2-3][0-9]</b> )(.*?)? )(.*)',s).group(3)



# export
items_str=''.join(['\n'.join([item['index'],item['title']]+item['content'][:-1])+'\n</>\n' for item in items])
items_str=items_str[:-4]+'</>'
with open('D:/dict-out.txt','w',encoding='utf-8',buffering=30*1024*1024) as f:
    f.write(items_str)

items_str[-10:]
item=items[0]


# todo: <b>［シソーラス］</b>あたたかい<br> 相反的 eg-cn/eg-jp 拼音



# 查询单词
def search(input_str:str)->list:
    pattern=input_str.replace('?','.').replace('*','.*')+'.*'
    pattern_reg=re.compile(pattern)
    return [item for item in items if pattern_reg.match(item['index'])]


# content line <-> html
def content2html(item):
    item['content']='\n'.join(item['content'])
for item in items:
    content2html(item)
    
def content2lines(item):
    item['content']=item['content'].split('\n')
for item in items:
    content2lines(item)
    
items[2000]
search('あたたかい')
item=items[1101]
print(item['content'])
item['content'][-10:]



# add id for items
for i,item in enumerate(items):
    item['id']=i
    


# シソーラス 拼音消去 synonym
'<b>［シソーラス］</b>'
s='【暖】nuǎn （気候や環境が）あたたかい．'
s='【其间】qíjiān<br>'
s='【之间】zhī jiān （両者の間を表す）…の間．'
s='【空】kòng 空である．あいている．使われていない．'
for item in items:
    for i,s in enumerate(item['content']):
        m=re.match('^(【.*】).*( |<br>)(.*)',s)
        if m:
            if m[3].endswith('．'):
                m3=m[3][:-1]
            else:
                m3=m[3]
            m3=m3.replace('．','、')
            item['content'][i]=f'<p class="synonym">{m[1]} {m3}</p>'
s[:-1]
item


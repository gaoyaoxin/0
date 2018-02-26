import re
items=[]

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



# class="item-title"
for item in items:
    item['title']=item['title'].replace('<h1 class="item-title">','').replace('</h1>','')
items[50]['title']
s='abcd'
s.replace('ab','cd')


# ［シソーラス］中日例句互换，去掉句号
for item in items:
    synonym=False
    for i,s in enumerate(item['content']):
        if re.match('.*［シソーラス］.*',s):
            synonym=True
        if synonym:
            item['content'][i]=re.sub('(.*)．</span>／<span class="eg-cn">(.*)',r'\1</span>／<span class="eg-cn">\2',s)
s='<span class="eg-jp">もろ手をあげて賛成する．</span>／<span class="eg-cn">～双手赞成</span><br>'
s='<div class="egs"><span class="eg-jp">杯をあげる．</span>／<span class="eg-cn">～杯</span><br>'
re.sub('(.*)．</span>／<span class="eg-cn">(.*)',r'\1</span>／<span class="eg-cn">\2',s)
item



# iDict

一个简洁、智能、美观的词典。

前端基于Vue、后端基于Flask，使用Websocket通信。

## 预览

![2](preview/2.png?raw=true)

![1](preview/1.png?raw=true)

## 词典

牛津高阶英汉双解词典（第８版）（词条数 92667）

講談社日中辞典 （词条数 85958）

## 功能

在Web浏览器中显示搜索结果，可通过修改CSS样式修改词条的显示效果

正则表达式搜索词条

前进、后退

## 快捷键（全程无需鼠标）

### 全局

Esc 聚焦输入框并清空

#### 焦点位于输入框

Enter 查询单词（正则表达式）

#### 焦点不位于输入框

Tab/Shift+Tab 上下移动条目

E 聚焦输入框编辑查询内容（不清空）

F 或 S 聚焦输入框输入查询内容（清空）

j/J 向下滚动／直达底部

k/K 向上滚动／直达顶部

h 后退，转到上一个历史查询词条

l 前进，转到下一个历史查询词条

## Build Setup

``` bash
# 运行服务器
cd ./Server
pip install flask flask_sockets base64 gevent geventwebsocket
python ./main.py

# 运行前端
cd ./Web

# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report
```



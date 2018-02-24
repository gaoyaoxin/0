<template lang="pug">
    el-container#dict
        el-header#header
            search-bar(ref='search_bar')
        el-container#body
            el-aside#sidebar(ref='sidebar' tabindex='1')
                #item-list
                    .item(v-for='item in items')
                        h6.item-index(@click='select_item(item)') {{item.index}}
            el-main#content(ref='content' tabindex='2')
                h1#item-title(v-if='item' v-html='item.title')
                #item-content(v-if='item' v-html='item.content')
</template>
    

<script lang="coffee">
    import SearchBar from './SearchBar.vue'
    export default
        data: ->
            items:[]
            item:null
            search_bar:null
            sidebar:null
            content:null
        components:{SearchBar}
        methods:
            select_item:(item)->
                this.item=item
                history.replaceState(null,'',"##{dict.search_bar.search_text},#{dict.item.i}")
            # 切换至 上一条目/下一条目
            next_item:()->
                this.sidebar.$el.focus()
                this.select_item(this.items[this.item.i+1]) if this.item?.i+1<this.items.length
            previous_item:()->
                this.sidebar.$el.focus()
                this.select_item(this.items[this.item.i-1]) if this.item?.i-1>=0
            select_item_i:(i)->
                this.sidebar.$el.focus()
                this.select_item(dict.items[i]) if 0<=i<dict.items.length
        
        mounted: ->
            window.dict = this
            sidebar     = this.sidebar    = this.$refs.sidebar
            search_bar  = this.search_bar = this.$refs.search_bar
            content     = this.content    = this.$refs.content
            
            dict.search_results = {} # 搜索结果缓存
            
            window.websocket_connect=->
                if !window.ws || Date.now()-ws.last_connected>1000*5
                    console.log 'try sconnecting to the server'
                    window.ws=new WebSocket 'ws://localhost:8081/ws'
                    ws.last_connected=new Date()
                    ws.onopen=(event)->
                        console.log 'websocket connected with server'
                    ws.onmessage=(event)->
                        response=JSON.parse(event.data)
                        console.log response
                        response.retval.forEach (x,i)-> x.i=i # 加入 index
                        dict.search_results[search_bar.search_text]=dict.items=response.retval
                        if dict.items
                            dict.item=dict.items[0]
                        search_bar.blur()
                        dict.sidebar.$el.focus()
                    ws.onerror=(event)->
                        console.log 'websocket error'
                        setTimeout websocket_connect, 2000
                    ws.onclose=(event)->
                        console.log 'websocket closed'
                        setTimeout websocket_connect, 2000
                else
                    console.error 'disconnected with the server'
            websocket_connect()
            
            
            
            document.onkeydown=(event)->
                key=event.key
                
                if event.target==search_bar.input_el
                    null
                if event.target!=search_bar.input_el
                    if !isNaN(key)
                        dict.select_item_i(key-1)
                        event.preventDefault()
                    if key=='s' || key=='f'
                        search_bar.clear()
                        search_bar.focus()
                        event.preventDefault()
                    if key=='e'
                        search_bar.focus()
                        event.preventDefault()
                    if key=='j'
                        content.$el.focus()
                        content.$el.scrollTop+=80
                        event.preventDefault()
                    if key=='J'
                        content.$el.focus()
                        content.$el.scrollTop=1e5
                        event.preventDefault()
                    if key=='k'
                        content.$el.focus()
                        content.$el.scrollTop-=80
                        event.preventDefault()
                    if key=='K'
                        content.$el.focus()
                        content.$el.scrollTop=0
                        event.preventDefault()
                    if key=='h'
                        history.go(-1)
                        event.preventDefault()
                    if key=='l'
                        history.go(1)
                        event.preventDefault()
                
                if key=='Escape'
                    event.preventDefault()
                    search_bar.clear()
                    search_bar.focus()
                if !event.shiftKey && key=='Tab'
                    dict.next_item()
                    event.preventDefault()
                if event.shiftKey && key=='Tab'
                    dict.previous_item()
                    event.preventDefault()
                            
    
            # 后退，状态加载
            window.addEventListener 'hashchange',(event)->
                parts=event.newURL.split('#')
                if parts?[1]
                    parts=parts[1].split(',')
                    parts[0]=decodeURI(parts[0])
                    dict.search_text=parts[0]
                    dict.items=dict.search_results[parts[0]]
                    if dict.items
                        dict.item=dict.items[parts[1]]
</script>


<style lang="stylus">
    #dict
        width 97%
        margin auto
        #header
            padding unset
            #search-bar
                margin-top 20px
                .el-icon-search
                    font-size 1.7em
        #body
            #sidebar
                min-width: 300px;
                height 600px
                border-right 1px solid #eeeeee
                border-left 1px solid #eeeeee
                padding-left 1em
                h6.item-index 
                    font-weight normal
                    font-size 1em
                    padding-top 1em
                    margin-top unset
                    margin-bottom unset
                    cursor pointer
            #content
                height 600px
                line-height 1.5em
                padding-top 30px
                border-right 1px solid #eeeeee
                font-size 1.3em
                #item-title
                    line-height 1em
                    font-size 60px
                    font-weight normal
                    margin-top 0
                    margin-bottom 40px
                    word-break keep-all
                    word-wrap break-word
                .exp
                    margin-top 0
                    margin-bottom 0
                    color #0070C0
                .egs
                    margin-bottom 1em
</style>

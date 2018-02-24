<template lang="pug">
    el-container#dict
        el-header#header
            search-bar(ref='search_bar')
        el-container#body
            el-aside#sidebar(ref='sidebar' tabindex='1')
                #item-list
                    .item(v-for='item in items')
                        h6.item-index(@click='select_item(item)') {{item.index}}
            el-main#content
                h1#item-title(v-if='item' v-html='item.title')
                #item-content(v-if='item' v-html='item.content')
</template>
    

<script lang="coffee">
    import SearchBar from './SearchBar.vue'
    export default
        data: ->
            items:[]
            item:null
        methods:
            select_item:(item)->
                this.item=item
        components:{SearchBar}
        mounted: ->
            window.dict=this
            sidebar=this.sidebar=this.$refs.sidebar
            search_bar=this.search_bar=this.$refs.search_bar
            
            # init search results cache
            dict.search_results={}
            
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
                        dict.search_bar.search_input_el.blur()
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
                    
                    
                    
            # handle sidebar key events
            sidebar.$el.addEventListener 'keydown',(event)->
                key=event.key
                console.log key
                search_input=search_bar.search_input
            #    debugger
                switch true
                    # Navigate
                    when !event.shiftKey && key=='Tab'
                        dict.item=dict.items[dict.item.i+1] if dict.item?.i+1<dict.items.length
                        event.preventDefault()
                    when event.shiftKey && key=='Tab'
                        dict.item=dict.items[dict.item.i-1] if dict.item?.i-1>=0
                        event.preventDefault()
                    when !isNaN(key)
                        dict.item=dict.items[key-1] if 0<=key-1<dict.items.length
                    # Focus search input
                    when key=='s' || key=='f'
                        event.preventDefault()
                        search_bar.search_input_el.value=''
                        search_bar.search_input_el.focus()
                    when key=='e'
                        event.preventDefault()
                        search_bar.search_input_el.focus()
            
            # handle global(dict) key events
            document.addEventListener 'keydown',(event)->
                key=event.key
                switch true
                    when key=='Escape'
                        event.preventDefault()
                        search_bar.search_input_el.value=''
                        search_bar.search_input_el.focus()
                    when key=='Tab'
                        event.preventDefault()
                        sidebar.$el.focus()
    
    
    
            # history management
            window.addEventListener 'hashchange',(event)->
                parts=event.newURL.split('#')
                if parts?[1]
                    dict.items=dict.search_results[decodeURI(parts[1])]
                    if dict.items
                        dict.item=dict.items[0]
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

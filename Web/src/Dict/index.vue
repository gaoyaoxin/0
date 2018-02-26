<template lang="pug">
    el-container#dict
        el-header#header
            search-bar(ref='search_bar')
        el-container#body
            el-aside#sidebar(ref='sidebar' tabindex='1' width='250px')
                #item-list
                    .item(v-for='item in items')
                        h6.item-index(@click='select_item(item)')
                            span.i {{item.i+1<=9?(item.i+1+' '):'&nbsp;'}}
                            | {{item.index}}
            el-main#content(ref='content' tabindex='2')
                h1#item-title(v-if='item' v-html='item.title')
                #item-content(v-if='item' v-html="item.content.join('\\n')")
</template>
    

<script lang="coffee">
import SearchBar from './SearchBar'
export default
    data      : ->
        items     : []
        item      : null
        search_bar: null
        sidebar   : null
        content   : null
    components: {SearchBar}
    methods   :
        select_item  : (item)->
            this.item = item
            history.replaceState(null, '', "##{dict.search_bar.search_text},#{dict.item.i}")
        # 切换至 上一条目/下一条目
        next_item    : ->
            this.sidebar.$el.focus()
            this.select_item(this.items[this.item.i+1]) if this.item?.i+1<this.items.length
        previous_item: ->
            this.sidebar.$el.focus()
            this.select_item(this.items[this.item.i-1]) if this.item?.i-1>=0
        select_item_i: (i)->
            this.sidebar.$el.focus()
            this.select_item(dict.items[i]) if 0<=i<dict.items.length
    
    mounted  : ->
        window.dict = this
        sidebar     = this.sidebar    = this.$refs.sidebar
        search_bar  = this.search_bar = this.$refs.search_bar
        content     = this.content    = this.$refs.content
        
        dict.search_results = {} # 搜索结果缓存
        
        window.websocket_connect=->
            if !window.ws || Date.now()-ws.last_connected>1000*5
                console.log 'try sconnecting to the server'
                window.ws         = new WebSocket 'ws://localhost:8081/ws'
                ws.last_connected = new Date()
                ws.onopen    = (event)->
                    console.log 'websocket connected with server'
                ws.onmessage = (event)->
                    response = JSON.parse(event.data)
                    console.log response
                    response.retval.forEach (x, i)-> x.i = i # 加入 index
                    dict.search_results[search_bar.search_text] = dict.items = response.retval
                    if dict.items
                        dict.item = dict.items[0]
                    search_bar.blur()
                    dict.sidebar.$el.focus()
                ws.onerror = (event)->
                    console.log 'websocket error'
                    setTimeout websocket_connect, 2000
                ws.onclose = (event)->
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
                    font-size 1.7rem
        #body
            #sidebar
                min-width 250px
                height 600px
                border-right 1px solid #eeeeee
                border-left 1px solid #eeeeee
                padding-left 0.5rem
                h6.item-index 
                    font-weight normal
                    font-size 1rem
                    padding-top 1rem
                    margin-top unset
                    margin-bottom unset
                    cursor pointer
                    .i
                        color:#757575
            #content
                height 600px
                line-height 1.5rem
                padding-top 15px
                border-right 1px solid #eeeeee
                font-size 1.3rem
                #item-title
                    line-height 4rem
                    font-size 4rem
                    font-weight normal
                    margin-top 0
                    margin-bottom 15px
                    word-break keep-all
                    word-wrap break-word
                /* 讲谈社日中 */
                .exp
                    margin-top 0
                    margin-bottom 0
                    color #0063b4
                    line-height 2rem
                .egs
                    margin-bottom 1rem
                    font-size 1.1rem
                /* 牛津高阶OLAD */
                .fayin
                    display inline
                
                img
                    border 0
                    max-width 700px
                    &.fayin
                        width 15px
                        height 15px
                    &.img
                        width 1em
                        height 1em
                        margin-left -4px
                        margin-bottom -2px
                    &.Media
                        clear both
                
                .h-g
                    .top-g
                        .h
                            font-weight bold
                            color blue
                        .vs-g
                            .v
                                font-weight bold
                
                .id-g
                    display inline

                
                .revout + .id-g, .z + .pv-g
                    display block
                
                .revout
                    display block
                    font-weight bold
                    color red
                    margin-top 15px
                    text-align left
                    &:before
                        content "【"
                        color red
                    &:after
                        content "】"
                        color red
                
                .ids-g
                
                span.arbd1, span.dhb, span.fm, span.unei, .ndv, .cl, .ei, .ndv
                    font-weight bold
                    padding-right 0.2em
                
                span.unsyn, span.unfm, .eb
                    font-weight bold
                    padding-right 0.2em
                    text-transform uppercase
                    font-size smaller
                    color #C76E06
                
                .ungi, .gi, .g
                    color green
                    padding-right 0.2em
                    font-style italic
                
                .label-g
                    color #004AAC
                    .r
                        color green
                    .chn
                        display inline
                        &:before
                            content ""
                
                .dr-g
                    display block
                
                .pos
                    text-align left
                    font-weight bold
                
                .pos-g
                    .pos
                        display table-cell
                        margin 0px auto 0px auto
                        color darkRed
                        font-style italic
                        display block
                        &:before
                            content "◙ "
                            color red
                            font-style normal
                
                .pos-g .z, .pos-g img, .pos-g .symbols-small_coresym
                    display none
                
                .phon-gb, .phon-us
                    color red
                
                .z_phon-us
                    color #8f0610
                    font-style italic
                    margin-right .1em
                
                .alt
                    font-weight bold
                
                .alt[q="also"]
                    display block
                
                .z_a
                    font-weight normal
                    padding-right 5px
                
                .z
                    font-weight normal
                
                .sd
                    display block
                    font-weight bold
                    &:before
                        content "›› "
                    .chn
                        font-weight normal
                
                .cf
                    font-weight bold
                    .swung-dash
                        margin-right .4em
                
                .cf[display="block"]
                    font-weight bold
                    display block
                
                .n-g
                    display block
                
                .z_n
                    font-weight bold
                    &:after
                        content "."
                .x-g
                    display block
                    padding-left 1em
                    img
                        display none
                
                .x
                    color #04F
                    &:before
                        content "» "
                
                .tx
                    display block
                    color #039
                    font-size 90%
                
                .sense-g
                    display block
                
                .pvs-g .z .revout, .ids-g .revout, .xr-g .revout
                
                .pv, .id
                    color blue
                
                .pvs-g, .pv-g, .sense-g, .d
                
                .pvs-g
                
                .xr-g[level="2"]
                
                .xr-g
                
                .Ref
                    font-weight bold
                    color #004AAC
                
                .block-g
                    display block
                    margin-bottom 16px
                
                .ids-g, .pvs-g
                    display block
                
                .id
                    &:before
                        content "◘ "
                        color red
                
                .pracpron
                    display none
                
                .infl
                    display block
                    display none
                    .inflection
                        margin-right .4em
                        font-weight bold
                
                .para
                    display block
                    padding-left 2px
                
                .wordbox
                    display block
                    margin-left 18px
                    margin-right 18px
                    padding 5px 16px
                    border-radius 10px
                    border-color #C76E06
                    border-style ridge
                    clear both
                
                .word
                    display table-cell
                    margin 0px auto 0px auto
                    background-color #C76E06
                    color #FAFAFA
                    font-weight bold
                    text-transform uppercase
                
                .wf-g
                    display block
                    .pos-g
                        display inline
                    .pos
                        display inline
                
                .wfw
                    display inline
                
                .unbox
                    display block
                    padding-left 2px
                
                .tab
                    display table-cell
                    background-color #C76E06
                    color #FAFAFA
                    font-weight bold
                    text-transform uppercase
                    text-align left
                
                .title
                    display block
                    font-weight bold
                    text-transform uppercase
                    font-size small
                
                .collsubhead
                    font-weight bold
                
                .table
                    display table
                    margin 12px 0 8px 0
                
                .tr
                    display table-row
                
                .td
                    display table-cell
                    margin-right 10px
                
                .th
                    display table-cell
                    color #C76E06
                    font-weight bold
                    text-transform uppercase
                
                .althead
                    font-weight bold
                    text-transform uppercase
                
                .patterns
                    display block
                    clear both
                    .althead
                        display table-cell
                        margin 0px auto 0px auto
                        font-weight bold
                        text-transform uppercase
                    .para
                        -ms-word-break break-all
                        word-break break-word
                        -webkit-hyphens auto
                        -moz-hyphens auto
                        hyphens auto
                
                .help
                    display block
                
                .symbols-coresym
                    color green
                    display inline-block
                
                .symbols-small_coresym
                    color green
                    display inline-block
                    font-size 70%
                    top -.1em
                    margin-right .15em
                
                .symbols-xsym
                    display none
                    color rgb(180, 180, 180)
                    font-size 55%
                    top -.25em
                    margin-right .25em
                
                .symbols-xrsym
                    font-style normal
                    color #555555
                    margin-right .25em
                
                .symbols-helpsym, .symbols-synsym, .symbols-awlsym, .symbols-oppsym, .symbols-etymsym, .symbols-notesym
                    color rgb(255, 255, 255)
                    background rgb(183, 128, 50)
                    font-size 65%
                    padding 1px 3px 2px
                    display inline-block
                    margin 0 .4em 0 0
                    text-transform uppercase
                    top -1px
                    line-height 1em
                    border-radius 1px
                
                .symbols-oppsym
                    background darkred
                
                .symbols-drsym
                    font-style normal
                    font-size 70%
                    color rgb(0, 0, 0)
                
                .symbols-para_square
                    color rgb(80, 80, 80)
                    font-size 65%
                    top -.2em
                
                .symbols-synsep
                    color rgb(80, 80, 80)
                    font-size 65%
                    top -.2em
                
                .symbols-xsep
                    display none
                
                .def-g .d .dh, .def-g .d .ndv, .p-g .x-g .x .cl
                    padding-right 0.2em
                    font-weight bold
                
                .z_xr
                
                .unebi
                    font-weight bold
                
                span#wx
                    text-decoration line-through
                
                span#unwx
                    text-decoration line-through
                
                swung-dash
                    visibility hidden
                    &::after
                        visibility visible
                        content "\007E \0020"
                
                .pv-g
                    .swung-dash
                        visibility hidden
                        &::after
                            visibility visible
                            content "\007E \0020"
                
                .pv
                    &:before
                        content "◘ "
                        color red
                
                .d
                    .chn
                        color #FF5000
                        &:before
                            content ""
                
                .def-g
                    padding-left 2px
                    .chn
                        &:before
                            content ""
                
                .chn
                    color #FF5000
                
                .z_ab
                    font-weight normal
                    color green
                    padding-right 0.2em
                
                .ab
                    font-weight bold
                    .z
                        font-weight normal
                
                .gr, .subject
                    color green
                
                .dr
                    font-weight bold
                    color blue
    
                
</style>

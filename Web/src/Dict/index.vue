<template lang="pug">
    el-container#dict
        el-header#header(height='40px')
            search-bar(ref='search_bar')
        el-container#body
            el-aside#sidebar(ref='sidebar' tabindex='1' width='250px')
                #item-list
                    .item(v-for='item in items')
                        h6.item-index(@click='select_item(item)')
                            span.i {{item.i+1<=9?(item.i+1+' '):'&nbsp;'}}
                            | {{item.index}}
            el-main#content(ref='content' v-bind:class='item_type_class' tabindex='2')
                h1#item-title(v-if='item && item.type=="jp/JTS"' v-html='item.index')
                #item-content(v-if='item' v-html="render_item_content(item)", @click='jump($event)')
</template>
    

<script lang="coffee">
import SearchBar from './SearchBar'
import cheerio from 'cheerio'
export default
    data      : ->
        items     : []
        item      : null
        search_bar: null
        sidebar   : null
        content   : null
    components: {SearchBar}
    computed:
        item_type_class: ->
            this.item?.type.replace('/','-')
    methods   :
        select_item  : (item)->
            this.item = item
            history.replaceState(null, '', "##{dict.search_bar.search_text},#{dict.item.i}")
        render_item_content: (item)->
            item.$ = $ = cheerio.load(item.content.join('\n'))
            if item.type=='en/OALD'
                $('img').each (i,e)=>
                    $(e).attr 'src', (i,src) =>
                        "data:image/#{src.split('.').pop()};base64,#{item.assets[src[1..-1]]}"
                # 去除英音
                $('[resource="phon-gb"]').remove()
                $('.phon-gb').remove()
                $('[resource="uk_pron"]').remove()
                $('.chn').each (i,e)->
                    $(e).text (i,text)->
                        text.replace(/╱/g,'/').replace(/；/g,'、')
                $('.tx').each (i,e)->
                    $(e).text (i,text)->
                        text.replace(/╱/g,'/').replace(/；/g,'、')
                $('a[type="sound"]').each (i,e)=>
                    $(e).replaceWith("""
                    <audio id="audio-#{i}"
                        src="data:audio/wav;base64,#{item.assets[$(e).attr('href').replace('sound://','')]}">
                    </audio>
                    <span onclick="document.querySelector('#audio-#{i}').play()" style="cursor:pointer">▶</span>
                    """)
                setTimeout (->
                    document.querySelector('#audio-0')?.play()
                ), 200
                if item.origin
                    $_ = cheerio.load(item.origin)
                    $_($_('object')?[1]).attr 'data', (i, link)->
                        "http://www.dicts.cn#{link}"
                    $.root().append($_.html())
                if item.word_root
                    $_ = cheerio.load(item.word_root.replace(/(来自.*?\*)/g,'').replace(/[.。]/g,'。<br>'))
                    $('.h').after("<div class='word-root'>#{$_.html()}</div>")
            $.html()
        set_content_type_class: (item)->
            item.type.split('/')[0]
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
        jump: (event)->
            e=event.target
            if e.href?.startsWith('entry://')
                dict.search_bar.input_text=e.href[8..]
                dict.search_bar.search(e.href[8..])
    mounted  : ->
        window.dict = this
        sidebar     = this.sidebar    = this.$refs.sidebar
        search_bar  = this.search_bar = this.$refs.search_bar
        content     = this.content    = this.$refs.content
        
        dict.search_results = {} # 搜索结果缓存
        
        window.websocket_connect=->
            if !window.ws || Date.now()-ws.last_connected>1000*5
                console.log 'try sconnecting to the server'
                window.ws         = new WebSocket "ws://#{location.hostname}:8081/ws"
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
                ws.onerror = (event)->
                    console.log 'websocket error'
                    setTimeout websocket_connect, 5000
                ws.onclose = (event)->
                    console.log 'websocket closed'
                    setTimeout websocket_connect, 5000
            else
                console.error 'disconnected with the server'
        websocket_connect()
        
        
        
        document.onkeydown=(event)->
            key=event.key
            
            if event.getModifierState('Control') || event.getModifierState('Alt') then return
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
    html, body
        overflow-y hidden
    #dict
        width 100%
        height 97vh
        margin auto
        #header
            padding unset
            #search-bar
                .el-icon-search
                    font-size 1.7rem
                input
                    color #000
                    font-size 1.6rem
                    border-color #ccc
                    &:hover
                        border-color #888
        #body
            #sidebar
                min-width 250px
                border-right 1px solid #ccc
                border-left 1px solid #ccc
                border-bottom 1px solid #ccc
                padding-left 0.5rem
                word-wrap break-word
                word-break keep-all
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
                border-right 1px solid #ccc
                border-bottom 1px solid #ccc
                word-break keep-all
                word-wrap break-word
            #content.jp-JTS
                line-height 1.5rem
                padding-top 15px
                font-size 1.3rem
                #item-title
                    line-height 4rem
                    font-size 4rem
                    font-weight normal
                    margin-top 0
                    margin-bottom 15px
                /* 讲谈社日中 */
                .exp
                    margin-top 0
                    margin-bottom 0
                    color #0063b4
                    line-height 2rem
                .egs
                    margin-bottom 1rem
                    font-size 1.1rem
                /* 牛津高阶OALD */
            #content.en-OALD
                .word-root
                    margin-bottom 1rem
                    font-weight bold
                .d .chn
                    font-weight bold
                .gl
                    &:after
                        content ' '
                a
                    text-decoration none
                .top-g .z
                    display none
                .pos
                    display block
                    color #d11000
                    margin-top 1rem
                    font-weight bold
                    font-size 1.2rem
                .fayin
                    display inline
                .sd
                    display block
                    font-weight bold
                    margin-top 1rem
                .cf
                    color #0070C0
                    .swung-dash
                        margin-right .4em
                .cf[display="block"]
                    display block
                .pv, .id
                    display block
                    color #0070C0
                    font-weight bold
                .tx
                    &:before
                        content '　'
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
                            font-size 3rem
                            display block
                .id-g
                    display inline
                .revout + .id-g, .z + .pv-g
                    display block
                .revout
                    font-weight bold
                    margin-top 1rem
                    display block
                    &:before
                        content "【"
                    &:after
                        content "】"
                span.arbd1, span.dhb, span.fm, span.unei, .ndv, .cl, .ei, .ndv
                    padding-right 0.2em
                span.unsyn, span.unfm, .eb
                    padding-right 0.2em
                    text-transform uppercase
                    font-size smaller
                    color #C76E06
                .ungi, .gi, .g
                    color green
                    font-style italic
                .label-g
                    color green
                    .chn
                        display inline
                        &:before
                            content ""
                .dr-g
                    display block
                .phon-gb, .phon-us
                    color red
                .z_phon-us
                    display none
                .alt[q="also"]
                    display block
                .n-g
                    display block
                    margin-bottom 1rem
                .x-g
                    display block
                    margin-left 2em
                .n-g .xr-g
                    margin-left 2em
                .xr-g
                    display block
                .z_ei-g
                    display none
                .sense-g
                    display block
                .block-g
                    display block
                .ids-g, .pvs-g
                    display block
                .infl
                    display block
                .para
                    display block
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
                    background-color #C76E06
                    color #FAFAFA
                    text-transform uppercase
                .wfw
                    display inline
                .unbox
                    display block
                    padding-left 2px
                .tab
                    display table-cell
                    background-color #C76E06
                    color #FAFAFA
                    text-transform uppercase
                    text-align left
                .title
                    display block
                    text-transform uppercase
                    font-size small
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
                    text-transform uppercase
                .althead
                    text-transform uppercase
                .patterns
                    display block
                    clear both
                    .althead
                        display table-cell
                        margin 0px auto 0px auto
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
                    font-size 70%
                    color rgb(0, 0, 0)
                .symbols-para_square
                    color rgb(80, 80, 80)
                    font-size 65%
                .symbols-synsep
                    color rgb(80, 80, 80)
                    font-size 65%
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
                .z_n
                    display none
                .symbols-small_coresym
                    display none
                .z_ab
                    color green
                .gr, .subject
                    color green
                .dr
                    color blue
            
                #cigencizui-content
                    .word
                        display unset
                        background-color unset
                        color unset
                        text-transform unset
    
                
</style>

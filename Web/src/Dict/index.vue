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
            item.$ = $ = cheerio.load(item.content)
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
                        <span id="audio-#{i}" onclick="dict.play_spx('proncs/#{e.attribs.href.split('/').pop()}')" style="cursor:pointer">▶</span>
                    """)
                setTimeout (->
                    document.querySelector('#audio-0')?.click()
                ), 200
                if item.origin
                    $_ = cheerio.load(item.origin)
                    $_($_('object')?[1]).attr 'data', (i, link)->
                        "http://www.dicts.cn#{link}"
                    $.root().append($_.html())
                if item.word_root
                    $_ = cheerio.load(item.word_root.replace(/(来自.*?\*)/g,'').replace(/PIE\*/g,'').replace(/[.。]/g,'。<br>'))
                    $('.h').after("<div class='word-root'>#{$_.html()}</div>")
            $.html()
        set_content_type_class: (item)->
            item.type.split('/')[0]
        # 切换至 上一条目/下一条目
        next_item     : ->
            this.sidebar.$el.focus()
            this.select_item(this.items[this.item.i+1]) if this.item?.i+1<this.items.length
        previous_item : ->
            this.sidebar.$el.focus()
            this.select_item(this.items[this.item.i-1]) if this.item?.i-1>=0
        select_item_i : (i)->
            this.sidebar.$el.focus()
            this.select_item(dict.items[i]) if 0<=i<dict.items.length
        jump          : (event)->
            e=event.target
            if e.href?.startsWith('entry://')
                dict.search_bar.input_text=e.href[8..]
                dict.search_bar.search(e.href[8..])
        
        # Speex 解码
        play_spx      : (asset_key)->
            spx = dict.item.assets[asset_key]
#            spx = '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'
            spx = atob(spx)
            [samples, header] = Speex.decodeFile(spx)
            Speex.util.play(samples, header.rate)
        
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
        font-family 'XHei iOS7 Mono' ,Menlo, '华文细黑'
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

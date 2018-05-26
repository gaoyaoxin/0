<template lang="pug">
    #reader(v-if='chapter')
        h1 {{chapter.content[0]}}
        #content
</template>


<script lang="coffee">
    export default
        data: ->
            chapter_i    : 63
            chapter      : null
            chapter_cache: {}
            
            # 从该段落开始显示， -1 代表该章节已全部显示
            para_i       : 1
            para_stack   : []
            
        methods:
            request_chapter: (index)->
                if this.chapter_cache[index]
                    this.chapter_i = index
                    this.chapter = this.chapter_cache[index]
                    this.display_content()
                    return
                ws.send JSON.stringify
                    api : '/reader/get_chapter'
                    args: {index: index}
            
            display_content    : ->
                if this.para_i == -1 then return
                # 记录当前位置，以备回退
                this.para_stack.push(this.para_i)
                content = document.querySelector('#content')
                content.innerHTML = ''
                for para in this.chapter?.content[this.para_i..]
                    p = document.createElement('p')
                    p.innerHTML = para
                    content.appendChild(p)
                    if content.offsetTop + content.offsetHeight > window.innerHeight
                        content.removeChild(p)
                        return
                    this.para_i++
                this.para_i = -1
            
            next_page      : ->
                if this.para_i == -1
                    this.para_stack = []
                    this.next_chapter()
                else 
                    this.display_content()
            prev_page      : ->
                # 去掉当前开头状态
                this.para_stack.pop()
                if this.para_stack.length == 0
                    this.prev_chapter()
                else
                    # 设置为上次开头状态
                    this.para_i = this.para_stack.pop()
                    this.display_content()
                console.log this.para_i
                console.log this.para_stack
            
            next_chapter   : ->
                this.para_i = 1
                this.request_chapter(++this.chapter_i)
            prev_chapter   : ->
                this.para_i = 1
                this.request_chapter(--this.chapter_i) if this.chapter_i - 1 >= 0
        mounted   : ->
            window.reader = reader = this
            window.websocket_connect = ->
                if !window.ws || Date.now()-ws.last_connected>1000*5
                    console.log '尝试连接服务器'
                    window.ws         = new WebSocket "ws://#{location.hostname}:8081/ws"
                    ws.last_connected = new Date()
                    
                    # WebSocket 连接后获取 chapter
                    ws.onopen    = (event)->
                        console.log 'Websocket 已连接'
                        reader.request_chapter(reader.chapter_i)
                        
                    ws.onmessage = (event)->
                        resp = JSON.parse(event.data)
                        console.log resp
                        reader.chapter_cache[resp.retval.index] = reader.chapter = resp.retval
                        setTimeout(reader.display_content, 0)
                        
                    ws.onerror = (event)->
                        console.log 'Websocket 错误，5 秒后尝试重连'
                        setTimeout websocket_connect, 5000
                    ws.onclose = (event)->
                        console.log 'Websocket 关闭，5 秒后尝试重连'
                        setTimeout websocket_connect, 5000
                else
                    console.error 'disconnected with the server'
            websocket_connect()
            
            document.onkeydown = (event)->
                key = event.key
                # console.log key
                
                if event.getModifierState('Control') || event.getModifierState('Alt') then return
                if key == 'ArrowLeft'  || key == 'k'
                    reader.prev_page()
                if key == 'ArrowRight' || key == 'j'
                    reader.next_page()
</script>


<style lang="stylus">
    body
        overflow-y hidden
    #content
        line-height 1.5rem
        word-break keep-all
        word-wrap break-word
        padding-left 2rem
</style>

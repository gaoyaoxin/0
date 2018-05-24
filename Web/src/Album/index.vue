<template lang="pug">
    #album(v-if='script')
        #character(v-if='chr' v-html='chr.html+"："')
        #sentence(v-html='stc')
        div#caption 事件: {{script_i+1}}, 句子: {{line_i+1}}, 脚本文件: {{script.name}}
</template>


<script lang="coffee">
    export default
        data: ->
            script_i    : 0
            script      : null
            script_cache: {}
            
            line_i       : 0
            stc          : null
            
            # 当前角色
            chr         : null
            
        methods:
            load_script: (index)->
                if album.script_cache[index]
                    album.script = album.script_cache[index]
                    album.script_i = index
                    return
                ws.send JSON.stringify
                    api : '/album/get_script'
                    args: {index: index}
            next_stc   : ->
                if not (album.line_i < album.script.lines.length - 1) then return
                s = album.script.lines[album.line_i + 1]
                if s.text in album.script.characters
                    album.chr = s
                    album.line_i += 2
                    album.stc = album.script.lines[album.line_i].html
                else
                    album.line_i += 1
                    album.stc += '<br>' + album.script.lines[album.line_i].html
                setTimeout(window.scrollTo, 0.1, 0, document.body.scrollHeight)
            prev_stc   : ->
                album.line_i-- if album.line_i > 0
                album.stc = album.script.lines[album.line_i].html
            next_script: ->
                album.load_script(++album.script_i)
                album.line_i = 0
            prev_script: ->
                album.load_script(--album.script_i) if album.script_i - 1 >= 0
                album.line_i = 0
        mounted   : ->
            window.album = album = this
            window.websocket_connect = ->
                if !window.ws || Date.now()-ws.last_connected>1000*5
                    console.log '尝试连接服务器'
                    window.ws         = new WebSocket "ws://#{location.hostname}:8081/ws"
                    ws.last_connected = new Date()
                    
                    # WebSocket 连接后获取 script
                    ws.onopen    = (event)->
                        console.log 'Websocket 已连接'
                        album.load_script(0)
                        
                    ws.onmessage = (event)->
                        resp = JSON.parse(event.data)
                        console.log resp
                        album.script_cache[resp.retval.index] = album.script = resp.retval
                        album.stc = album.script.lines[album.line_i].html
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
                    album.prev_stc()
                if key == 'ArrowRight' || key == 'j' || key == ' '
                    album.next_stc()
                if key == 'ArrowUp'
                    album.prev_script()
                if key == 'ArrowDown'
                    album.next_script()
    
</script>


<style lang="stylus">
    #character
        min-height 3rem
        font-size 3rem
        margin-bottom 1rem
    #sentence
        font-size 3rem
        line-height 6rem
        word-break keep-all
        word-wrap break-word
    #caption
        position fixed
        bottom 1vh
        right 1vw
    rt
        user-select none
</style>

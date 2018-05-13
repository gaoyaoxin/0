<template lang="pug">
    #album
        h6#title 事件: {{script_i+1}}, 句子: {{stc_i+1}}, 脚本文件: {{script.file}} 
        #sentence(v-if='script' v-html='stc.html')
</template>
    

<script lang="coffee">
    export default
        data      : ->
            script_i    : 0
            script      : null
            script_cache: {}
            
            # sentence index
            stc_i       : 0
            
        computed:
            stc: ->
                this.script?.sentences[this.stc_i]
        methods   :
            load_script: (index)->
                if album.script_cache[index]
                    album.script = album.script_cache[index]
                    album.script_i = index
                    return
                ws.send JSON.stringify
                    api : '/album/get_script'
                    args: {index: index}
            next_stc   : ->
                album.stc_i++ if album.stc_i < album.script.sentences.length - 1
            prev_stc   : ->
                album.stc_i-- if album.stc_i > 0
            next_script: ->
                album.load_script(++album.script_i)
                album.stc_i = 0
            prev_script: ->
                album.load_script(--album.script_i) if album.script_i - 1 >= 0
                album.stc_i = 0
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
                if key == 'ArrowRight' || key == 'j'
                    album.next_stc()
                if key == 'ArrowUp'
                    album.prev_script()
                if key == 'ArrowDown'
                    album.next_script()
    
</script>


<style lang="stylus">
    h6
        font-weight normal
    #sentence
        font-size 5rem
        line-height 12rem
        word-break keep-all
        word-wrap break-word
    
</style>

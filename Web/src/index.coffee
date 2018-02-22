import Vue from 'vue' # The Vue build version to load with the `import` command (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import ElementUI from 'element-ui'
#import { Button, Select } from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import Dict from './Dict'
#import router from './router'

# Vue init
window.Vue=Vue
Vue.config.productionTip = false
Vue.use(ElementUI)

# root element
window.root=new Vue
    el: '#root'
#    router
    template: '<dict ref="dict"/>'
    components: {Dict}
    
# dict element
window.dict=root.dict=root.$refs.dict
# dict.search_bar
dict.search_bar=dict.$refs.search_bar

window.ws=new WebSocket 'ws://localhost:8081/ws'
###
todo: 连接服务器成功的状态展示
ws.onopen=->
    ws.send JSON.stringify
        api: 'search'
        args:
            input_str:'だく'
###

ws.onmessage=(e)->
    response=JSON.parse(e.data)
    console.log response
    response.retval.forEach (x,i)-> x.i=i
    root.$refs.dict.items=response.retval
    if response.retval
        dict.item=dict.items[0]
#        items.splice(0,items.length,...new_items.retval)

window.search_input=document.querySelector('input#search-input')
document.addEventListener 'keydown', (e)->
    if e.srcElement!=search_input
        console.log e.key
        switch true
            when e.key=='ArrowRight' || (dict.last_key!='Shift' && e.key=='Tab')
                dict.item=dict.items[dict.item.i+1] if dict.item.i+1<dict.items.length
                e.preventDefault()
            when e.key=='ArrowLeft'  || (dict.last_key=='Shift' && e.key=='Tab')
                dict.item=dict.items[dict.item.i-1] if dict.item.i-1>=0
                e.stopPropagation()
            when e.key=='s'
                search_input.focus()
                search_input.value=''
                e.preventDefault()
            when e.key=='e'
                search_input.focus()
                e.preventDefault()
            when !isNaN(e.key)
                console.log '!isNaN(e.key)'                
                dict.item=dict.items[e.key-1] if e.key-1<dict.items.length
        dict.last_key=e.key

#window.app=new Vue
#    computed:
#        g_data: -> this.abc.length
#    created: -> console.log "init: ",this.alist
    

#app.$watch 'abc',(n,o)->
#    console.log "before #{o}"
#    console.log "after #{n}"
#    console.log this


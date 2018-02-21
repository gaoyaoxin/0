import Vue from 'vue' # The Vue build version to load with the `import` command (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import ElementUI from 'element-ui'
#import { Button, Select } from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import Dict from './Dict'
#import router from './router'

Vue.config.productionTip = false
Vue.use(ElementUI)


window.dict=new Vue
    el: '#dict'
#    router
    template: '<dict/>'
    components: {Dict}



#Vue.component 'todo-item',
#    template:'<li>{{todo.text}}123</li>'
#    props:['todo']

#window.app=new Vue
#    el:'#dict'
#    data:
#        message:'a message'
#    data:
#        myfun: -> 
#            console.log 'in myfun'
#            'in myfun'
#        abc: '1234'
#        message: new Date().toUTCString()
#        seen: true
#        alist:[
#            {id:1, text:'a'}
#            {id:2, text:'b'}
#            {id:3, text:'c'}
#        ]
#        my_submit:->
#            console.log arguments
#    computed:
#        g_data: -> this.abc.length
#    created: -> console.log "init: ",this.alist
#    components: { TodoList:TodoList }
#    components: {App}
    

#window.todo_list_1=new Vue
#    el:'#todo-list-1'
#    data:
#        title:

#app.$watch 'abc',(n,o)->
#    console.log "before #{o}"
#    console.log "after #{n}"
#    console.log this


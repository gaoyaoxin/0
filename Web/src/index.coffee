# The Vue build version to load with the `import` command
# (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
#import App from './App'
#import router from './router'

Vue.config.productionTip = false

#new Vue({
#    el: '#app',
#    router,
#    components: { App },
#    template: '<App/>',
#    data:{
#        message:'message'
#    }
#})

Vue.component 'todo-item',
    template:'<li>{{todo.text}}123</li>'
    props:['todo']


window.app=new Vue
    el:'#app'
    data:
        myfun: -> 
            console.log 'in myfun'
            'in myfun'
        abc: '1234'
        message: new Date().toUTCString()
        seen: true
        alist:[
            {id:1, text:'a'}
            {id:2, text:'b'}
            {id:3, text:'c'}
        ]
        my_submit:->
            console.log arguments
#    created: -> console.log "init: ",this.alist


app.$watch 'abc',(n,o)->
    console.log "before #{o}"
    console.log "after #{n}"
    console.log this


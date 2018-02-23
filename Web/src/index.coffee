import Vue from 'vue' # The Vue build version to load with the `import` command (runtime-only or standalone) has been set in webpack.base.conf with an alias.
#import VueRouter from 'vue-router'
import ElementUI from 'element-ui'
#import { Button, Select } from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import Dict from './Dict'
#import router from './router'


# Vue,Vuex init
window.Vue=Vue
Vue.config.productionTip = false
Vue.use ElementUI
#Vue.use VueRouter

# elements init
window.root=new Vue
    el: '#root'
#    router
    template: '<dict ref="dict"/>'
    components: {Dict}
    mounted: ->
        console.log this.$refs
        this.dict=this.$refs.dict

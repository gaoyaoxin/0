import Vue from 'vue' # The Vue build version to load with the `import` command (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import Dict from './Dict/index.vue'

# 将Vue组件挂在到根元素
window.Vue               = Vue
Vue.config.productionTip = false
Vue.use ElementUI

window.root=new Vue
    el        : '#root'
    template  : '<dict ref="dict"/>'
    components: {Dict}
    mounted   : ->
        console.log this.$refs
        this.dict=this.$refs.dict


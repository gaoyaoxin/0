import Vue from 'vue' # The Vue build version to load with the `import` command (runtime-only or standalone) has been set in webpack.base.conf with an alias.
# import ElementUI from 'element-ui'
# import 'element-ui/lib/theme-chalk/index.css'

import Reader from './index.vue'

# 将Vue组件(Reader)挂载到根元素
window.Vue               = Vue
Vue.config.productionTip = false
# Vue.use ElementUI

window.root = new Vue
    el        : '#root'
    template  : '<reader ref="reader"/>'
    components: {Reader}
    mounted: ->
        console.log this.$refs
        this.reader = this.$refs.reader
    

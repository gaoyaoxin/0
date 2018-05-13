import Vue from 'vue' # The Vue build version to load with the `import` command (runtime-only or standalone) has been set in webpack.base.conf with an alias.
# import ElementUI from 'element-ui'
# import 'element-ui/lib/theme-chalk/index.css'

import Album from './index.vue'

# 将Vue组件(Album)挂载到根元素
window.Vue               = Vue
Vue.config.productionTip = false
# Vue.use ElementUI

window.root = new Vue
    el        : '#root'
    template  : '<album ref="album"/>'
    components: {Album}
    mounted: ->
        console.log this.$refs
        this.album = this.$refs.album
    

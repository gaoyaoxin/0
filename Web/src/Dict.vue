<template lang="pug">
    #dict
        h1 Dict
        #todo
        p after
</template>
<!--#app-->
    <!--//img(src="./assets/logo.png")-->
    <!--p-->
        <!--a(href="/#/") Index-->
        <!--|        -->
        <!--a(href="/#/dev") Dev-->
    <!--//router-view-->
    <!--| text-->
    <!---->

<script lang="coffee">
    import todo from './todo.vue'
    console.log todo
    debugger
    export default {
        components:{todo}
    }
</script>

<style lang="stylus">
    #dict
        text-align center
        color #000
</style>

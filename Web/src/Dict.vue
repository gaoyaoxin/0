<template lang="pug">
    #dict
        h1 Dict
        #todo-list
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
    import Vue from 'Vue'
    import TodoList from './TodoList'
    
    export default {}
</script>

<style lang="stylus">
    #dict
        text-align center
        color #000
</style>

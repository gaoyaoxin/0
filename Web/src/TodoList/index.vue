<template lang="pug">
    #todo-list
        h3 {{title}}
        input(placeholder='New Todo' @keyup.enter='add_item')
        ol.items
            li(v-for='item in items') {{item}}
</template>
    <!--.todo-list-->
        <!--p {{title}}-->
        <!--input.todo-add-item(@keyup.enter='add_item')-->
        <!--ol-->
            <!--li.todo-item(v-for='item,i in items') 第{{i}}个 {{item.text}}-->
        <!--p(v-if='!items.length') none-->

<script lang="coffee">
    export default
        props: ['title']
        data: ->
            items:['todo-1','todo-2']
        methods:
            add_item:(e)-> 
                this.items.push(e.target.value)
</script>

<style lang="stylus">
    #todo-list
        p
            color red
        span
            font-weight bold
</style> 

<template lang="pug">
    p TodoList template
</template>
    <!--.todo-list-->
        <!--p {{title}}-->
        <!--input.todo-add-item(@keyup.enter='add_item')-->
        <!--ol-->
            <!--li.todo-item(v-for='item,i in items') 第{{i}}个 {{item.text}}-->
        <!--p(v-if='!items.length') none-->



<script lang="coffee">
    console.log 'in TodoList.vue'
    export default {}
#        props: ['title']
#        data:
#            items: -> []
#        methods:
#            add_item:-> console.log 'in add_item'
</script>



<style lang="stylus">
    
</style> 

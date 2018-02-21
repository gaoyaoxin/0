<template lang="pug">
    #dict
        h1 Dict
        todo-list(title='My Todo List')
        p after
        el-button button
</template>


<script lang="coffee">
    import TodoList from './TodoList/index.vue'
    export default
        components:{TodoList}
</script>

<style lang="stylus">
    #dict
        text-align center
</style>

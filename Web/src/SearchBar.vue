<template lang="pug">
    #search-bar
        el-input#search-input(v-model='search_text' @input='search_change')
            el-button(slot='append' icon='el-icon-search')
</template>

<script lang="coffee">
    export default
        data:->
            search_text: 'init search text'
        methods:
            search_change:-> 
                console.log this.search_text
                ws.send 'search: '+this.search_text
        
</script>

<style lang="stylus">
    
</style>

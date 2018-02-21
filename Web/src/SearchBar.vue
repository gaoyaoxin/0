<template lang="pug">
    #search-bar
        el-input#search-input(v-model='search_text' @input='search_change')
            el-button(slot='append' icon='el-icon-search')
</template>

<script lang="coffee">
    import _ from 'underscore'
    export default
        data:->
            search_text: 'init search text'
        methods:
            search_change: _.debounce ->
                ws.send JSON.stringify
                    api:'search'
                    data: 'data'
            , 1000
        
</script>

<style lang="stylus">
    
</style>

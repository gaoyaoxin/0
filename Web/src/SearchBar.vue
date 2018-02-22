<template lang="pug">
    #search-bar
        el-input#search-input(v-model='search_text' @change='search_change')
            el-button(slot='append' icon='el-icon-search')
</template>

<script lang="coffee">
    import _ from 'underscore'
    export default
        data:->
            search_text: '输入查询单词'
        methods:
            search_change: ->
                    ws.send JSON.stringify
                        api: 'search'
                        args:
                            input_str: this.search_text
                    console.log 'input:',this.search_text
###
            search_change: _.debounce ->
                    ws.send JSON.stringify
                        api: 'search'
                        args:
                            input_str: this.search_text
                    console.log 'changed'
                , 1000
###
        
</script>

<style lang="stylus">
    
</style>

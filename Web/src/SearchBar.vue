<template lang="pug">
    #search-bar
        el-input#search-input(v-model='search_text' @change='search_change' @keydown.esc='search_input.blur()')
            el-button(slot='append' icon='el-icon-search')
</template>

<script lang="coffee">
    import _ from 'underscore'
    export default
        data:->
            search_text: ''
        methods:
            search_change: ->
                ws.send JSON.stringify
                    api: 'search'
                    args:
                        input_str: this.search_text
                console.log 'search:',this.search_text
                search_input.blur()
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

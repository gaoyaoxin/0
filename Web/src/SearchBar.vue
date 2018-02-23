<template lang="pug">
    #search-bar
        el-input#search-input(v-model='search_text' @keyup.native.enter='search(search_text)' ref='search_input' tabindex='0')
            el-button(slot='append' icon='el-icon-search')
</template>

<script lang="coffee">
    export default
        data:->
            search_text: ''
        methods:
            search:(search_text)->
                if search_text && search_text!=this.last_search_text
                    history.pushState({search_text},'',"##{search_text}")
                    if dict.search_results[search_text]
                        return dict.search_results[search_text]
                    ws.send JSON.stringify
                        api: 'search'
                        args:
                            search_text: search_text
                    console.log 'search:',search_text
                this.last_search_text=search_text
        mounted: ->
            this.search_input_el=document.querySelector('#search-input')
        
</script>

<style lang="stylus">
    #search-bar
        *
            border-radius unset
</style>

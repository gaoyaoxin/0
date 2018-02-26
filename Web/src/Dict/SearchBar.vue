<template lang="pug">
    #search-bar
        el-input#search-input(v-model='input_text' @keyup.native.enter='search(input_text)' ref='search_input' tabindex='0')
            el-button(slot='append' icon='el-icon-search')
</template>

<script lang="coffee">
    export default
        data:->
            search_text: ''
            input_text: ''
            last_search_text:''
            input_el:null
        methods:
            search:(input_text)->
                if input_text
                    this.search_text=input_text
                    history.pushState(null,'',"##{input_text},0")
                    if dict.search_results[input_text]
                        dict.items=dict.search_results[input_text]
                        dict.item=dict.items[0]
                    else
                        ws.send JSON.stringify
                            api: 'search'
                            args:
                                search_text: input_text
                        console.log 'search:',input_text
                    dict.search_bar.blur()
                    dict.sidebar.$el.focus()
            clear:->
                this.input_el.value=''
            focus:->
                this.input_el.focus()
            blur:->
                this.input_el.blur()
        mounted:->
            this.input_el=document.querySelector('#search-input')
        
</script>

<style lang="stylus">
    #search-bar
        *
            border-radius unset
</style>

<template lang="pug">
    #dict
        search-bar(ref='search_bar')
        #item-list
            .item(v-for='item in items')
                h2(v-html='item.title')
                .content(v-html='item.content')
</template>
    


<script lang="coffee">
    import SearchBar from './SearchBar.vue'
    window.ws=new WebSocket 'ws://localhost:8081/ws'
    ###
    ws.onopen=->
        ws.send JSON.stringify
            api: 'search'
            args:
                input_str:'だく'
    ###
    ws.onmessage=(e)->
        items=root.$refs.dict.items
        new_items=JSON.parse(e.data)
        console.log new_items
        items.splice(0,items.length,...new_items.retval)
    export default
        data: ->
            items:[]
        components:{SearchBar}
</script>



<style lang="stylus">
    #dict
        text-align center
</style>

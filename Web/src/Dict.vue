<template lang="pug">
    el-container#dict
        el-header#header
            search-bar(ref='search_bar')
        el-container#body
            el-aside#sidebar(width='20%')
                #item-list
                    .item(v-for='item in items')
                        h6.item-index(@click='select_item(item)') {{item.index}}
            el-main#content
                h1#item-title(v-html='item.title')
                #item-content(v-html='item.content')
</template>
    

<script lang="coffee">
    import SearchBar from './SearchBar.vue'
    export default
        data: ->
            items:[]
            item:{}
        methods:
            select_item:(item)->
                this.item=item
        components:{SearchBar}
</script>


<style lang="stylus">
    #dict
        width 97%
        margin auto
        #header
            padding unset
            #search-bar
                margin-top 20px
                .el-icon-search
                    font-size 1.7em
        #body
            #sidebar
                border-right 1px solid #eeeeee
                border-left 1px solid #eeeeee
                padding-left 1em
                h6.item-index 
                    font-size 1em
                    margin-top 1em
                    margin-bottom unset
            #content
                line-height 1.5em
                padding-top 30px
                border-right 1px solid #eeeeee
                font-size 1.3em
                #item-title
                    font-size 60px
                    font-weight normal
                    margin-top 0
                    margin-bottom 40px
                .exp
                    &:not(:first-child)
                        margin-top 1em
                    margin-top 0
                    margin-bottom 0
                    color #0070C0
</style>

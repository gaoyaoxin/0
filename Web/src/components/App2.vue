<template lang="pug">
    p in App.vue
</template>
<!--#app-->
    <!--//img(src="./assets/logo.png")-->
    <!--p-->
        <!--a(href="/#/") Index-->
        <!--|        -->
        <!--a(href="/#/dev") Dev-->
    <!--//router-view-->
    <!--| text-->
    <!---->

<script lang="coffee">
#console.log 'in App.vue module'
#export default
#    name: 'app'
#    data: (comp)->
#        console.log "in App.vue export"
#        console.log arguments
##        message:"App.vue export #{input}"
#        new Object()
</script>

<style lang="stylus">
#app
    text-align: center;
    color:#000;
</style>

<template lang="pug">
div#app
    img(src="./assets/logo.png")
    p
        a(href="/#/") Index
    p
        a(href="/#/dev") Dev
    router-view
</template>

<script lang="coffee">
export default
    name: 'app'
</script>

<style lang="stylus">
#app
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color:#000000;
    margin-top: 60px;
</style>

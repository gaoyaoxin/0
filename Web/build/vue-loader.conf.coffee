get_css_loaders = (options) ->
    
    # generate loader string to be used with extract text plugin
    generate_loaders = (loader, loaderOptions) ->
        loaders = [cssLoader, postcssLoader]
        if loader
            loaders.push
                loader: loader + '-loader'
                options: Object.assign({}, loaderOptions, sourceMap: true)
        # Extract CSS when that option is specified
        # (which is the case during production build)
        if options.extract
            ExtractTextPlugin.extract
                use: loaders
                fallback: 'vue-style-loader'
        else
            [ 'vue-style-loader' ].concat loaders
    
    options = options or {}
    cssLoader = 
        loader: 'css-loader'
        options: sourceMap: true
    postcssLoader = 
        loader: 'postcss-loader'
        options: sourceMap: options.sourceMap
    
    # https://vue-loader.vuejs.org/en/configurations/extract-css.html
    {
        css: generate_loaders()
        postcss: generate_loaders()
        less: generate_loaders('less')
        sass: generate_loaders('sass', indentedSyntax: true)
        scss: generate_loaders('sass')
        stylus: generate_loaders('stylus')
        styl: generate_loaders('stylus')
    }

module.exports =
    loaders: get_css_loaders(
        sourceMap: true
        extract: false)
    cssSourceMap: true
    cacheBusting: true
    transformToRequire:
        video: [
            'src'
            'poster'
        ]
        source: 'src'
        img: 'src'
        image: 'xlink:href'

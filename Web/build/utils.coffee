path = require 'path'
config = require('./base.env')
ExtractTextPlugin = require('extract-text-webpack-plugin')
packageConfig = require('../package.json')

exports.assetsPath = (_path) ->
    assetsSubDirectory = if process.env.NODE_ENV == 'production' then config.build.assetsSubDirectory else config.dev.assetsSubDirectory
    path.posix.join assetsSubDirectory, _path

exports.cssLoaders = (options) ->
    # generate loader string to be used with extract text plugin

    generateLoaders = (loader, loaderOptions) ->
        loaders = if options.usePostCSS then [
            cssLoader
            postcssLoader
        ] else [ cssLoader ]
        if loader
            loaders.push
                loader: loader + '-loader'
                options: Object.assign({}, loaderOptions, sourceMap: options.sourceMap)
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
        options: sourceMap: options.sourceMap
    postcssLoader = 
        loader: 'postcss-loader'
        options: sourceMap: options.sourceMap
    # https://vue-loader.vuejs.org/en/configurations/extract-css.html
    {
        css: generateLoaders()
        postcss: generateLoaders()
        less: generateLoaders('less')
        sass: generateLoaders('sass', indentedSyntax: true)
        scss: generateLoaders('sass')
        stylus: generateLoaders('stylus')
        styl: generateLoaders('stylus')
    }

# Generate loaders for standalone style files (outside of .vue)

exports.styleLoaders = (options) ->
    output = []
    loaders = exports.cssLoaders(options)
    for extension of loaders
        loader = loaders[extension]
        output.push
            test: new RegExp('\\.' + extension + '$')
            use: loader
    output

exports.createNotifierCallback = ()=>
    notifier = require('node-notifier')
    (severity, errors) =>
        if severity != 'error'
            return
        error = errors[0]
        filename = error.file and error.file.split('!').pop()
        notifier.notify
            title: packageConfig.name
            message: severity + ': ' + error.name
            subtitle: filename or ''
            icon: path.join(__dirname, 'logo.png')
        return

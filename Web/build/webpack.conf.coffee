# see http://vuejs-templates.github.io/webpack for documentation.
path = require('path')
portfinder = require('portfinder')
webpack = require('webpack')

ExtractTextPlugin = require('extract-text-webpack-plugin')
HtmlWebpackPlugin = require('html-webpack-plugin')
FriendlyErrorsPlugin = require('friendly-errors-webpack-plugin')
# CopyWebpackPlugin = require('copy-webpack-plugin')

vueLoaderConfig = require('./vue-loader.conf')


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

get_style_loaders=(options)->
    # Generate loaders for standalone style files (outside of .vue)
    output = []
    loaders = get_css_loaders(options)
    for extension of loaders
        loader = loaders[extension]
        output.push
            test: new RegExp('\\.' + extension + '$')
            use: loader
    output

config = 
    dev: 
        # Paths
        proxyTable: {}
        
        
        # If you have problems debugging vue-files in devtools, set this to false - it *may* help
        # https://vue-loader.vuejs.org/en/options.html#cachebusting
        cacheBusting: true,
        
        cssSourceMap: true

    build: 
        
        
        # https://webpack.js.org/configuration/devtool/#production
        devtool: '#source-map',
        
        # Gzip off by default as many popular static hosts such as
        # Surge or Netlify already gzip all static assets for you.
        # Before setting to `true`, make sure to:
        # npm install --save-dev compression-webpack-plugin
        productionGzip: false,
        productionGzipExtensions: ['js', 'css'],
        
        # Run the build command with an extra argument to
        # View the bundle analyzer report after build finishes:
        # `npm run build --report`
        # Set to `true` or `false` to always turn it on or off
        bundleAnalyzerReport: true


resolve = (dir) ->
    path.join __dirname, '..', dir

webpack_config =
    context: path.resolve(__dirname, '../')
    entry: 
        index: './src/index.coffee'
    output:
        path      : path.resolve(__dirname, '../dist')
        filename  : 'bundle.js'
        publicPath: '/'
        pathinfo  : true
    resolve:
        extensions: [
            '.coffee'
            '.js'
            '.vue'
            '.json'
        ]
        alias:
            'vue$': 'vue/dist/vue.esm.js'
            '@': resolve('src')
    module: rules: [
        test: /\.vue$/
        loader: 'vue-loader'
        options: vueLoaderConfig
    ,
        test: /\.coffee$/
        loader: 'coffee-loader'
        include: [
            resolve('src')
            resolve('test')
        ]
    ,
        test: /\.js$/
        loader: 'babel-loader'
        include: [
            resolve('src')
            resolve('test')
            resolve('node_modules/webpack-dev-server/client')
        ]
    ,
        test: /\.(png|jpe?g|gif|svg|mp4|webm|ogg|mp3|wav|flac|aac|woff2?|eot|ttf|otf)(\?.*)?$/
        loader: 'url-loader'
        options:
            limit: 10000
            name: '[path][name].[ext]'
            context   : 'src'
    ,
        test   : /\.ico$/
        loader : 'file-loader'
        options:
            name      : '[path][name].[ext]'
            context   : resolve 'src'
            # mimetype: extname
    ,
        test   : /\.txt$/
        loader : 'raw-loader'
    ,
        test   : /\.pug$/
        loader : 'pug-loader'
        options:
            pretty: true
    ].concat(get_style_loaders())
    
    plugins: [
        new webpack.HotModuleReplacementPlugin()
        new webpack.NamedModulesPlugin()
        new webpack.NoEmitOnErrorsPlugin()
        new HtmlWebpackPlugin(
            name: 'index.html'
            template: 'src/index.pug'
            inject: true
         )
#        new CopyWebpackPlugin([ {
#            from: path.resolve(__dirname, '../static')
#            to: config.dev.assetsSubDirectory
#            ignore: [ '.*' ]
#        } ])
    ]
    
    # cheap-module-eval-source-map is faster for development
    # Source Maps https://webpack.js.org/configuration/devtool/#development
    devtool: 'cheap-module-eval-source-map',
    
    devServer:
        clientLogLevel: 'warning'
#        historyApiFallback:
#            rewrites: [{
#                from: /.*/
#                to  : '/index.html'
#            }]
        hot: true
        contentBase: false
        compress: true
        host: process.env.HOST || '0.0.0.0'
        port: process.env.PORT && Number(process.env.PORT) || 8080
        open: false
        overlay: true # error overlay
        proxy: config.dev.proxyTable
        quiet: true # necessary for FriendlyErrorsPlugin
        watchOptions: 
            poll: false
#        notifyOnErrors: true

    node:
        # prevent webpack from injecting useless setImmediate polyfill because Vue
        # source contains it (although only uses it if it's native).
        setImmediate : false
        # prevent webpack from injecting mocks to Node native modules
        # that does not make sense for the client
        dgram        : 'empty'
        fs           : 'empty'
        net          : 'empty'
        tls          : 'empty'
        child_process: 'empty'


module.exports = new Promise((resolve, reject) =>
    portfinder.basePort = webpack_config.devServer.port
    portfinder.getPort (err, port) =>
        if err
            reject err
        else
            process.env.PORT = port # publish the new Port, necessary for e2e tests
            webpack_config.devServer.port = port # add port to devServer config
            webpack_config.plugins.push new FriendlyErrorsPlugin(
                compilationSuccessInfo: messages: [ "Your application is running here: http://#{webpack_config.devServer.host}:#{port}" ]
                onErrors: if config.dev.notifyOnErrors then (()=>
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
                )() else undefined)
            resolve webpack_config
        return
    return
)

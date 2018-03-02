# see http://vuejs-templates.github.io/webpack for documentation.
path       = require('path')
portfinder = require('portfinder')
webpack    = require('webpack')

HtmlWebpackPlugin    = require('html-webpack-plugin')
FriendlyErrorsPlugin = require('friendly-errors-webpack-plugin')


webpack_config =
    entry: 
        index: './src/index.coffee'
    output:
        path      : __dirname+'/dist'
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
            '@': 'src'
    module: rules: [
        test   : /\.vue$/
        loader : 'vue-loader'
        options:
            loaders           :
                css: ['vue-style-loader', {loader: 'css-loader', options: {sourceMap: true}}, {loader: 'stylus-loader'}]
            cssSourceMap      : true
            # If you have problems debugging vue-files in devtools, set this to false - it *may* help
            # https://vue-loader.vuejs.org/en/options.html#cachebusting
            cacheBusting      : true
            transformToRequire:
                video : ['src', 'poster']
                source: 'src'
                img   : 'src'
                image : 'xlink:href'
    ,
        test   : /\.coffee$/
        loader : 'coffee-loader'
    ,
        test   : /\.pug$/
        loader : 'pug-loader'
        options:
            pretty: true
    ,
        test   : /\.css$/
        use    : [
            'vue-style-loader'
            {loader: 'css-loader', options: {sourceMap: true}}]
    ,
        test   : /\.styl$/
        use    : [
            'vue-style-loader'
            {loader: 'css-loader', options: {sourceMap: true}}
            {loader: 'stylus-loader'}]
    ,
        test   : /\.(png|jpe?g|gif|svg|mp4|webm|ogg|mp3|wav|flac|aac|woff2?|eot|ttf|otf)(\?.*)?$/
        loader : 'url-loader'
        options:
            limit  : 10000
            name   : '[path][name].[ext]'
            context: 'src'
    ,
        test   : /\.ico$/
        loader : 'file-loader'
        options:
            name      : '[path][name].[ext]'
            context   : 'src'
            # mimetype: extname
    ,
        test   : /\.txt$/
        loader : 'raw-loader'
    ]
    
    plugins: [
        new webpack.HotModuleReplacementPlugin()
        new webpack.NamedModulesPlugin()
        new webpack.NoEmitOnErrorsPlugin()
        new HtmlWebpackPlugin(
            name    : 'index.html'
            template: 'src/index.pug'
            inject  : true
         )
    ]
    
    # cheap-module-eval-source-map is faster for development
    # Source Maps https://webpack.js.org/configuration/devtool/#development
    devtool: 'cheap-module-eval-source-map',
    
    devServer:
        clientLogLevel: 'warning'
        hot           : true
        contentBase   : false
        compress      : true
        host          : process.env.HOST || '0.0.0.0'
        port          : process.env.PORT && Number(process.env.PORT) || 8080
        open          : false
        overlay       : true # error overlay
        proxy         : {}
        quiet         : true # necessary for FriendlyErrorsPlugin
        watchOptions  : poll: false
        # historyApiFallback:
        #     rewrites: [{
        #         from: /.*/
        #         to  : '/index.html'
        #     }]
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


module.exports = new Promise (resolve, reject) =>
    portfinder.basePort = webpack_config.devServer.port
    portfinder.getPort (err, port) =>
        if err
            reject err
        else
            process.env.PORT = port # publish the new Port, necessary for e2e tests
            webpack_config.devServer.port = port # add port to devServer config
            webpack_config.plugins.push new FriendlyErrorsPlugin
                compilationSuccessInfo: messages: [ "Your application is running here: http://#{webpack_config.devServer.host}:#{port}" ]
                onErrors: (()=>
                    notifier = require('node-notifier')
                    (severity, errors) =>
                        if severity != 'error'
                            return
                        error = errors[0]
                        filename = error.file and error.file.split('!').pop()
                        notifier.notify
                            title: error.toString()
                            message: severity + ': ' + error.name
                            subtitle: filename || ''
                        return
                )()
            resolve webpack_config
        return
    return


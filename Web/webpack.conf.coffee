# see http://vuejs-templates.github.io/webpack for documentation.
portfinder = require('portfinder')
webpack    = require('webpack')

HtmlWebpackPlugin = require('html-webpack-plugin')


webpack_config =
    entry: # 从每个入口开始构建依赖图，生成多个 bundle.js 文件
        index: './src/index.coffee'
        album: './src/Album/index.coffee'
    output:
        path      : __dirname+'/dist'
        filename  : '[name].js'
        publicPath: '/' # 通过 URL 访问的路径，如 /index.js
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
        new HtmlWebpackPlugin( # 最终生成一个 html 文件
            filename    : 'index.html'      # 生成的 html 路径，默认为 /index.html
            template    : 'src/index.pug'
            inject      : false             # 是否自动插入 bundle.js（默认插入） ，插入位置等
         )
        new HtmlWebpackPlugin(
            filename    : 'album.html'
            template    : 'src/Album/index.pug'
            inject      : false
         )
    ]
    
    # cheap-module-eval-source-map is faster for development
    # Source Maps https://webpack.js.org/configuration/devtool/#development
    devtool: 'cheap-module-eval-source-map',
    
    devServer:
        host            : process.env.HOST || '0.0.0.0'
        port            : process.env.PORT && Number(process.env.PORT) || 8080
        publicPath      : '/'    # 部署网站的根目录
        contentBase     : 'root' # 将项目中的 root 文件夹作为部署网站的 Web 文件根目录，与 URL 对应
        hot             : true
        compress        : true
        clientLogLevel  : 'warning'
        open            : false
        overlay         : true   # error overlay
        proxy           : {}
        quiet           : false
        watchOptions    : poll: false
        disableHostCheck: true
        # historyApiFallback:
        #     rewrites: [{
        #         from: /.*/
        #         to  : '/index.html'
        #     }]

    node: # prevent webpack from injecting useless setImmediate polyfill because Vue source contains it (although only uses it if it's native).
        setImmediate : false
        # prevent webpack from injecting mocks to Node native modules that does not make sense for the client
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
            resolve webpack_config
        return
    return


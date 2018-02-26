utils = require('./utils')
webpack = require('webpack')
config = require('./base.env')
merge = require('webpack-merge')
path = require('path')
baseWebpackConfig = require('./webpack.base.conf')
CopyWebpackPlugin = require('copy-webpack-plugin')
HtmlWebpackPlugin = require('html-webpack-plugin')
FriendlyErrorsPlugin = require('friendly-errors-webpack-plugin')
portfinder = require('portfinder')

HOST = process.env.HOST
PORT = process.env.PORT && Number(process.env.PORT)

devWebpackConfig = merge(baseWebpackConfig,
    module: rules: utils.styleLoaders(
        sourceMap: config.dev.cssSourceMap
        usePostCSS: true)
    # cheap-module-eval-source-map is faster for development
    devtool: config.dev.devtool
    # these devServer options should be customized in /cfg/index.coffee
    devServer:
        clientLogLevel: 'warning'
        historyApiFallback: rewrites: [ {
            from: /.*/
            to: path.posix.join(config.dev.assetsPublicPath, 'index.html')
        } ]
        hot: true
        contentBase: false
        compress: true
        host: HOST or config.dev.host
        port: PORT or config.dev.port
        open: config.dev.autoOpenBrowser
        overlay: if config.dev.errorOverlay then { warnings: false, errors: true } else false
        publicPath: config.dev.assetsPublicPath
        proxy: config.dev.proxyTable
        quiet: true # necessary for FriendlyErrorsPlugin
        watchOptions: poll: config.dev.poll
    plugins: [
        new (webpack.DefinePlugin)('process.env': require('./base.env'))
        new (webpack.HotModuleReplacementPlugin)
        new (webpack.NamedModulesPlugin)
        new (webpack.NoEmitOnErrorsPlugin)
        new HtmlWebpackPlugin(
            filetype: 'html'
            template: '!!pug-loader!src/index.pug'
            inject: true)
###
        new CopyWebpackPlugin([ {
            from: path.resolve(__dirname, '../static')
            to: config.dev.assetsSubDirectory
            ignore: [ '.*' ]
        } ])
###
    ])
module.exports = new Promise((resolve, reject) =>
    portfinder.basePort = process.env.PORT or config.dev.port
    portfinder.getPort (err, port) =>
        if err
            reject err
        else
            # publish the new Port, necessary for e2e tests
            process.env.PORT = port
            # add port to devServer config
            devWebpackConfig.devServer.port = port
            # Add FriendlyErrorsPlugin
            devWebpackConfig.plugins.push new FriendlyErrorsPlugin(
                compilationSuccessInfo: messages: [ "Your application is running here: http://#{devWebpackConfig.devServer.host}:#{port}" ]
                onErrors: if config.dev.notifyOnErrors then utils.createNotifierCallback() else undefined)
            resolve devWebpackConfig
        return
    return
)

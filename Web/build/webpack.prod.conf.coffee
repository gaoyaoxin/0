path = require('path')
utils = require('./utils')
webpack = require('webpack')
config = require('./base.env')
merge = require('webpack-merge')
baseWebpackConfig = require('./webpack.base.conf')
CopyWebpackPlugin = require('copy-webpack-plugin')
HtmlWebpackPlugin = require('html-webpack-plugin')
ExtractTextPlugin = require('extract-text-webpack-plugin')
OptimizeCSSPlugin = require('optimize-css-assets-webpack-plugin')
UglifyJsPlugin = require('uglifyjs-webpack-plugin')

env = require('../cfg/prod.env')

webpackConfig = merge(baseWebpackConfig,
    module: 
        rules: utils.styleLoaders(
        sourceMap: config.build.productionSourceMap
        extract: true
        usePostCSS: true)
    devtool: if config.build.productionSourceMap then config.build.devtool else false
    output:
        path: config.build.assetsRoot
        filename: utils.assetsPath('js/[name].[chunkhash].js')
        chunkFilename: utils.assetsPath('js/[id].[chunkhash].js')
    plugins: [
        # http://vuejs.github.io/vue-loader/en/workflow/production.html
        new (webpack.DefinePlugin)('process.env': env)
        
        new UglifyJsPlugin(
            uglifyOptions: compress: warnings: false
            sourceMap: config.build.productionSourceMap
            parallel: true)
        
        # extract css into its own file
        new ExtractTextPlugin(
            filename: utils.assetsPath('css/[name].[contenthash].css')
            # Setting the following option to `false` will not extract CSS from codesplit chunks.
            # Their CSS will instead be inserted dynamically with style-loader when the codesplit chunk has been loaded by webpack.
            # It's currently set to `true` because we are seeing that sourcemaps are included in the codesplit bundle as well when it's `false`, 
            # increasing file size: https://github.com/vuejs-templates/webpack/issues/1110
            allChunks: true)
        
        # Compress extracted CSS. We are using this plugin so that possible
        # duplicated CSS from different components can be deduped.
        new OptimizeCSSPlugin(cssProcessorOptions: if config.build.productionSourceMap then { safe: true, map: { inline: false } } else { safe: true })
        
        # generate dist index.html with correct asset hash for caching.
        # you can customize output by editing /index.html
        new HtmlWebpackPlugin(
            filename: config.build.index
            template: '!!pug-loader!src/index.pug'
            inject: true
            minify:
                removeComments: true
                collapseWhitespace: true
                removeAttributeQuotes: true
                # more options: https://github.com/kangax/html-minifier#options-quick-reference
            chunksSortMode: 'dependency')
        
        # keep module.id stable when vendor modules does not change
        new (webpack.HashedModuleIdsPlugin)
        
        # enable scope hoisting
        new (webpack.optimize.ModuleConcatenationPlugin)
        
        # split vendor js into its own file
        new (webpack.optimize.CommonsChunkPlugin)(
            name: 'vendor'
            minChunks: (module) ->
                # any required modules inside node_modules are extracted to vendor
                module.resource && /\.js$/.test(module.resource) && module.resource.indexOf(path.join(__dirname, '../node_modules')) == 0
        )
        
        # extract webpack runtime and module manifest to its own file 
        # in order to prevent vendor hash from being updated whenever app bundle is updated
        new (webpack.optimize.CommonsChunkPlugin)(
            name: 'manifest'
            minChunks: Infinity)
        
        # This instance extracts shared chunks from code splitted chunks and bundles them
        # in a separate chunk, similar to the vendor chunk
        # see: https://webpack.js.org/plugins/commons-chunk-plugin/#extra-async-commons-chunk
        new (webpack.optimize.CommonsChunkPlugin)(
            name: 'app'
            async: 'vendor-async'
            children: true
            minChunks: 3)
        
        # copy custom static assets
###
        new CopyWebpackPlugin([ {
            from: path.resolve(__dirname, '../static')
            to: config.build.assetsSubDirectory
            ignore: [ '.*' ]
        } ])
###
    ])

if config.build.productionGzip
    CompressionWebpackPlugin = require('compression-webpack-plugin')
    webpackConfig.plugins.push new CompressionWebpackPlugin(
        asset: '[path].gz[query]'
        algorithm: 'gzip'
        test: new RegExp('\\.(' + config.build.productionGzipExtensions.join('|') + ')$')
        threshold: 10240
        minRatio: 0.8)

if config.build.bundleAnalyzerReport
    BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin
    webpackConfig.plugins.push new BundleAnalyzerPlugin

module.exports = webpackConfig

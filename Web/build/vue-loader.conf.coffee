utils = require('./utils')
config = require('./base.env')
isProduction = process.env.NODE_ENV == 'production'
sourceMapEnabled = if isProduction then config.build.productionSourceMap else config.dev.cssSourceMap

module.exports =
    loaders: utils.cssLoaders(
        sourceMap: sourceMapEnabled
        extract: isProduction)
    cssSourceMap: sourceMapEnabled
    cacheBusting: config.dev.cacheBusting
    transformToRequire:
        video: [
            'src'
            'poster'
        ]
        source: 'src'
        img: 'src'
        image: 'xlink:href'

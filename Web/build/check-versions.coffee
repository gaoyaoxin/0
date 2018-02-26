chalk = require('chalk')
semver = require('semver')
packageConfig = require('../package.json')
shell = require('shelljs')

versionRequirements = [ {
    name: 'node'
    currentVersion: semver.clean(process.version)
    versionRequirement: packageConfig.engines.node
} ]

exec = (cmd) ->
    require('child_process').execSync(cmd).toString().trim()

if shell.which('npm')
    versionRequirements.push
        name: 'npm'
        currentVersion: exec('npm --version')
        versionRequirement: packageConfig.engines.npm

module.exports = ->
    warnings = []
    i = 0
    while i < versionRequirements.length
        mod = versionRequirements[i]
        if !semver.satisfies(mod.currentVersion, mod.versionRequirement)
            warnings.push mod.name + ': ' + chalk.red(mod.currentVersion) + ' should be ' + chalk.green(mod.versionRequirement)
        i++
    if warnings.length
        console.log ''
        console.log chalk.yellow('To use this template, you must update following to modules:')
        console.log()
        i = 0
        while i < warnings.length
            warning = warnings[i]
            console.log '  ' + warning
            i++
        console.log()
        process.exit 1
    return

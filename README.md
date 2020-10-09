# Experitest Integration for XL Release

![GitHub release](https://img.shields.io/github/release/xebialabs-community/xlr-experitest-plugin.svg)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Github All Releases](https://img.shields.io/github/downloads/xebialabs-community/xlr-experitest-plugin/total.svg)](https://github.com/xebialabs-community/xlr-experitest-plugin/releases)
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-blue.svg)](https://github.com/RichardLitt/standard-readme)

## Installation

### Requirements

1. XL Release 9.6+

### Building the plugin
The gradle wrapper facilitates building the plugin.  Use the following command to build using [Gradle](https://gradle.org/):
```bash
./gradlew clean build
```
The built plugin, along with other files from the build, can then be found in the _build_ folder.

### Adding the plugin to XL Release

Download the latest version of the plugin from the [releases page](https://github.com/xebialabs-community/xlr-experitest-plugin/releases).  The plugin can then be installed through the XL Release graphical interface or the server backend.  For additional detail, please refer to [the docs.xebialabs.com documentation on XLR plugin installation](https://docs.xebialabs.com/xl-release/how-to/install-or-remove-xl-release-plugins.html)

## Usage

__Available Tasks__: None

__Available Triggers__: None

__Available Dashboard Tiles__: Test History Tile, Test Pass Rate Tile

### Tiles

#### Test History Tile
Properties:
* Experitest Instance _input_ 
* Project Name _input_ 
* Max Count _input_ 
   * Maximum number of tests to display.

#### Test Pass Rate Tile
Properties:
* Experitest Instance _input_ 
* Project Name _input_ 
* Max Count _input_ 
   * Maximum number of tests to display.

## Contributing

Please review the contributing guidelines for _xebialabs-community_ at [http://xebialabs-community.github.io/](http://xebialabs-community.github.io/)

## License

This community plugin is licensed under the [MIT license](https://opensource.org/licenses/MIT).

See license in [LICENSE.md](LICENSE.md)
